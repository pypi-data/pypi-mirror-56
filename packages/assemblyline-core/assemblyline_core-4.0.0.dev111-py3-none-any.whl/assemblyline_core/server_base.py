"""
A base class to provide a common set of behaviours for the assemblyline core server nodes.
"""
import time
import threading
import logging
import signal
import sys

from assemblyline.common import log as al_log
# al_log.init_logging(component_name)

SHUTDOWN_SECONDS_LIMIT = 10


class ServerBase(threading.Thread):
    """Utility class for Assmblyline server processes.

    Inheriting from thread so that the main work is done off the main thread.
    This lets the main thread handle interrupts properly, even when the workload
    makes a blocking call that would normally stop this.
    """
    def __init__(self, component_name: str, logger: logging.Logger = None,
                 shutdown_timeout: float = SHUTDOWN_SECONDS_LIMIT):
        super().__init__(name=component_name)
        al_log.init_logging(component_name)

        self.running = None
        self.log = logger or logging.getLogger(component_name)
        self._exception = None
        self._traceback = None
        self._shutdown_timeout = shutdown_timeout
        self._old_sigint = None
        self._old_sigterm = None

    def __enter__(self):
        self.log.info(f"Initialized")
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        self.close()
        if _exc_type is not None:
            self.log.exception(f'Terminated because of an {_exc_type} exception')
        else:
            self.log.info(f'Terminated')

    def __stop(self):
        """Hard stop"""
        time.sleep(self._shutdown_timeout)
        self.log.error(f"Server has shutdown hard after waiting {self._shutdown_timeout} seconds to stop")
        exit(1)

    def close(self):
        pass

    def interrupt_handler(self, signum, stack_frame):
        self.log.info(f"Instance caught signal. Coming down...")
        self.stop()
        if signum == signal.SIGINT and self._old_sigint:
            self._old_sigint(signum, stack_frame)
        if signum == signal.SIGTERM and self._old_sigterm:
            self._old_sigterm(signum, stack_frame)

    def raising_join(self):
        self.join()
        if self._traceback and self._exception:
            raise self._exception.with_traceback(self._traceback)

    # noinspection PyBroadException
    def run(self):
        try:
            self.try_run()
        except Exception:
            _, self._exception, self._traceback = sys.exc_info()
            self.log.exception("Exiting:")

    def serve_forever(self):
        self.start()
        self.join()

    def start(self):
        """Start the server workload."""
        self.running = True
        super().start()
        self.log.info(f"Started")
        self._old_sigint = signal.signal(signal.SIGINT, self.interrupt_handler)
        self._old_sigterm = signal.signal(signal.SIGTERM, self.interrupt_handler)

    def stop(self):
        """Ask nicely for the server to stop.

        After a timeout, a hard stop will be triggered.
        """
        # The running loops should stop within a few seconds of this flag being set.
        self.running = False

        # If it doesn't stop within a few seconds, this other thread should kill the entire process
        stop_thread = threading.Thread(target=self.__stop)
        stop_thread.daemon = True
        stop_thread.start()

    def try_run(self):
        pass

