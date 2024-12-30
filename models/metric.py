import json

from pydantic import BaseModel, Field
from typing import List

from deepeval.test_case import LLMTestCaseParams


class MetricDefinition(BaseModel):
    """
    a class to define a metric

    Attributes:
        name (str): Name of the metric
        criteria (str): Criteria description for the metric
        evaluation_steps (List[str]): List of evaluation steps describtion for the metric
        evaluation_params (List[LLMTestCaseParams]): List of evaluation parameters for the metric

    Examples:
        >>> metric_def = MetricDefinition(name="BLEU",
                                          criteria="BLEU score",
                                          evaluation_steps=["1. Tokenize the input and reference sentences",
                                                            "2. Calculate the BLEU score"],
                                          evaluation_params=[LLMTestCaseParams.INPUT,
                                                             LLMTestCaseParams.ACTUAL_OUTPUT])
    """

    name: str = Field(..., description="Name of the metric")
    criteria: str = Field(..., description="Criteria description for the metric")
    evaluation_steps: List[str] = Field(
        ..., description="List of evaluation steps describtion for the metric"
    )
    evaluation_params: List[LLMTestCaseParams] = Field(
        default=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        description="List of evaluation parameters for the metric",
    )

    @staticmethod
    def from_json(json_path_or_dict: str):
        if isinstance(json_path_or_dict, str):
            metric_json = json.load(open(json_path_or_dict))
        else:
            metric_json = json_path_or_dict
        return MetricDefinition(**metric_json)
