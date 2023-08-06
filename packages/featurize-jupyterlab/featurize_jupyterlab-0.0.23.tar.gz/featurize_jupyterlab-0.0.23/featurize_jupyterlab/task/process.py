import sys
import time
from multiprocessing import Process

from .. import constants as C
from . import env

# current_status = C.STATUS_IDLE
current_status = C.STATUS_RUNNING
training_process = None


def main_process(config_file):
    global current_status, training_process
    env.init_process_env(config_file)
    env.logger.info('runtime main process has started')
    hey_yo_interval = env.config.get('hey_yo_interval', 3)
    try:
        while True:
            res = env.rpc.hey_yo(current_status)
            # if res.command == C.COMMAND_RUN and current_status != C.STATUS_RUNNING:
            #     env.logger.info('start training process')
            #     current_status = C.STATUS_RUNNING
            #     training_process = spawn_task_process(config_file)
            # elif res.command == C.COMMAND_HALT and current_status != C.STATUS_IDLE:
            #     env.logger.info('terminating training process')
            #     current_status = C.STATUS_IDLE
            #     training_process.terminate()
            #     training_process.join()
            #     env.logger.info('training process has been terminated')
            # elif res.command == C.COMMAND_KILL:
            #     env.logger.info('main process has been killed')
            #     break

            # ignore idle status
            if (res.command == C.COMMAND_KILL or res.command == C.COMMAND_HALT) and training_process is not None:
                training_process.terminate()
                training_process.join()
                env.logger.info('task process has been terminated')
                break
            elif training_process is None:
                current_status = C.STATUS_RUNNING
                training_process = spawn_task_process(config_file)
            elif training_process.exitcode is not None:
                env.logger.info('task process has existed')
                break
            time.sleep(hey_yo_interval)
        current_status = C.STATUS_NOT_RUNNING
        env.rpc.hey_yo(current_status)
    except Exception as e:
        env.logger.exception(f'unexpected error in main process: {e}')
    sys.exit(0)


def task_process_entry(config_file):
    from .task_process import main as task_process_main
    from . import env

    env.init_process_env(config_file)
    task_process_main(env)
    env.rpc.executor.shutdown()


def spawn_task_process(config_file):
    child_process = Process(target=task_process_entry, args=(config_file,))
    child_process.start()
    return child_process
