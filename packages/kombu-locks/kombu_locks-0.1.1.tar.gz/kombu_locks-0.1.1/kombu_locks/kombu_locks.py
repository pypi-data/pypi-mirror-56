import time
import logging
from kombu import Connection, Exchange, Queue


CHANNEL_ERRORS = []
try:
    import amqp.exceptions
    CHANNEL_ERRORS.append(amqp.exceptions.ResourceLocked)
except ImportError:
    pass
try:
    import _librabbitmq
    CHANNEL_ERRORS.append(_librabbitmq.ChannelError)
except ImportError:
    pass
CHANNEL_ERRORS = tuple(CHANNEL_ERRORS)


logger = logging.getLogger(__name__)


class LockError(Exchange):
    pass


class Lock(object):
    def __init__(self, connection_string, key, wait=0.5):
        self._connection_string = connection_string
        self._key = key
        self._lock_key = 'lock.{}'.format(key)
        self._wait = wait
        self._connection = None
        self._channel = None
        self._queue = None

    def adquire(self, block=True):
        if self._connection is not None or self._channel is not None or self._queue is not None:
            raise LockError("adquiring/adquired lock")
        self._connection = Connection(self._connection_string)
        self._channel = self._connection.channel()
        is_waiting = False
        while True:
            try:
                self._queue = Queue(name=self._lock_key, channel=self._channel, exclusive=True,)
                self._queue.declare()
                logger.debug("[kombu-lock] Adquired lock for key: '{}'".format(self._lock_key))
                return True
            except CHANNEL_ERRORS:
                if not block:
                    self._channel.close()
                    self._channel = None
                    self._connection.close()
                    self._connection = None
                    return False
                if not is_waiting:
                    logger.debug("[kombu-lock] Waiting to adquire lock for key: '{}'".format(self._lock_key))
                    is_waiting = True
                time.sleep(self._wait)

    def release(self):
        if self._queue is not None:
            self._queue.delete()
            self._queue = None
        if self._channel is not None:
            self._channel.close()
            self._channel = None
        if self._connection is not None:
            self._connection.close()
            self._connection = None
        logger.debug("[kombu-lock] Released lock for key: '{}'".format(self._lock_key))

    def __enter__(self):
        self.adquire(block=True)

    def __exit__(self, *args, **kwargs):
        self.release()

    @property
    def is_adquired(self):
        return self._queue is not None
