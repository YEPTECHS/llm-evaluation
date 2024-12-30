import asyncio
import pandas as pd

from typing import List, Dict
from prefect import task
from prefect.logging import get_run_logger
from deepeval.test_case import ConversationalTestCase, LLMTestCase
from deepeval.metrics import ConversationalGEval

from models.evaluation import EvaluationResult
from models.metric import MetricDefinition
from utils.preprocessing import preprocess_csv


@task
async def evaluate_single_conversation(
    conversation_id: str, df: pd.DataFrame, metrics: List[MetricDefinition]
) -> EvaluationResult:
    logger = get_run_logger()

    turns = []
    conversation_content = []
    user_input = None

    try:
        for _, row in df.iterrows():
            match row["Role"]:
                case "user":
                    user_input = row["Content"]
                    conversation_content.append(f"User: {user_input}")
                case "assistant" if user_input:
                    turns.append(
                        LLMTestCase(input=user_input, actual_output=row["Content"])
                    )
                    conversation_content.append(f"Assistant: {row['Content']}")
                    user_input = None

        if not turns:
            return EvaluationResult(
                ConversationID=conversation_id,
                ConversationContent="\n".join(conversation_content),
                scores={},
                reasons={},
            )

        test_case = ConversationalTestCase(turns=turns)

        scores = {}
        reasons = {}

        for metric in metrics:
            eval_metric = ConversationalGEval(
                name=metric.name,
                criteria=metric.criteria,
                evaluation_steps=metric.evaluation_steps,
                evaluation_params=metric.evaluation_params,
            )
            eval_metric.measure(test_case)
            scores[metric.name] = eval_metric.score
            reasons[metric.name] = eval_metric.reason

        return EvaluationResult(
            ConversationID=conversation_id,
            ConversationContent="\n".join(conversation_content),
            scores=scores,
            reasons=reasons,
        )

    except Exception as e:
        logger.error(
            f"core.tasks.evaluation.evaluate.single_conversation.error: conversation {conversation_id}: {e}"
        )


@task
async def evaluate_all_conversations(
    file_path: str, metrics: List[MetricDefinition], **kwargs
) -> List[EvaluationResult]:
    # TODO: replace with real data and preprocessing
    conversation_dict: Dict[str, pd.DataFrame] = await preprocess_csv(
        file_path, **kwargs
    )

    tasks = []
    for conversation_id in conversation_dict.keys():
        tasks.append(
            evaluate_single_conversation(
                conversation_id=conversation_id,
                df=conversation_dict[conversation_id],
                metrics=metrics,
            )
        )

    results = await asyncio.gather(*tasks)
    return list(results)
