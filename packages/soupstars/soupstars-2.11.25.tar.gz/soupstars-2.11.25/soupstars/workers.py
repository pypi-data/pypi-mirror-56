"""
Worker
======

A thread-based worker for crawling web pages. It pulls URLs to parse from
a queue, and places finished results into a list accessible by multiple
workers.
"""

import logging
from threading import Thread, Lock

from soupstars.queues import EmptyQueueError, MaxResultsExceededError
from soupstars.loggers import Logger
from soupstars.loaders import Loader


class WorkerStates():
    WAITING = "WAITING"
    STOPPED = "STOPPED"
    RUNNING = "RUNNING"
    READY = "READY"
    STATES = [WAITING, STOPPED, RUNNING, READY]


class Worker(WorkerStates, Thread):
    """
    :param queue: a Soup Stars queue, which only allows putting an item once
    :type queue: class:`soupstars.queue.Queue`
    :param results: a results queue
    :type results: class:`list`
    """

    states = WorkerStates

    @classmethod
    def start_all(kls, num, *args, **kwargs):
        """
        Create and start `num` workers. Arguments are passed to the worker's
        __init__ function.
        """

        workers = [kls(id=id, *args, **kwargs) for id in range(1, num+1)]
        for worker in workers:
            worker.start()
        return workers

    @classmethod
    def stop_all(kls, workers):
        for worker in workers:
            worker.stop()
        for worker in workers:
            worker.join()
        return workers

    @classmethod
    def all_waiting(kls, workers):
        return all([w.state == w.WAITING for w in workers])

    @classmethod
    def all_stopped(kls, workers):
        return all([w.state == w.STOPPED for w in workers])

    def __str__(self):
        return f"<{self.__class__.__name__} {self.id}>"

    def start(self):
        """
        Starts the worker, running until `stop` is called.
        """
        self.state = self.set_state(self.RUNNING)
        self.logger.okay(f"Starting")
        super().start()

    def set_state(self, state):
        if state not in self.STATES:
            raise AttributeError(f"Can not change state to {state}, must be \
                                   one of {self.STATES}")
        self.lock.acquire()
        if self.state == self.STOPPED:
            pass
        else:
            self.state = state
        self.lock.release()
        return self.state

    def stop(self):
        """
        Stops the worker from running after it has finished any work
        currently in process.
        """

        self.logger.okay("Got signal to stop")
        self.set_state(self.STOPPED)


class LinksWorker(Worker):
    """
    Processes a `links` queue
    """

    def __init__(self, id, links_queue, results_queue, parser):
        self.lock = Lock()
        self.id = id
        self.links_queue = links_queue
        self.results_queue = results_queue
        self.parser = parser
        self.state = self.READY
        self.logger = logging.getLogger(str(self))
        self.logger.setLevel(15)
        self.loader = Loader()
        super().__init__()

    def run(self):
        self.links_queue.put_all(self.parser.seeds(), ignore_duplicates=True)
        while not self.state == self.STOPPED:
            if self.results_queue.full():
                self.set_state(self.WAITING)
                continue
            try:
                url = self.links_queue.get(timeout=0.1)
                self.set_state(self.RUNNING)
            except EmptyQueueError:
                self.set_state(self.WAITING)
                continue

            try:
                response = self.loader.load(url)
                data, links = self.parser.parse(response)
                if data:
                    try:
                        self.results_queue.put(data)
                    except MaxResultsExceededError:
                        continue
                self.links_queue.put_all(links, ignore_duplicates=True)
                self.logger.okay(f"Processed {url}")
            except Exception as err:
                self.logger.fail(f"Failed processing {url}: {err}")
            finally:
                self.links_queue.task_done()
        else:
            self.logger.okay(f"Stopped")


class ResultsWorker(Worker):
    """
    Processes the `results` queue
    """

    def __init__(self, id, writer, results_queue):
        self.lock = Lock()
        self.id = id
        self.state = self.READY
        self.logger = logging.getLogger(str(self))
        self.logger.setLevel(15)
        self.writer = writer
        self.results_queue = results_queue
        super().__init__()

    def run(self):
        while not self.state == self.STOPPED:
            try:
                result = self.results_queue.get(timeout=0.1)
                self.set_state(self.RUNNING)
            except EmptyQueueError:
                self.set_state(self.WAITING)
                continue
            try:
                self.writer.write(result)
                self.logger.okay(f"Processed {result['url']}")
            except Exception as err:
                self.logger.fail(f"Failed writing {result['url']}: {err}")
                raise err
            finally:
                self.results_queue.task_done()
        else:
            self.logger.okay(f"Stopped")
