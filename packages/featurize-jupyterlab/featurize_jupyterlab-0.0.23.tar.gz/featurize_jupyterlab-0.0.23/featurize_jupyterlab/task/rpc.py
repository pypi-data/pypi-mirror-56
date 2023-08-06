import grpc
from ..proto import minetorch_pb2_grpc
from ..proto import minetorch_pb2
from functools import wraps
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


def retry(number):
    def decorator(func):
        @wraps(func)
        def __decorator(*args, **kwargs):
            nonlocal number
            for _ in range(number - 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    continue
            return func(*args, **kwargs)
        return __decorator
    return decorator


def async_call(func):

    @wraps(func)
    def __decorator(self, *args, **kwargs):
        self.executor.submit(func, self, *args, **kwargs)
    return __decorator


class RuntimeRpc():
    """
    TODO: The very first RPC call after forking the child process will fail 100%,
    it will be ok for the second call by retry, not sure why but we can dump the
    network traffic to see what really happens.

    TODO: This should work when there is no network, all the rpc call should be
    persisted and queued in local disk. Maybe provide a @queue decorator.
    """
    def __init__(self, addr, identity):
        self.channel = grpc.insecure_channel(addr)
        self.stub = minetorch_pb2_grpc.MinetorchStub(self.channel)
        self.identity = identity
        self.point_cache = []
        self.log_cache = []
        self.executor = ThreadPoolExecutor()

    def finish(self, rpc, message, metadata=[]):
        return rpc(
            message,
            metadata=[
                ('identity', self.identity),
                *metadata
            ],
            wait_for_ready=True,
        )

    @retry(3)
    def create_graph(self, graph_name):
        message = minetorch_pb2.Graph(
            identity=self.identity,
            graph_name=graph_name,
        )
        return self.finish(self.stub.CreateGraph, message)

    @async_call
    def add_point(self, graph_name, x, y):
        self.point_cache.append(
            minetorch_pb2.Point(
                identity=self.identity,
                graph_name=graph_name,
                x=x,
                y=y
            )
        )
        if len(self.point_cache) > 100:
            self.finish(self.stub.AddPoint, iter(self.point_cache))
            self.point_cache = []

    def add_image(self, filepath):
        return self.add_file(filepath, 'images')

    def add_checkpoint(self, filepath):
        return self.add_file(filepath, 'checkpoints')

    @retry(3)
    def get_file(self, filepath, filetype, distpath, identity=None):
        filepath = minetorch_pb2.File(filename=filepath, filetype=filetype)
        with open(distpath, 'wb') as f:
            binaries = self.stub.GetBinary(filepath, metadata=[('identity', identity or self.identity)])
            for response in binaries:
                f.write(response.bin)

    # @async_call
    def add_file(self, filepath, filetype='files'):
        filepath = Path(filepath)

        def generator():
            with open(filepath, 'rb') as f:
                while True:
                    _bytes = f.read(1024 * 1024)
                    yield minetorch_pb2.Binary(bin=_bytes)
                    if len(_bytes) < 1024 * 1024:
                        break
        return self.finish(
            self.stub.SendBinary,
            generator(),
            [('filename', filepath.name), ('filetype', filetype)],
        )

    @retry(3)
    def hey_yo(self, status):
        message = minetorch_pb2.HeyMessage(
            # TODO: we can get ip from server, don't need this
            ip_addr='client ip addr',
            status=status,
            identity=self.identity
        )
        return self.finish(self.stub.HeyYo, message)

    @retry(3)
    @async_call
    def log(self, record):
        self.log_cache.append(minetorch_pb2.Log(
            identity=self.identity,
            log=record.msg,
            level=record.levelname
        ))
        if len(self.log_cache) > 100:
            self.finish(self.stub.SendLog, iter(self.log_cache))
            self.log_cache = []
