import logging
import pytest
import pytest_asyncio
import pandas as pd

from prefect.testing.utilities import prefect_test_harness
from dotenv import load_dotenv

from models.metric import MetricDefinition

load_dotenv()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prefect_test_fixture():
    """Setup and teardown prefect test environment"""
    with prefect_test_harness():
        yield


@pytest.fixture(autouse=True)
def setup_logging():
    logging.getLogger("prefect").setLevel(logging.WARNING)
    yield


@pytest.fixture(scope="function")
def correctness_metric() -> MetricDefinition:
    correctness_metric: MetricDefinition = MetricDefinition.from_json(
        r"C:\Users\steqi\Documents\llm-evaluation\tests\data\metrics\correctness.json"
    )
    print(correctness_metric)
    return correctness_metric


@pytest.fixture
def sample_conversation_data():
    return {
        "conv_1": pd.DataFrame(
            {
                "timestamp": ["2024-01-01 10:00:00"],
                "role": ["user"],
                "content": ["Hello"],
            }
        ),
        "conv_2": pd.DataFrame(
            {
                "timestamp": ["2024-01-01 10:01:00"],
                "role": ["assistant"],
                "content": ["Hi there"],
            }
        ),
    }


@pytest.fixture
def sample_conversation_csv_data_path():
    return "tests/data/conversation/Result-YepAI.csv"


@pytest.fixture
def sample_metrics_json_path():
    return "tests/data/metrics/correctness.json"


@pytest.fixture
def sample_metrics():
    return [
        {
            "name": "correctness",
            "description": "Test metric",
            "evaluation_type": "basic",
        }
    ]
