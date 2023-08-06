import importlib

__all__ = [
    'args',
    'main',
    'log',
]

for module in __all__:
    importlib.import_module('.%s' % module, 'gitlabevents')

