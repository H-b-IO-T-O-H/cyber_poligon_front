import enum
import logging
import queue
import subprocess
import time
import typing
import uuid
import threading

logger = logging.getLogger('task_manager')
logger.setLevel(logging.INFO)
logging.basicConfig()


class TaskStatus(enum.Enum):
    Pending = 'pending'
    Running = 'running'
    Success = 'success'
    Canceled = 'canceled'
    Failed = 'failed'

    def __str__(self):
        return self.value


class Task:
    def __init__(self, user_id, executable):
        self.executable = executable
        self.user_id = user_id
        self.id = str(uuid.uuid4())
        self.status: TaskStatus = TaskStatus.Pending
        self.exception = ''
        self.log = ''
        self.create_ts = time.time()


class TaskManager:
    def __init__(self):
        self.incoming_queue = queue.Queue(maxsize=10)
        self.progress_pool = {}
        self.outgoing = {}
        self.max_parallel_workers = 1
        self.main_thread = threading.Thread(name="TaskManager", target=self.run)
        self.mu = threading.Lock()
        self.main_thread.start()

    def push_task(self, task: Task):
        with self.mu:
            if task.user_id not in self.progress_pool:
                self.progress_pool[task.user_id] = {task.id: task}
        self.incoming_queue.put(task)
        return task

    def get_user_task(self, user_id, task_id=None) -> typing.Optional[Task]:
        with self.mu:
            tasks = self.progress_pool.get(user_id, None)
        if tasks is None:
            return None
        if task_id is not None:
            return tasks.get(task_id)
        return None if len(tasks) == 0 else list(tasks.values())[0]

    def task_status(self, user_id, task_id) -> dict:
        task = self.get_user_task(user_id, task_id)
        resp = {"status": str(task.status) if task is not None else None,
                "exception": task.exception if task is not None else 'no task in pool'}
        return resp

    def run(self):
        task: Task = self.incoming_queue.get()
        self.mu.acquire()
        self.progress_pool[task.user_id][task.id].status = TaskStatus.Running
        self.mu.release()
        try:
            process = subprocess.Popen(task.executable, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            if error != b'':
                raise Exception(error.decode("utf-8"))
            if output != b'':
                log = output.decode("utf-8")
                self.mu.acquire()
                self.progress_pool[task.user_id][task.id].log = log
                logging.info(log)
                self.mu.release()
        except Exception as e:
            self.mu.acquire()
            self.progress_pool[task.user_id][task.id].status = TaskStatus.Failed
            self.progress_pool[task.user_id][task.id].exception = str(e)
            self.mu.release()
            return
        self.mu.acquire()
        self.progress_pool[task.user_id][task.id].status = TaskStatus.Success
        self.mu.release()
