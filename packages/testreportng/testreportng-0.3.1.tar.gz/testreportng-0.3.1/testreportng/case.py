import unittest

from testreportng.result import NGCaseDetail, NGResult
from testreportng.constants import Label
from testreportng.utils import get_timestamp


class NGCase(unittest.TestCase):
    # default cls
    ng_detail_kls = NGCaseDetail
    ng_result_kls = NGResult

    # result inst
    ng_result: NGResult

    # ng hook
    def _start_hook(self, name: str):
        mapping = {
            Label.LABEL_STATUS_PASS: "when_pass",
            Label.LABEL_STATUS_FAIL: "when_fail",
            Label.LABEL_STATUS_ERROR: "when_error",
            Label.LABEL_STATUS_SKIP: "when_skip",
        }
        assert name in mapping, f"hook [ {name} ] not found"
        target = mapping[name]
        assert hasattr(self, target)
        return getattr(self, target)()

    def when_pass(self):
        """ will execute when case passed """
        pass

    def when_fail(self):
        """ will execute when case failed """

    def when_error(self):
        """ will execute when case error """

    def when_skip(self):
        """ will execute when case skipped """
        pass

    def when_always(self):
        """ will execute after each cases """
        pass

    # origin hook
    @classmethod
    def setUpClass(cls) -> None:
        cls.ng_result: NGResult = cls.ng_result_kls(cls.__name__)

    def setUp(self) -> None:
        # init this case
        cur = self.ng_detail_kls(self._testMethodName)
        # time record
        cur.start_time = get_timestamp()
        self.ng_result.set(cur)

    def tearDown(self) -> None:
        # update case's result
        cur = self.ng_result.get(self._testMethodName)
        # time record
        cur.end_time = get_timestamp()
        cur.duration = cur.end_time - cur.start_time
        cur.outcome = getattr(self, "_outcome")
        self.ng_result.set(cur)

        # ng hook
        self._start_hook(cur.status)
        self.when_always()
