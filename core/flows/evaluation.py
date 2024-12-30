import nest_asyncio

from prefect import flow
from prefect.logging import get_run_logger
from typing import List, Union
from models.metric import MetricDefinition
from models.evaluation import EvaluationResult
from core.tasks.evaluation import evaluate_all_conversations


# TODO: ?
original_apply = nest_asyncio.apply


def _patched_apply(*args, **kwargs):
    if not getattr(_patched_apply, "applied", False):
        original_apply(*args, **kwargs)
        _patched_apply.applied = True


nest_asyncio.apply = _patched_apply
nest_asyncio.apply()


@flow
async def evaluate_flow(
    metrics_dict_or_path_list: List[Union[str, dict]], csv_file_path: str
):
    """
    This flow evaluates the conversations in the given CSV file using the given metrics.

    Args:
        metrics_dict_or_path_list (List[Union[str, dict]]): A list of metric definitions or paths to metric definitions.
        csv_file_path (str): The path to the CSV file containing the conversations to be evaluated.

    Returns:
        List[EvaluationResult]: A list of evaluation results for each conversation in the CSV file.
    """
    logger = get_run_logger()
    logger.info("core.flows.evaluation.start")

    metrics: List[MetricDefinition] = [
        MetricDefinition.from_json(metrics_dict_or_path)
        for metrics_dict_or_path in metrics_dict_or_path_list
    ]
    logger.info(f"core.flows.evaluation: Metrics: {metrics}")

    results: List[EvaluationResult] = await evaluate_all_conversations(
        file_path=csv_file_path, metrics=metrics
    )
    logger.info(f"core.flows.evaluation: Results: {[r.model_dump() for r in results]}")

    logger.info("core.flows.evaluation.end")
    return results
