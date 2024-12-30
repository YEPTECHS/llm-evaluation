# llm-evaluation

This repository demonstrates how to asynchronously evaluate multi-turn conversations using the **deepeval** library. We split our logic into **preprocessing**, **evaluation**, and **metrics** modules, and use **pytest** for testing.

## Requirements

1. `uv sync --all-extras` to install the required dependencies.
2. `uv run pre-commit install` to install the pre-commit hooks.

## Project Structure


![image](https://github.com/user-attachments/assets/9bbd521a-5914-4862-9425-f4c7758889a3)


### core/
- **`evaluater.py`**
  Implements async evaluation with functions like `evaluate_all_conversations()`. Uses **deepeval** classes (`LLMTestCase`, `ConversationalTestCase`) to build multi-turn dialogues and measure them with metrics.
- **`preprocessing.py`**
  Provides an async routine (`preprocess_csv`) to load CSV data via `pandas`, clean/ filter duplicates, split by `ConversationID`, etc.

### models/
- **`metric.py`**
  Defines or loads metric configurations (e.g., `MetricDefinition` objects that contain `criteria`, `evaluation_steps`, etc.). Can also import or wrap **deepeval** metrics like `ConversationalGEval`.

### tests/
- **`data/`**
  Holds sample conversation CSVs (`Result-YepAI.csv`) and metric JSON configurations (`correctness.json`).
- **`conftest.py`**
  Declares common **pytest** fixtures (e.g., a `correctness_metric` fixture that references `correctness.json`).
- **`test_evaluator.py`**
  Tests the logic in `core.evaluater`.
- **`test_metrics.py`**
  Validates metric definitions in `models.metric`.

### Miscellaneous
- **`ttt_results.py`**
  A simple script to invoke the evaluator and print or inspect results, useful for quickly debugging outside of pytest.

---
### Usage
Evaluating Conversations
If you want to run an evaluation script (e.g., ttt_results.py):

python ttt_results.py
Under the hood, it might:

1.Load metrics (e.g., correctness).
2.Call evaluate_all_conversations() from core.evaluater.
3.Print or save the resulting scores.
