import json
from flask import Flask
from .config import config
from .addon import create_addon
from .context import Context
from .router import register_routes
from .test import test_addons

def setup(props, cache=None):
    config.set_cache(cache)
    new_props = {'mirrors': []}
    new_props.update(props)
    new_props.update({
      'type': 'repository',
      'sdk': {
        'engine': 'python',
        'version': '0.0.0'
      }
    })
    config.set_repository(create_addon(new_props))
    print(config.repository.props)

def _parse(args):
    req = {}
    for arg in args:
        key, value = arg.split('=', 1)
        try:
            value = json.loads(value)
        except Exception:
            pass
        req[key] = value
    return req

def main(*args):
    try:
        cmd = args[0]
    except IndexError:
        cmd = None

    if cmd == 'start':
        app = Flask(__name__)
        register_routes(app)
        app.run('0.0.0.0', 3000, debug=True if 'debug' in args else False)

    elif cmd == 'call':
        data = _parse(args[1:])
        addon_id = data.pop('addon_id', 'repository')
        action = data.pop('action', 'infos')
        ctx = Context(addon_id, action)
        response = ctx.run(data)
        print(json.dumps(response, indent=2))

    elif cmd == 'test':
        test_addons(*args[1:])

    else:
        raise ValueError('Usage: watched_sdk <www|call|test> [...]')
