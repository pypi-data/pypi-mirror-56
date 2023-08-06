import threading
import sys
import json
import traceback
from flask import request
from uuid import uuid4
from watched_schema import validators
from markdown import markdown
from .context import Context
from .config import config
from .common import logger

class TunnelResponse:
    def __init__(self, r):
        self.r = r

    @property
    def error(self):
        return self.r['error']

    @property
    def status_code(self):
        return self.r['status']

    @property
    def url(self):
        return self.r['url']

    @property
    def headers(self):
        return self.r['headers']

    def json(self):
        return self.r['json']

    @property
    def text(self):
        if 'text' not in self.r and 'json' in self.r:
            return json.dumps(self.json())
        return self.r['text']

    @property
    def content(self):
        if 'raw' not in self.r:
            return self.text
        return self.r['raw'].decode('base64')

class HttpContext(Context):
    def __init__(self, addon_id, action):
        super(HttpContext, self).__init__(addon_id, action)
        self.result_channel = None
        self.event = threading.Event()

    def send(self, status, body):
        if self.result_channel:
            data = json.dumps([status, body])
            config.cache.set('task:response:'+self.result_channel, data)
        else:
            self.response = status, body
            self.event.set()

    def fetch_remote(self, url, timeout=30, **kwargs):
        # Create and send task
        id = str(uuid4())
        task = {
            'id': id,
            'action': 'fetch',
            'url': url,
            'params': kwargs,
        }
        validators['task']['task'](task)
        config.cache.set('task:wait:'+id, '1')
        print('task.create', id)
        self.send(428, task)

        # Wait for result
        data = config.cache.wait_key('task:result:'+id, timeout, True)
        result_channel, result = json.loads(data)
        if not result_channel:
            raise ValueError('Missing result_channel')
        self.result_channel = result_channel
        print('task.result.get', result["id"])
        validators['task']['result'](result)
        return TunnelResponse(result)

def validate_response(ctx, status, response):
    if status == 500:
        validators['models']['apiError'](response)
    elif status == 428:
        validators['task']['task'](response)
    else:
        ctx.schema['response'](response)

def task(ctx, result):
    validators['task']['result'](result)

    # Make sure the key exists to prevent spamming
    if not config.cache.get('task:wait:'+result['id']):
        raise ValueError('Task wait key '+result['id']+' does not exists')
    config.cache.delete('task:wait:'+result['id'])

    # Set the result
    logger.warning('task.result.set %r', result['id'])
    result_channel = str(uuid4())
    raw = json.dumps([result_channel, result])
    config.cache.set('task:result:'+result['id'], raw)

    # Wait for the response
    data = config.cache.wait_key('task:response:'+result_channel)
    status, response = json.loads(data)
    validate_response(ctx, status, response)
    return json.dumps(response), status, {'Content-Type': 'application/json'}

# Health check

def health():
    return 'OK'

# Index page

def index():
    return markdown('OK')

# Addon routes

def run(addon_id, action):
    ctx = HttpContext(addon_id, action)
    req = request.json
    if req.get('kind') == 'taskResult':
        return task(ctx, req)

    class Thread(threading.Thread):
        def run(self):
            try:
                status, response = 200, ctx.run(req)
            except Exception as e:
                status, response = 500, {"error": e.args[0]}
                traceback.print_exc()
            validate_response(ctx, status, response)
            ctx.send(status, response)
    Thread().start()
    ctx.event.wait()
    status, response = ctx.response
    return json.dumps(response), status, {'Content-Type': 'application/json'}

def addon_index():
    return run(config.repository.id, 'addons')

def addon_infos(addon_id):
    return run(addon_id, 'infos')

def addon_action(addon_id, action):
    return run(addon_id, action)

def register_routes(app):
    app.route('/health', methods=['GET'])(health)
    app.route('/index', methods=['GET'])(index)
    app.route('/addons', methods=['POST'])(addon_index)
    app.route('/<addon_id>', methods=['POST'])(addon_infos)
    app.route('/<addon_id>/<action>', methods=['POST'])(addon_action)
