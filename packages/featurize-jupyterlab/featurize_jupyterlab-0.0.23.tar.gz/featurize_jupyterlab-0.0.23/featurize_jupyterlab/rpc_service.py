from . import constants as C
from .logger import get_runtime_logger

from .proto import minetorch_pb2, minetorch_pb2_grpc
from .models import Execution
from sqlalchemy.orm import sessionmaker
from .config import Config
from functools import wraps


def with_session(func):
    @wraps(func)
    def __decorator(self, *args, **kwargs):
        self.session = self.make_session()
        result = func(self, *args, **kwargs)
        self.session.commit()
        return result

    return __decorator


class MinetorchServicer(minetorch_pb2_grpc.MinetorchServicer):

    def __init__(self):
        self.make_session = sessionmaker(bind=Config.engine)

    # TODO: performance of rpc server
    caches = {}

    def _get_execution(self, identity):
        return self.session.query(Execution).get(identity)

    @with_session
    def CreateGraph(self, request, context):
        # TODO: duplicate checking
        execution = self._get_execution(request.identity)
        execution.create_graph(request.graph_name)
        return minetorch_pb2.StandardResponse(
            status=0,
            message='ok'
        )

    @with_session
    def GetBinary(self, request, context):
        identity = None
        # TODO: refacotr this, add get_metadata method
        for key, value in context.invocation_metadata():
            if key == 'identity':
                identity = value
        execution = self._get_execution(identity)
        with open(execution.agent_file(request.filename, request.filetype), 'rb') as f:
            while True:
                _bytes = f.read(1024 * 1024)
                yield minetorch_pb2.Binary(bin=_bytes)
                if len(_bytes) < 1024 * 1024:
                    break

    @with_session
    def SendBinary(self, request_iterator, context):
        identity = None
        filename = None
        filetype = None
        # TODO: refacotr this, add get_metadata method
        for key, value in context.invocation_metadata():
            if key == 'filename':
                filename = value
            elif key == 'identity':
                identity = value
            elif key == 'filetype':
                filetype = value
        execution = self._get_execution(identity)
        agent_file = execution.agent_file(filename, filetype)
        agent_file.touch()
        with open(agent_file, 'wb') as f:
            for request in request_iterator:
                f.write(request.bin)
        return minetorch_pb2.StandardResponse(
            status=0,
            message='ok'
        )

    @with_session
    def AddPoint(self, request_iterator, context):
        # TODO: performance
        identity = None
        for key, value in context.invocation_metadata():
            if key == 'identity':
                identity = value
        execution = self._get_execution(identity)
        for request in request_iterator:
            execution.add_point(request.graph_name, {'x': request.x, 'y': request.y})
        return minetorch_pb2.StandardResponse(
            status=0,
            message='ok'
        )

    @with_session
    def SendLog(self, request_iterator, context):
        # TODO: performance
        # TODO: refacotr this, add get_metadata method
        identity = None
        for key, value in context.invocation_metadata():
            if key == 'identity':
                identity = value
        logger = get_runtime_logger(identity, self.session)
        for request in request_iterator:
            getattr(logger, request.level.lower())(request.log)
        return minetorch_pb2.StandardResponse(
            status=0,
            message='ok'
        )

    @with_session
    def HeyYo(self, request, context):
        execution = self._get_execution(request.identity)
        agent_status = request.status
        server_status = getattr(C, f"status_{execution.status.value}".upper())

        # Priority of status: Server Verb status > agent_status > server_status
        if server_status == C.STATUS_STARTING and agent_status == C.STATUS_IDLE:
            command = C.COMMAND_RUN
        elif server_status == C.STATUS_STOPPING and agent_status == C.STATUS_RUNNING:
            command = C.COMMAND_HALT
        # elif server_status == C.STATUS_KILLING and agent_status == C.STATUS_IDLE:
        elif server_status == C.STATUS_KILLING and (agent_status == C.STATUS_IDLE or agent_status == C.STATUS_RUNNING):
            command = C.COMMAND_KILL
        else:
            execution.status = getattr(Execution.Status, minetorch_pb2.HeyMessage.Status.Name(agent_status).lower()).value
            self.session.commit()
            command = C.COMMAND_NONE
        return minetorch_pb2.YoMessage(
            roger=True,
            command=command
        )
