from ..core import registed_components, boot


def _find_component_by_name(component_key):
    return next((klass for klass in registed_components() if klass.key == component_key), None)


def main(env):
    boot()
    task_klass = _find_component_by_name(env.config['task'])
    task = task_klass(env)
    task()
