import pytest

from typing import List

from models.evaluation import EvaluationResult
from core.flows.evaluation import evaluate_flow


@pytest.mark.asyncio
async def test_evaluation_flow(
    sample_conversation_csv_data_path, sample_metrics_json_path
):
    results: List[EvaluationResult] = await evaluate_flow(
        metrics_dict_or_path_list=[sample_metrics_json_path],
        csv_file_path=sample_conversation_csv_data_path,
    )
    assert len(results) != 0  # TODO: need to be exact number of results
    assert results[0] is not None
    # TODO: Add more assertions to check the content of the EvaluationResult object
