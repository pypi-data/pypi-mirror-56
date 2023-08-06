import logging
from threading import Thread, Event

LOGGER = logging.getLogger(__name__)


class Trigger(Thread):
    """Periodically execute registered tasks.
    """

    def __init__(self):
        Thread.__init__(self)
        self.tasks = []
        self.running = False

    def add_task(self, task: Thread):
        self.tasks.append(task)

    def run_nonblocking(self):
        self.run()
        self.running = True

    def start_blocking(self, close_event: Event):
        self.run_nonblocking()
        close_event.wait()
        self.stop_tasks()

    def run(self):
        LOGGER.info("Starting tasks...")

        for t in self.tasks:
            t.start()
            LOGGER.info("Active task {}".format(t.name))

        LOGGER.info("Trigger is active.")

    def stop_tasks(self):
        for t in self.tasks:
            LOGGER.info("Stopping task {}".format(t.name))
            t.stop()

        LOGGER.info("Trigger exited.")
