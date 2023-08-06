import time
import requests
from watched_schema import validators
from .config import config


def _addons(ctx, **kwargs):
    addons = []
    # TODO: Make this async
    for addon in config.addons.values():
        addons.append(addon.infos(ctx, index=True, **kwargs))
    return addons


class Context(object):
    def __init__(self, addon_id, action):
        if addon_id == 'repository':
            addon_id = config.repository.id
        elif addon_id.startswith('.'):
            addon_id = config.repository.id + addon_id
        if addon_id not in config.addons:
            raise ValueError('Addon {} not found (called with action {})'.format(addon_id, action))
        addon = config.addons[addon_id]
        if action == 'infos':
            self.fn = lambda ctx, **kwargs: addon.infos(ctx, index=False, **kwargs)
        elif action == 'addons':
            if addon_id != config.repository.id:
                raise ValueError('Action addons is only allowed for this repository')
            self.fn = _addons
        elif action in ('directory', 'metadata', 'source', 'subtitle', 'resolve'):
            self.fn = getattr(addon, action)
        else:
            raise ValueError('Unknown action '+action)

        self.schema = validators['actions'][action]

    def run(self, request):
        self.schema['request'](request)
        response = self.fn(self, **request)
        self.schema['response'](response)
        return response

    def fetch(self, url, method="GET", **kwargs):
        return requests.request(method, url, **kwargs)

    def fetch_remote(self, *args, **kwargs):
        return self.fetch(*args, **kwargs)
