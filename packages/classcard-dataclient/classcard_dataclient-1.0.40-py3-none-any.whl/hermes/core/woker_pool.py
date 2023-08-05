import threading
from redis.exceptions import ConnectionError
from utils.redis_utils import RedisQueue
from business.profession.processor import ProfessionProcessor
from config import THREAD_NUM, NICE_PROJECT


class MessageThreadPool(object):
    def __init__(self, project, thread_num):
        self.project = project
        self.threads = []
        # self.task_queue = RedisQueue(project)
        self.running = 0
        self.thread_num = thread_num
        self._init_pool()

    @property
    def task_queue(self):
        return RedisQueue(self.project)

    def _init_pool(self):
        for _ in range(self.thread_num):
            self.threads.append(MessageWorker(self))

    def start_task(self):
        for item in self.threads:
            item.start()

    def increase_running(self):
        self.running += 1

    def decrease_running(self):
        self.running -= 1

    def add_task(self, content):
        self.task_queue.put(content)

    def get_task(self):
        content = self.task_queue.get()
        return content


class MessageWorker(threading.Thread):
    def __init__(self, thread_pool):
        super(MessageWorker, self).__init__()
        self.thread_pool = thread_pool
        self.processors = {NICE_PROJECT: ProfessionProcessor}

    def run(self):
        while True:
            try:
                content = self.thread_pool.get_task()
                self.thread_pool.increase_running()
                print("get task {}".format(content))
                processor = self.processors.get(self.thread_pool.project, None)
                if processor:
                    processor.distribute(content['topic'], content['payload'])
            except (ConnectionError,):
                pass
            except (Exception,) as e:
                import traceback
                print(traceback.print_exc())
            finally:
                self.thread_pool.decrease_running()


profession_message_pool = MessageThreadPool(NICE_PROJECT, THREAD_NUM)
MESSAGE_POOLS = {NICE_PROJECT: profession_message_pool}
