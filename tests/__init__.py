import unittest

from goless.backends import Deadlock
from goless.backends import current as be


class BaseTests(unittest.TestCase):
    """
    Base class for unit tests.
    Yields in setup and teardown so no lingering tasklets
    are run in a later test,
    potentially causing an error that would leave people scratching their heads.
    """

    def setUp(self):
        # These yields fail with an exception in stackless.py if no tasklets are running.
        # Since we yield to make sure that's the case, we can swallow the exception.
        try:
            be.yield_()
        except Deadlock:
            pass

        def doyield():
            try:
                be.yield_()
            except Deadlock:
                pass

        self.addCleanup(doyield)
