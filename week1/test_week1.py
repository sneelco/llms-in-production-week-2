
from langchain.schema import HumanMessage
import pandas as pd

from deepeval.test_case import LLMTestCase
from deepeval.dataset import EvaluationDataset
from deepeval.evaluate import aggregate_metric_pass_rates

from week1.llm import llm
from week1.consts import BASIC_GROUND_TRUTH_DATASET, ZERO_SHOT_PROMPT_TEMPLATE, FEW_SHOT_PROMPT_TEMPLATE
from week1.metrics import ExactMatchMetric

df = pd.DataFrame(BASIC_GROUND_TRUTH_DATASET)

test_cases = []

def run_eval(PROMPT):
    for test_data in BASIC_GROUND_TRUTH_DATASET:
        test_case_query = test_data["Query"]
        test_case_expected_output = test_data["Ground Truth"]
        test_case_context = [""]

        # Build the prompt
        prompt = PROMPT.format(
            query=test_case_query
        )
        # Execute and to get the result
        result = llm.generate([[HumanMessage(content=prompt)]])
        test_case_actual_output = result.generations[0][0].text

        # Run the test
        test_case = LLMTestCase(
            input=test_case_query,
            actual_output=test_case_actual_output,
            expected_output=test_case_expected_output,
            context=test_case_context
        )

        test_cases.append(test_case)

    dataset = EvaluationDataset(test_cases=test_cases)

    exact_match_metric = ExactMatchMetric()
    result = dataset.evaluate([exact_match_metric])

    pass_rate_run_1 = aggregate_metric_pass_rates(result.test_results)

    return pass_rate_run_1.get("ExactMatch")

def test_zeroshot():
    result = run_eval(ZERO_SHOT_PROMPT_TEMPLATE)

    assert result > 0.3


def test_fewshot():
    for test_data in BASIC_GROUND_TRUTH_DATASET:
        test_case_query = test_data["Query"]
        test_case_expected_output = test_data["Ground Truth"]
        test_case_context = [""]

        # Build the prompt
        prompt = FEW_SHOT_PROMPT_TEMPLATE.format(
            query=test_case_query
        )
        # Execute and to get the result
        result = llm.generate([[HumanMessage(content=prompt)]])
        test_case_actual_output = result.generations[0][0].text

        # Run the test
        test_case = LLMTestCase(
            input=test_case_query,
            actual_output=test_case_actual_output,
            expected_output=test_case_expected_output,
            context=test_case_context
        )

        test_cases.append(test_case)

    dataset = EvaluationDataset(test_cases=test_cases)

    exact_match_metric = ExactMatchMetric()
    result = dataset.evaluate([exact_match_metric])

    pass_rate_run_1 = aggregate_metric_pass_rates(result.test_results)

    assert pass_rate_run_1.get("ExactMatch") > 0.4
