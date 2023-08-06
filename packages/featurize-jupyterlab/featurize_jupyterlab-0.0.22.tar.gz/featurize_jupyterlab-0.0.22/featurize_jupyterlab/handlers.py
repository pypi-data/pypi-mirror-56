import json
import humps
import torch
import tornado
import os
import pandas as pd

import stream
from notebook.base.handlers import APIHandler, web
from notebook.utils import url_path_join as ujoin

from sqlalchemy.orm import sessionmaker

from . import core
from .models import Experiment, Execution, Module, Comment
from .package_manager import PackageManager
from .proto import minetorch_pb2
from .config import Config


class FeaturizeHandler(APIHandler):

    def finish(self, data={}):
        wrapped_data = {
            'status': 'success',
            'data': data,
        }
        self.session.commit()
        return super().finish(json.dumps(humps.camelize(wrapped_data)))

    def prepare(self):
        self.experiment = None
        self.comment = None
        self.post_data = None
        self.session = sessionmaker(bind=Config.engine)()

        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

        if (self.request.method == 'POST' or self.request.method == 'PUT') and self.request.headers['Content-Type'] == 'application/json':
            self.post_data = humps.decamelize(json.loads(self.request.body))
            identity = self.post_data.get('identity', self.path_kwargs.get('identity', None))
        else:
            identity = self.get_argument('identity', self.path_kwargs.get('identity', None))

        if 'experiments' in self.request.uri:
            if identity is not None:
                self.experiment = self.session.query(Experiment).get(identity)

        if 'comments' or 'comment' in self.request.uri:
            self.comment = Comment(_session=self.session)


class DockerfileHandler(web.RequestHandler):

    def get(self):
        identity = self.get_argument('identity', None)
        if identity is None:
            self.set_status(400)
            self.finish()
            return
        experiment = Experiment(identity)

        self.set_header("Content-Disposition", "attachment; filename=docker.tar.gz")
        with open(experiment.docker_file(), 'rb') as f:
            while 1:
                data = f.read(16384)  # or some other nice-sized chunk
                if not data:
                    break
                self.write(data)
        self.finish()


class ExperimentsHandler(FeaturizeHandler):

    def post(self):
        package = PackageManager()
        experiment = Experiment(
            name=self.post_data['name'],
            enabled_packages=','.join(package.packages)
        )

        self.session.add(experiment)
        self.session.flush()
        experiment.prepare_directories()
        self.finish()

    def get(self):
        experiments = []
        for one_experiment in self.session.query(Experiment).all():
            experiments.append(one_experiment.todict())
        self.finish(experiments)


class ExperimentHandler(FeaturizeHandler):

    def get(self, identity):
        self.finish(self.experiment.todict())

    def put(self, identity):
        for key, value in self.post_data.items():
            setattr(self.experiment, key, value)
        self.finish()

    def delete(self, identity):
        self.session.delete(self.experiment)
        self.finish()


class ComponentsHandler(FeaturizeHandler):

    def get(self, identity):
        components = core.registed_components()
        data = list(map(lambda m: m.to_json_serializable(), components))
        self.finish(data)


class ConfigHandler(FeaturizeHandler):

    def get(self):
        one_version_dict = self.experiment.get_config('draft')
        self.finish(one_version_dict)

    def post(self):
        data = json.loads(self.request.body)
        version_post_dict = self.experiment.update_config(data['config'])
        self.finish(version_post_dict)


class ExperimentStatusHandler(FeaturizeHandler):

    def post(self):
        self.experiment.update_metadata({
            'status': self.post_data['status']
        })


class GraphsHandler(FeaturizeHandler):

    def prepare(self):
        super().prepare()
        execution_id = self.path_kwargs.get('execution_identity')
        self.execution = self.session.query(Execution).get(execution_id)

    def get(self, execution_identity):
        self.finish(self.execution.get_graphs())


class GraphHandler(FeaturizeHandler):

    def prepare(self):
        super().prepare()
        execution_id = self.path_kwargs.get('execution_identity')
        self.execution = self.session.query(Execution).get(execution_id)

    def get(self, execution_identity):
        graph_name = self.get_argument('graph_name', None)
        start_at = int(self.get_argument('start_at', 0))

        with open(self.execution.graph_file(graph_name), 'rb') as f:
            f.seek(start_at)
            points = [a for a in stream.parse(f, minetorch_pb2.Point)]
            points = list(map(lambda p: {'x': p.x, 'y': p.y}, points))
            self.finish({
                'position': f.tell(),
                'points': points,
            })


class LogHandler(FeaturizeHandler):

    def get(self):
        offset = int(self.get_argument('offset', 0))
        limit = int(self.get_argument('limit', 1000))

        with open(self.experiment.log_file(), 'r') as f:
            f.seek(offset)
            content = f.read(limit)
            while True:
                char = f.read(1)
                if char and char != "\n":
                    content += char
                else:
                    break
            self.finish({
                'read_up_to': f.tell(),
                'logs': content,
            })


class RemarkHandler(FeaturizeHandler):

    def post(self):
        self.experiment.add_remark(self.post_data['remark'])
        self.finish()


class ExecutionsHandler(FeaturizeHandler):

    def post(self, identity):
        execution = Execution(
            name=self.post_data['name'],
            status=Execution.Status.not_running,
            task_type=self.post_data['task_type'],
            agent_config=self.post_data['agent_config'],
            experiment_id=self.experiment.id
        )
        self.session.add(execution)
        self.session.flush()
        execution.prepare_directories()
        self.finish()

    def get(self, identity):
        self.finish(list(map(lambda x: x.todict(), self.experiment.executions)))


class ExecutionHandler(FeaturizeHandler):

    def prepare(self):
        super().prepare()
        execution_id = self.path_kwargs.get('execution_identity')
        self.execution = self.session.query(Execution).get(execution_id)

    def get(self, execution_identity):
        self.finish({
            **self.execution.todict(),
            'graphs': self.execution.get_graphs(),
            'modules': list(map(lambda x: x.todict(), self.execution.modules))
        })

    def put(self, execution_identity):
        for key, value in self.post_data.items():
            setattr(self.execution, key, value)
        self.finish()

    def delete(self, execution_identity):
        self.session.delete(self.execution)
        self.finish()


class ModulesHandler(FeaturizeHandler):

    def get(self, identity):
        self.finish(list(map(lambda x: x.todict(), self.experiment.modules)))
        # modules = []
        # for one_module in self.session.query(Module).filter(Module.experiment_id == self.experiment.id).all():
        #     modules.append(one_module.todict())
        # self.finish(modules)

    def post(self, identity):
        module = Module(
            name=self.post_data['name'],
            config=self.post_data['config'],
            experiment_id=self.experiment.id
        )
        self.session.add(module)
        self.finish()


class ExecutionModulesHandler(FeaturizeHandler):

    def prepare(self):
        super().prepare()
        execution_id = self.path_kwargs.get('execution_identity')
        self.execution = self.session.query(Execution).get(execution_id)

    def get(self, execution_identity):
        self.finish(list(map(lambda x: x.todict(), self.execution.modules)))

    def post(self, execution_identity):
        module = Module(
            key=self.post_data['key'],
            config=self.post_data['config'],
            experiment_id=self.execution.experiment_id
        )
        self.execution.modules.append(module)
        self.session.commit()


class ModuleHandler(FeaturizeHandler):

    def prepare(self):
        super().prepare()
        module_identity = self.path_kwargs.get('module_identity')
        self.module = self.session.query(Module).get(module_identity)

    def put(self, module_identity):
        for key, value in self.post_data.items():
            setattr(self.module, key, value)
        self.finish()

    def delete(self, module_identity):
        self.session.delete(self.module)
        self.finish()


class CommentsHandler(FeaturizeHandler):

    def get(self, commentable_identity):
        commentable_identity = self.get_argument('commentable_identity', self.path_kwargs.get('commentable_identity', None))
        comments = self.comment.get_comment(commentable_identity)
        self.finish(comments)

    def post(self, commentable_identity):
        commentable_identity = self.get_argument('commentable_identity', self.path_kwargs.get('commentable_identity', None))
        self.comment.add_comment(commentable_identity, self.post_data)
        self.finish()


class CommentHandler(FeaturizeHandler):

    def put(self, comment_identity):
        comment_identity = self.get_argument('comment_identity', self.path_kwargs.get('comment_identity', None))
        self.comment.update_comment(comment_identity, self.post_data)
        self.finish()

    def delete(self, comment_identity):
        comment_identity = self.get_argument('comment_identity', self.path_kwargs.get('comment_identity', None))
        self.comment.delete_comment(comment_identity)
        self.finish()


class CommitmentHandler(FeaturizeHandler):

    def post(self, execution_identity):
        execution = self.session.query(Execution).get(execution_identity)
        for key, value in self.post_data.items():
            setattr(execution, key, value)
        execution.generate_config()
        execution.create_docker_tarball()
        self.finish()


class DownloadExecutionFileHandler(FeaturizeHandler):

    def prepare(self):
        super().prepare()
        execution_id = self.path_kwargs.get('execution_identity')
        self.execution = self.session.query(Execution).get(execution_id)

    def get(self, execution_identity):
        file_name = self.get_argument('file_name')
        self.set_header("Content-Disposition", f"attachment; filename={file_name}")
        with open(self.execution.agent_file(file_name), 'rb') as f:
            while 1:
                data = f.read(16384)
                if not data:
                    break
                self.write(data)
        self.finish()


class ExecutionFilesHandler(FeaturizeHandler):

    def prepare(self):
        super().prepare()
        execution_id = self.path_kwargs.get('execution_identity')
        self.execution = self.session.query(Execution).get(execution_id)

    def get(self, execution_identity, file_type='files'):
        file_name = self.get_argument('file_name', None)
        if file_name is None:
            self.finish(self.execution.files(file_type))
        else:
            ext = file_name.split('.')[-1]
            file = self.execution.agent_file(file_name, file_type)
            self.finish(getattr(self, f'_process_{ext}_file')(file))

    def _process_csv_file(self, file):
        df = pd.read_csv(file)
        columns = list(df.columns)
        rows = []
        for index, row in df.iterrows():
            rows.append(list(row))
        return ({
            'columns': columns,
            'rows': rows
        })

    def _process_tar_file(self, file):
        checkpoint = torch.load(file)
        return {
            'name': file.split('/')[-1],
            'epoch': checkpoint['epoch'],
            'train_iteration': checkpoint['train_iteration'],
            'val_iteration': checkpoint['val_iteration'],
        }

    def delete(self, execution_identity, file_type):
        self.execution.delete_file(self.get_argument('file_name'))
        self.finish()


class ExecutionFileUploadHandler(FeaturizeHandler):

    def prepare(self):
        super().prepare()
        execution_id = self.path_kwargs.get('execution_identity')
        self.execution = self.session.query(Execution).get(execution_id)

    def post(self, execution_identity):
        field_name = list(self.request.files.keys())[0]
        file_name = self.request.files[field_name][0]['filename']
        content = self.request.files[field_name][0]['body']
        self.execution.add_field_file(field_name, file_name, content)
        self.finish(self.execution.get_field_files(field_name))

    def get(self, execution_identity):
        field_name = self.get_argument('field')
        self.finish(self.execution.get_field_files(field_name))

    def delete(self, execution_identity):
        field_name = self.get_argument('fieldname')
        file_name = self.get_argument('filename')
        os.remove(self.execution.agent_file(f'{field_name}/{file_name}', 'inputs'))
        self.finish(self.execution.get_field_files(field_name))


class StaticHandler(tornado.web.StaticFileHandler):

    def initialize(self):
        super().initialize('./.featurize_experiments')


class ExperimentCheckpointHandler(FeaturizeHandler):

    def get(self, identity):
        experiment_id = self.path_kwargs.get('identity')
        self.experiment = self.session.query(Experiment).get(experiment_id)
        result = {}
        for execution in self.experiment.executions:
            checkpoints = execution.files('checkpoints')
            if len(checkpoints) == 0:
                next
            checkpoints = list(map(lambda c: {**c, 'execution_id': str(execution.id)}, checkpoints))
            result[execution.name] = checkpoints
        self.finish(result)


def setup_handlers(npapp):
    featurize_handlers = [
        (r"/featurize/experiments/(?P<identity>[\w\d\-]+)/components", ComponentsHandler),
        ("/featurize/config", ConfigHandler),
        ("/featurize/experiments/status", ExperimentStatusHandler),
        ("/featurize/experiments/log", LogHandler),
        ("/featurize/experiments/remark", RemarkHandler),
        ("/featurize/experiments/dockerfile", DockerfileHandler),
        ("/featurize/experiments", ExperimentsHandler),
        (r"/featurize/experiments/(?P<identity>[\w\d\-]+)", ExperimentHandler),
        (r"/featurize/experiments/(?P<identity>[\w\d\-]+)/executions", ExecutionsHandler),
        (r"/featurize/experiments/(?P<identity>[\w\d\-]+)/modules", ModulesHandler),
        (r"/featurize/experiments/(?P<identity>[\w\d\-]+)/checkpoints", ExperimentCheckpointHandler),
        (r"/featurize/experiments/modules/(?P<module_identity>[\w\d\-]+)", ModuleHandler),

        (r"/featurize/experiments/executions/(?P<execution_identity>[\w\d\-]+)", ExecutionHandler),
        (r"/featurize/executions/(?P<execution_identity>[\w\d\-]+)/modules", ExecutionModulesHandler),
        (r"/featurize/executions/(?P<execution_identity>[\w\d\-]+)/graphs", GraphsHandler),
        (r"/featurize/executions/(?P<execution_identity>[\w\d\-]+)/graph", GraphHandler),
        (r"/featurize/executions/(?P<execution_identity>[\w\d\-]+)/commitment", CommitmentHandler),
        (r"/featurize/executions/(?P<execution_identity>[\w\d-]+)/upload", ExecutionFileUploadHandler),
        (r"/featurize/executions/(?P<execution_identity>[\w\d-]+)/(?P<file_type>[\w\d-]+)/download", DownloadExecutionFileHandler),
        (r"/featurize/executions/(?P<execution_identity>[\w\d-]+)/(?P<file_type>[\w\d-]+)", ExecutionFilesHandler),

        (r"/featurize/comments/(?P<commentable_identity>[\w\d-]+)", CommentsHandler),
        (r"/featurize/comment/(?P<comment_identity>[\w\d-]+)", CommentHandler),
        (r"/featurize/static/(.*)", StaticHandler),
    ]

    # add the baseurl to our paths
    base_url = npapp.web_app.settings["base_url"]
    featurize_handlers = [(ujoin(base_url, x[0]), x[1]) for x in featurize_handlers]
    npapp.web_app.add_handlers(".*", featurize_handlers)
