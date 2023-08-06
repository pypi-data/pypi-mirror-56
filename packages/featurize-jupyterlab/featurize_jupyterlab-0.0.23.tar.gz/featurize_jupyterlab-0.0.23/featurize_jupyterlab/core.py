import collections
import importlib
import os
import sys
import urllib
from abc import ABCMeta, abstractmethod
from inspect import isabstract

import torch

from .package_manager import package_manager
from .task import env


def load_default_modules():
    for package in package_manager.packages:
        importlib.import_module(package)


class Option:
    """Option is a field of a Optionable.

    An option represents a connection between a form field and an property of
    an attribute.

    Some attributes are only be used in the web and some are used for property.
    e.g. the `type` attribute is used for rendering the right web component while
    the `post_process` is used for post processing the value user has inputed in
    the code.
    """

    def __init__(self, name=None, type='string', required=True, default=None, post_process=None, **settings):
        self._name = name
        self.key = None
        self.default = default
        self.type = type
        self.post_process = post_process
        if self.type == 'hardcode':
            self.required = False
        else:
            self.required = required
        self.settings = settings

    @property
    def name(self):
        return self._name or self.key

    @name.setter
    def name(self, name):
        self._name = name

    def to_json_serializable(self):
        return {
            'key': self.key,
            'name': self.name,
            'settings': {
                'type': self.type,
                'required': self.required,
                'default': self.default,
                **self.settings,
            }
        }


class OptionableMeta(ABCMeta):
    """Meta class of Optionable
    """

    def __new__(cls, clsname, bases, context):
        options = []
        if len(bases) > 0:
            options += bases[0].options

        for key, value in context.items():
            if isinstance(value, Option):
                value.key = key
                options.append(value)
        context['options'] = options
        _cls = super().__new__(cls, clsname, bases, context)

        for option in filter(lambda o: o.type == 'uploader', _cls.options):
            def getter(self):
                urls = getattr(self, f'_{option.key}')
                return [f'./inputs/{option.key}/{url.split("/")[-1]}' for url in urls]

            def setter(self, urls):
                setattr(self, f'_{option.key}', urls)
                try:
                    os.makedirs(f'./inputs/{option.key}')
                except FileExistsError:
                    pass
                for url in urls:
                    filename = url.split('/')[-1]
                    urllib.request.urlretrieve(url, f'./inputs/{option.key}/{filename}')

            setattr(_cls, option.key, property(getter, setter))

        for option in filter(lambda o: o.type == 'checkpoint', _cls.options):
            def getter(self):
                checkpoint_name = getattr(self, f'_{option.key}')
                if checkpoint_name:
                    checkpoint_file = checkpoint_name.split('.', 1)[-1]
                    return f'./checkpoints/{checkpoint_file}'
                return None

            def setter(self, checkpoint_name):
                setattr(self, f'_{option.key}', checkpoint_name)
                if not checkpoint_name:
                    return
                try:
                    os.makedirs(f'./checkpoints/')
                except FileExistsError:
                    pass
                execution_id, checkpoint_file = checkpoint_name.split('.', 1)
                env.rpc.get_file(checkpoint_file, 'checkpoints', f'./checkpoints/{checkpoint_file}', execution_id)
            setattr(_cls, option.key, property(getter, setter))

        return _cls


class Optionable(metaclass=OptionableMeta):
    """Optionable is an object which can be configured by the web ui.

    In the web, Option is the field, Optionable is the form.
    In code, Optionable can make any classes be able to init by the web.

    Examples:
        # This is a normal class which defines a Car
        class Car:
            def __init__(self, color, is_used=True):
                self.color = color
                self.is_used = is_used

        # This is the same Car except it is Optionable
        class Car:
            color = Option(name='Color of this car', type='string', required=True)
            is_used = Option(name='Is this car used', type='boolean', default=True)

        # The following code works both for the 2 definations
        car = Car(color='red', is_used=False)
        print(car.color, car.is_used)
    """

    def __init__(self, user_settings, extra_parameters={}):
        for option in self.options:
            value = user_settings.get(option.key, option.default)
            if option.post_process:
                value = option.post_process(value)
            setattr(self, option.key, value)
        for key in extra_parameters:
            setattr(self, key, extra_parameters[key])
        self.initialize()

    def initialize(self):
        pass


class ComponentMeta(OptionableMeta):
    """Meta class for component
    """
    registed_components = []
    meta_mixin_props = ['namespace']

    def _get_mixin_dict(mixin):
        result_dict = {}
        for prop in ComponentMeta.meta_mixin_props:
            if not hasattr(mixin, prop):
                continue
            result_dict[prop] = getattr(mixin, prop, None)
        return result_dict

    def __new__(cls, clsname, bases, context):

        context['meta'] = ComponentMeta

        name = clsname
        description = context.get('__doc__', '').strip()
        component_type = None

        if len(bases) > 0:
            component_type = context.get('component_type', getattr(bases[0], 'component_type', None))

        for mixin in bases[1:]:
            context = {
                **context,
                **ComponentMeta._get_mixin_dict(mixin)
            }

        for key, value in context.items():
            if key == 'description':
                description = value
            if key == 'name':
                name = value

        context['name'] = name
        context['description'] = description
        context['component_type'] = component_type
        context['metadata'] = context.get('metadata', {})
        # TODO: namespace should be recorded to get
        # namespace conflicts
        if context.get('namespace', None) is not None:
            context['key'] = f'{context["namespace"]}/{clsname}'
        else:
            # TODO: warning
            context['key'] = f'{clsname}'

        klass = super().__new__(cls, clsname, bases, context)

        if not isabstract(klass):
            ComponentMeta.registed_components.append(klass)

        return klass

    @classmethod
    def __prepare__(cls, clsname, bases):
        return collections.OrderedDict()


class Component(Optionable, metaclass=ComponentMeta):
    """Component is a defination of function which can be created
    and configured by the web.

    Almost everything in featurize can be an component because that
    is what we do: migrating code to the web.

    Class which inherited from Component and implemented `__call__`
    method is a real component.

    A real comopnent should also announce its type by creating a class
    property named `component_type`. `component_type` is mostly used for
    grouping and validation.

    In most cases, many component classes will have the same `component_type`,
    so it's recommended to create a `component_type` second base class. And
    the real component class inherited from that. Just like the built in classes
    like `Dataset`, `Dataflow` do.
    """
    @classmethod
    def to_json_serializable(cls):
        return {
            'name': cls.name,
            'description': cls.description,
            'options': list(map(lambda o: o.to_json_serializable(), cls.options)),
            'metadata': cls.metadata,
            'type': cls.component_type,
            'key': cls.key
        }

    @abstractmethod
    def __call__(self):
        pass


class Model(Component):
    component_type = 'Model'
    checkpoint = Option(type='checkpoint', required=False)

    def __call__(self):
        model = self.create_model()
        if self.checkpoint:
            checkpoint = torch.load(self.checkpoint)
            model.load_state_dict(checkpoint['state_dict'])
        return model

    @abstractmethod
    def create_model(self):
        pass


class Dataflow(Component):
    component_type = 'Dataflow'


class Dataset(Component):
    component_type = 'Dataset'


class Optimizer(Component):
    model = Option(type='hardcode', help='The `Model` which should be already configured', required=False)
    component_type = 'Optimizer'


class Loss(Component):
    trainer = Option(type='hardcode', help='This is the `trainer` instance of `Minetorch`', required=False)
    component_type = 'Loss'


class Trainer(Component):
    component_type = 'Trainer'


class Metric(Component):
    component_type = 'Metric'
    prediction = Option(type='hardcode')
    truth = Option(type='hardcode')


class Module:
    """Module is a block of a task.

    A Module is a code block of a task which can be configured by the web.
    Task is a process that can require the user to provide some necessary module
    to make it run. Like training process could require a `train dataloader`
    module which is provided by the user.

    Module is composed by one or more `Components`. And `Component` can be added
    and configured in the web so that makes module can be configured in the web.
    """

    def __init__(self, component_types, key=None, name=None, required=True, multiple=False):
        self._name = name
        self.key = key
        self.component_types = component_types
        self.required = required
        self.multiple = multiple
        self.dependencies = []

    @property
    def name(self):
        return self._name or self.key

    @name.setter
    def name(self, name):
        self._name = name

    def to_json_serializable(self):
        return {
            'name': self.name,
            'key': self.key,
            'component_types': self.component_types,
            'required': self.required,
            'multiple': self.multiple
        }

    @abstractmethod
    def modulize(self):
        pass

    def init_component(self, component_config, extra_parameters={}):
        component_name = component_config['name']
        component_type = component_config['type']
        klass = next((klass for klass in registed_components() if klass.key == component_name), None)
        if klass is None:
            raise Exception(
                f"Could not found {component_type}: {component_name}, "
                f"be sure to add the coresponding package before use it"
            )
        return klass(component_config.get('parameters', {}), extra_parameters)

    def add_dependency(self, *modules):
        self.dependencies += modules


class Compose():

    def __init__(self, *transformations):
        self.transformations = list(transformations)

    def __call__(self, rowdata):
        for transformation in self.transformations:
            rowdata = transformation(rowdata)
        return rowdata

    def add(self, transformation):
        self.transformations.append(transformation)


class BasicModule(Module):

    def modulize(self, block_config, extra_parameters={}):
        components = list(map(lambda x: self.init_component(x, extra_parameters)(), block_config))
        if self.multiple:
            return components
        return components[0] if len(components) > 0 else None


class DataflowModule(Module):

    def modulize(self, block_config, extra_parameters={}):
        dataflow = Compose()
        for component_config in block_config:
            dataflow.add(self.init_component(component_config, extra_parameters))
        return dataflow


class TaskMeta(ComponentMeta):
    def __new__(cls, clsname, bases, context):
        modules = []
        if len(bases) > 0 and hasattr(bases[0], 'modules'):
            modules += bases[0].modules

        for key, value in context.items():
            if isinstance(value, Module):
                value.key = key
                modules.append(value)
        context['modules'] = modules
        _cls = super().__new__(cls, clsname, bases, context)
        return _cls


class Task(Component, metaclass=TaskMeta):
    component_type = 'Task'

    @classmethod
    def to_json_serializable(cls):
        return {
            **super().to_json_serializable(),
            'modules': list(map(lambda o: o.to_json_serializable(), cls.modules))
        }

    def init_module(self, module):
        """Make abstract modules of the task to be real modules
        """
        if module.key in self.initialized_module:
            return self.initialized_module[module.key]

        if module.key not in self.config['modules']:
            if module.required:
                raise Exception(f'Module {module.name} is required but not provided')
            setattr(self, module.key, None)
            return None

        extra_parameters = {}
        for dependency in module.dependencies:
            extra_parameters[dependency.key] = self.init_module(dependency)
        initialized_module = module.modulize(
            self.config['modules'][module.key]['config'],
            extra_parameters
        )

        self.initialized_module[module.key] = initialized_module
        setattr(self, module.key, initialized_module)

        return initialized_module

    def __init__(self, env):
        self.env = env
        self.config = self.env.config
        self.initialized_module = {}
        super().__init__(self.config.get('options', {}) or {})
        for module in self.modules:
            self.init_module(module)

    @abstractmethod
    def __call__(self):
        pass


def registed_components():
    return ComponentMeta.registed_components


def clear_registed_components():
    ComponentMeta.registed_components = []


def boot():
    sys.path.insert(0, os.getcwd())
    load_default_modules()
