# llm-evaluation

This repository demonstrates how to asynchronously evaluate multi-turn conversations using the **deepeval** library. We split our logic into **preprocessing**, **evaluation**, and **metrics** modules, and use **pytest** for testing.

## Project Structure

.
├── core
│   ├── __init__.py
│   ├── evaluater.py       # Contains async evaluation logic and calls to deepeval
│   └── preprocessing.py    # Async CSV reading and data filtering
├── models
│   ├── __init__.py
│   └── metric.py           # Metric definitions (e.g., correctness, relevance) 
├── tests
│   ├── data
│   │   ├── conversation
│   │   │   └── Result-YepAI.csv
│   │   └── metrics
│   │       └── correctness.json
│   ├── .deepeval_telemtry.txt  # Telemetry file (tracking usage, if enabled)
│   ├── __init__.py
│   ├── conftest.py         # Pytest fixtures
│   ├── test_evaluator.py   # Tests for evaluation logic
│   └── test_metrics.py     # Tests for metric definitions
├── .deepeval_telemtry.txt  # Another copy or placeholder of deepeval telemetry
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml
├── ttt_results.py          # A script to print or inspect evaluation results
└── uv.lock
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
