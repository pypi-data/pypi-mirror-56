"""
Runner
======

The runner is responsible for executing the parser module built by a user.

It can be configured in a number of ways:
- select the number of threaded workers, so that multiple requests can be made concurrently and the results of those requests processed in parallel.
- only process a select number of pages.
- write results to various locations and formats
"""

import logging
import importlib
import time
import datetime as dt
from types import ModuleType

from soupstars.queues import LinksQueue, ResultsQueue
from soupstars.workers import LinksWorker, ResultsWorker
from soupstars.loggers import Logger
from soupstars.parsers import Parser
from soupstars.writers import JsonWriter, Writer


class Runner(object):

    default_max_duration = dt.timedelta(minutes=10)

    def __init__(self, parser, writer='csv', writer_url=None,
                 num_link_workers=4, num_results_workers=1, max_results=0,
                 max_duration=None):
        self.created_at = dt.datetime.now()
        self.started_at = None
        self.finished_at = None
        self.max_results = max_results
        self.max_duration = max_duration or self.default_max_duration
        self.parser = Parser.from_string(parser)
        self.writer = Writer.from_string(writer)
        self.writer.url = writer_url or self.default_writer_url()
        self.results = ResultsQueue(max_results=self.max_results)
        self.queue = LinksQueue()
        self.logger = logging.getLogger(str(self))
        self.logger.setLevel(15)
        self.link_workers = []
        self.result_workers = []
        self.num_link_workers = num_link_workers
        self.num_results_workers = num_results_workers

    def __str__(self):
        return f"<Runner {self.parser.module.__name__}>"

    def default_writer_url(self):
        return f"{self.parser.module.__name__}-run-{self.created_at}"

    def all_waiting(self):
        return ResultsWorker.all_waiting(self.result_workers) and \
               LinksWorker.all_waiting(self.link_workers)

    def all_stopped(self):
        return ResultsWorker.all_stopped(self.result_workers) and \
               LinksWorker.all_stopped(self.link_workers)

    def exceeded_max_duration(self):
        if self.finished_at:
            return (self.finished_at - self.started_at) > self.max_duration
        elif self.started_at:
            return (dt.datetime.now() - self.started_at) > self.max_duration
        else:
            return False

    def finished(self):
        return self.all_waiting() or self.exceeded_max_duration() or self.all_stopped()

    def run(self):
        """
        Starts running the parser
        """

        self.started_at = dt.datetime.now()
        self.logger.okay(f"Starting")
        self.logger.okay(f"Using crawler {self.parser.module.__file__}")
        self.logger.okay(f"Using seeds {self.parser.seeds()}")
        self.logger.okay(f"Writing to {self.writer.url}")
        self.link_workers = LinksWorker.start_all(self.num_link_workers, links_queue=self.queue, results_queue=self.results, parser=self.parser)
        self.result_workers = ResultsWorker.start_all(self.num_results_workers, writer=self.writer, results_queue=self.results)

        while not self.finished():
            continue
        else:
            LinksWorker.stop_all(self.link_workers)
            ResultsWorker.stop_all(self.result_workers)
            self.logger.okay("Stopped all workers")
            self.logger.okay("Finished run")
            self.finished_at = dt.datetime.now()
