from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase
from deepeval.scorer import Scorer


class ExactMatchMetric(BaseMetric):
    def __init__(self, threshold: float = 0.0, async_mode: bool = True):
        self.threshold = threshold
        self.async_mode = async_mode

    def _base_measure(self, test_case: LLMTestCase):
        self.success = Scorer.exact_match_score(
            test_case.actual_output, test_case.expected_output
        )
        if self.success:
            self.score = 1
        else:
            self.score = 0
        return self.score

    def measure(self, test_case: LLMTestCase):
        self._base_measure(test_case=test_case)

    async def a_measure(self, test_case: LLMTestCase):
        self._base_measure(test_case=test_case)

    def is_successful(self):
        return bool(self.success)

    @property
    def __name__(self):
        return "ExactMatch"