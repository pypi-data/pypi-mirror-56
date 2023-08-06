import json
import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
import enum
import importlib

import stream
from sqlalchemy import (JSON, Column, DateTime, ForeignKey, Index, String,
                        Table, text, Enum)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship

from .config import Config
from .package_manager import package_manager
from .proto import minetorch_pb2
from .utils import dict_merge, make_tarfile, update_json_file, human_readable_size


def _declarative_constructor(self, _session=None, **kwargs):
    self._session = _session
    cls_ = type(self)
    for k in kwargs:
        if not hasattr(cls_, k):
            raise TypeError(
                "%r is an invalid keyword argument for %s" % (k, cls_.__name__)
            )
        setattr(self, k, kwargs[k])


BaseORM = declarative_base(constructor=_declarative_constructor)


class BaseModel():
    id = Column(UUID(as_uuid=True), server_default=text("uuid_generate_v4()"), primary_key=True, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def todict(self):
        result = {}
        for column in self.__table__.columns:
            if column.type.__class__.__name__ == 'DateTime':
                result[column.name] = getattr(self, column.name).strftime("%d/%m/%Y %H:%M:%S")
            elif column.type.__class__.__name__ == 'Enum':
                result[column.name] = getattr(self, column.name).value
            elif column.type.__class__.__name__ == 'UUID':
                result[column.name] = str(getattr(self, column.name))
            else:
                result[column.name] = getattr(self, column.name)
        return result


class Experiment(BaseModel, BaseORM):
    __tablename__ = 'experiments'

    name = Column(String)
    enabled_packages = Column(JSON)
    executions = relationship('Execution', backref='experiment', cascade="all, delete-orphan")
    modules = relationship('Module', backref='experiment', cascade="all, delete-orphan")

    def prepare_directories(self):
        try:
            os.makedirs(self.dir())
        except FileExistsError:
            pass

    def dir(self):
        return Path() / '.featurize_experiments' / str(self.id)

    def update_config(self, config):
        one_versoin = (self._session.query(Version)
                           .filter(Version.experiment_id == self.id)
                           .filter(Version.version == Version.DRAFT)
                           .scalar())

        if one_versoin:
            one_versoin.version = config['version']
            one_versoin.server_addr = config['server_addr']
            one_versoin.enabled_package = config['enabled_package']
            one_versoin.components = config['components']
        else:
            one_versoin = Version(
                version=config['version'],
                server_addr=config['server_addr'],
                enabled_package=config['enabled_package'],
                experiment_id=self.identity,
                components=config['components']
            )
            self._session.add(one_versoin)
        self._session.commit()
        return one_versoin.todict()

    def config_file(self, version):
        return self.experiment_dir / f'config.{str(version)}.json'

    def metadata_file(self):
        return self.experiment_dir / 'metadata.json'

    def runtime_config_file(self):
        return self.experiment_dir / 'runtime.config.json'

    def generate_runtime_config(self):
        """use metadata and current.config.json to generate a runtime.config.json
        file, which can be feed to featurize-runtime agent directly
        """
        runtime_config = self.get_metadata()
        config = self.get_config('current')
        dict_merge(runtime_config, config)
        update_json_file(self.runtime_config_file(), runtime_config)

    def commit_config(self):
        """Archived current version, publish draft version and create new draft
        version. Commit will also generate runtime config file
        """
        draft = self.config_file('draft')
        current = self.config_file('current')
        metadata = self.get_metadata()

        draft_config = self.get_config('draft')

        if os.path.isfile(current):
            # if has current, archived it
            current_config = self.get_config('current')
            shutil.move(current, self.config_file(current_config['version']))

        # make the draft version as the current
        shutil.copy(draft, current)

        # create a new draft version similar to the current,
        # except the version number should plus onek
        draft_config['version'] += 1
        self.update_config(draft_config)

        # update metadata
        metadata['total_versions'] += 1
        self.update_metadata(metadata)

    def update_metadata(self, metadata):
        update_json_file(self.metadata_file(), metadata)

    def get_metadata(self):
        one_experiment = (self._session.query(Experiment)
                              .filter(Experiment.id == self.id)
                              .scalar())
        return one_experiment.todict()

    def get_config(self, version):
        one_versoin = (self._session.query(Version)
                           .filter(Version.experiment_id == self.id)
                           .filter(Version.version==Version.DRAFT)
                           .scalar())
        return one_versoin.todict()

    def log_file(self):
        return self.experiment_dir / 'log.txt'

    def add_remark(self, remark):
        metadata = self.get_metadata()
        if 'remarks' not in metadata:
            metadata['remarks'] = []
        metadata['remarks'].insert(0, remark)
        self.update_metadata(metadata)



class Comment(BaseModel, BaseORM):
    __tablename__ = 'comments'

    content = Column(String)
    commentable_id = Column(UUID(as_uuid=True), unique=False, nullable=False)
    commentable_type = Column(String)

    def get_comment(self, commentable_id):
        comments = []
        for one_comment in self._session.query(Comment).filter(Comment.commentable_id == commentable_id).all():
            comments.append(one_comment.todict())
        self._session.commit()
        return comments

    def add_comment(self, commentable_id, comment_dict):
        comment = Comment(
            content=comment_dict['content'],
            commentable_type=comment_dict['commentable_type'],
            commentable_id=commentable_id
        )
        self._session.add(comment)
        self._session.commit()
        return comment

    def update_comment(self, comment_id, comment_dict):
        comment = self._session.query(Comment).filter(Comment.id == comment_id).scalar()
        comment.content = comment_dict['content']
        # comment.commentable_type = comment_dict['commentable_type']
        # comment.commentable_id = comment_dict['commentable_id']
        self._session.commit()
        return comment

    def delete_comment(self, comment_id):
        comment = self._session.query(Comment).filter(Comment.id == comment_id).scalar()
        self._session.delete(comment)
        self._session.commit()


Index('commentable_id_index', Comment.commentable_id)


execution_module_associations = Table(
    'execution_module_associations',
    BaseORM.metadata,
    Column('execution_id', UUID(as_uuid=True), ForeignKey('executions.id'), primary_key=True),
    Column('module_id', UUID(as_uuid=True), ForeignKey('modules.id'), primary_key=True)
)


class Execution(BaseModel, BaseORM):

    class Status(enum.Enum):
        running = 'running'
        idle = 'idle'
        error = 'error'
        not_running = 'not_running'
        booting = 'booting'
        starting = 'starting'
        stopping = 'stopping'
        killing = 'killing'

    __tablename__ = 'executions'

    status = Column(Enum(Status), default=Status.not_running)
    name = Column(String, default='Untitled Execution')
    task_type = Column(String)
    agent_config = Column(JSON)
    parameters = Column(MutableDict.as_mutable(JSON))
    experiment_id = Column(UUID(as_uuid=True), ForeignKey('experiments.id'), unique=False, nullable=False)
    modules = relationship("Module", back_populates="executions", secondary=execution_module_associations)

    def generate_config(self):
        config = {
            'identity': str(self.id),
            'task': self.task_type,
            'modules': {},
            'options': self.parameters,
            'agent_config': self.agent_config,
            'server_addr': f'{Config.server_addr}:{Config.rpc_port}',
            'enabled_package': package_manager.packages
        }
        for module in self.modules:
            config['modules'][module.key] = module.todict()
        with open(self.config_file(), 'w') as f:
            json.dump(config, f)

    def config_file(self):
        return self.dir() / 'config.json'

    def log_file(self):
        return self.dir() / 'log.txt'

    def files(self, file_type='files'):

        def get_file_info(name):
            nonlocal file_type
            state = os.stat(self.agent_file(name, file_type))
            return {
                'name': name,
                'created_at': datetime.utcfromtimestamp(state.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                'size': human_readable_size(state.st_size),
            }

        return list(map(get_file_info, os.listdir(self.dir() / file_type)))

    def delete_file(self, file_name, file_type):
        os.remove(self.dir() / file_type / file_name)

    def dir(self):
        return self.experiment.dir() / str(self.id)

    def prepare_directories(self):
        try:
            os.makedirs(self.dir())
            os.mkdir(self.dir() / 'files')
            os.mkdir(self.dir() / 'images')
            os.mkdir(self.dir() / 'checkpoints')
            os.mkdir(self.dir() / 'graphs')
            os.mkdir(self.dir() / 'inputs')
        except FileExistsError:
            pass

    def graph_file(self, graph_name):
        return self.dir() / 'graphs' / graph_name

    def agent_file(self, file_name, file_type='files'):
        return self.dir() / file_type / file_name

    def create_graph(self, graph_name):
        self.graph_file(graph_name).touch()

    def get_graphs(self):
        return os.listdir(self.dir() / 'graphs')

    def add_point(self, graph_name, point):
        graph_file = self.graph_file(graph_name)
        raw_point = minetorch_pb2.RawPoint()
        raw_point.x = point['x']
        raw_point.y = point['y']
        with open(graph_file, 'ab') as f:
            stream.dump(f, raw_point, gzip=False)

    def add_field_file(self, field_name, file_name, content):
        field_dir = self.agent_file(field_name, 'inputs')
        try:
            os.mkdir(field_dir)
        except FileExistsError:
            pass
        file_path = field_dir / file_name
        with open(file_path, 'wb') as f:
            f.write(content)
        return f'/featurize/static/{self.experiment_id}/{self.id}/inputs/{field_name}/{file_name}'

    def get_field_files(self, field_name):
        """The return values are highly bound to ant.design's uploader
        """
        field_dir = self.agent_file(field_name, 'inputs')
        try:
            os.mkdir(field_dir)
        except FileExistsError:
            pass

        def mapping(item):
            index, file_name = item
            return {
                'uid': index,
                'name': file_name,
                'status': 'done',
                'url': f'{Config.server_proto}{Config.server_addr}:{Config.server_port}/featurize/static/{self.experiment_id}/{self.id}/inputs/{field_name}/{file_name}'
            }
        return list(map(mapping, enumerate(os.listdir(self.agent_file(field_name, 'inputs')))))

    def docker_tarball(self):
        return self.dir() / 'docker.tar.gz'

    def create_docker_tarball(self):
        dirpath = Path(tempfile.mkdtemp())

        config_file = dirpath / 'config.json'
        docker_file = dirpath / 'Dockerfile'
        requirements_file = dirpath / 'requirements.txt'

        requirements = set()
        enabled_packages_command = []

        for package_name in package_manager.packages:
            module = importlib.import_module(package_name)
            requirements.add(module.PYPI_PACKAGE_NAME)
            enabled_packages_command.append(f'RUN featurize package:add {package_name}')

        with open(requirements_file, 'w') as f:
            content = "\n".join([
                'featurize-jupyterlab',
                *list(requirements)
            ])
            f.write(content)

        with open(docker_file, 'w') as f:
            content = "\n".join([
                'FROM python:3',
                'WORKDIR /runtime',
                'COPY . /runtime',
                'RUN pip3 install -r requirements.txt',
                *enabled_packages_command,
                'CMD featurize run --config config.json'
            ])
            f.write(content)

        shutil.copy(self.config_file(), config_file)
        make_tarfile(self.docker_tarball(), dirpath)
        return dirpath


Index('execution_experiment_id_index', Execution.experiment_id)


class Module(BaseModel, BaseORM):
    __tablename__ = "modules"

    name = Column(String)
    key = Column(String)
    config = Column(JSON)
    experiment_id = Column(UUID(as_uuid=True), ForeignKey('experiments.id'), unique=False, nullable=False)
    executions = relationship("Execution", back_populates="modules", secondary=execution_module_associations)


Index('module_experiment_id_index', Module.experiment_id)
