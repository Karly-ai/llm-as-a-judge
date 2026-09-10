# LLM-as-a-Judge: Dispatch Validation Evaluation

An AI Quality Engineering project that uses **Claude as an LLM-as-a-Judge** to evaluate validation error messages for a synthetic smart thermostat demand-response event system.

The project combines deterministic software testing with LLM-based semantic evaluation and integrates both into a **GitHub Actions CI/CD quality gate**.

## Project Goal

The goal is to determine whether an actual validation error message correctly communicates the same validation rule as an expected error message, even when the wording is different.

For example:

**Expected:**

> Precool cannot be set for Emergency events.

**Actual:**

> Emergency events do not support precooling.

Although the wording is different, both messages communicate the same validation rule. The LLM judge should therefore classify the result as:

**PASS**

The project also includes deliberately incorrect messages to test whether the judge can distinguish a genuinely equivalent message from an unrelated or incorrect validation rule.

## Key Features

* Python-based event validation
* Synthetic demand-response / smart thermostat scenarios
* 50-case LLM evaluation benchmark
* Claude-based semantic evaluation
* Structured evaluation rubric
* Positive and negative test cases
* False-positive and false-negative tracking
* Accuracy measurement
* Automated 95% CI/CD quality gate
* GitHub Actions integration
* Evaluation results saved as a CI artifact

## Current Benchmark Results

| Metric                  |   Result |
| ----------------------- | -------: |
| Total test cases        |       50 |
| True Positives          |       29 |
| True Negatives          |       21 |
| False Positives         |        0 |
| False Negatives         |        0 |
| Classification Accuracy | **100%** |
| CI Quality Threshold    |  **95%** |

> **Note:** The benchmark uses synthetic test cases created for this portfolio project. The validation rules are not presented as proprietary production rules.

## Why LLM-as-a-Judge?

Traditional automated tests often compare expected and actual results using exact string matching.

For example:

```text
Expected:
Precool cannot be set for Emergency events.

Actual:
Emergency events do not support precooling.
```

A traditional assertion such as:

```python
assert actual_error == expected_error
```

would fail because the strings are different.

However, the two messages communicate the **same validation rule**.

This project uses an LLM-as-a-Judge approach to evaluate the **meaning** of the messages rather than requiring an exact wording match.

### What the Judge Evaluates

The Claude-based judge evaluates each actual validation message against the expected message using several criteria:

* **Correctness** — Does the message communicate the correct validation rule?
* **Relevance** — Does it address the specific event configuration?
* **Completeness** — Does it include the important conditions of the rule?
* **Hallucination** — Does it introduce unsupported rules or information?
* **Overall score** — How closely does the actual message match the expected validation rule?

The judge returns a structured result containing the evaluation scores, a PASS/FAIL decision, and a brief explanation.

### Semantic Evaluation

The judge is instructed to focus on the underlying validation rule rather than surface-level wording.

For example:

| Expected Message                            | Actual Message                                      | Result |
| ------------------------------------------- | --------------------------------------------------- | ------ |
| Precool cannot be set for Emergency events. | Emergency events do not support precooling.         | PASS   |
| End time must be after start time.          | The event end time must occur after its start time. | PASS   |
| Preheat cannot be set for Emergency events. | Event duration must be greater than zero.           | FAIL   |

This allows the test framework to recognize legitimate variations in wording while still rejecting messages that describe a different validation rule.

### Why This Matters for AI Quality Engineering

LLM-powered applications frequently produce responses that can be **semantically correct even when their wording differs**.

Exact string matching is therefore often too rigid for evaluating generated language.

An LLM-as-a-Judge can provide a more flexible evaluation layer while automated benchmark cases, structured rubrics, and CI quality gates provide additional controls around the judge itself.

## System Architecture

The project uses a layered architecture that separates deterministic validation, test data, LLM evaluation, and CI/CD automation.

```text
                    Developer
                        │
                        ▼
                  Git Push / PR
                        │
                        ▼
                GitHub Actions
                        │
              ┌─────────┴─────────┐
              │                   │
              ▼                   ▼
       Deterministic Tests    LLM Evaluation
              │                   │
              ▼                   ▼
       Dispatch Validator      Claude Judge
              │                   │
              │             Semantic Evaluation
              │                   │
              └─────────┬─────────┘
                        │
                        ▼
                Evaluation Metrics
                        │
                        ▼
                  Accuracy ≥ 95%?
                    /        \
                  YES          NO
                   │            │
                   ▼            ▼
                🟢 PASS       🔴 FAIL
                   │
                   ▼
          Evaluation Artifact
```

### Main Components

#### 1. Dispatch Validator

`app/dispatch_validator.py`

The deterministic validation layer applies predefined validation rules to event configurations.

It produces validation error messages such as:

```text
Precool cannot be set for Emergency events.
```

This component represents the system under test.

#### 2. Synthetic Test Dataset

`data/dispatch_test_cases.json`

The dataset contains **50 synthetic event configurations**.

Each test case includes:

* Event configuration
* Expected validation message
* Event type
* Relevant timing or configuration fields

The benchmark includes both correct semantic variations and deliberately incorrect messages.

#### 3. LLM Judge

`judge/judge.py`

Claude evaluates whether the actual validation message communicates the same rule as the expected message.

The judge is specifically instructed to evaluate the **validation rule**, rather than relying on exact string matching.

It also considers important dimensions such as:

* Event type
* Field being validated
* Validation condition
* Allowed or disallowed behavior
* Timing relationships
* Numeric constraints
* Required versus optional fields

#### 4. Evaluation Runner

`judge/evaluate.py`

The evaluation runner:

1. Loads the 50 test cases
2. Runs each event through the Dispatch validator
3. Extracts the actual validation message
4. Sends the expected and actual messages to Claude
5. Records the judge decision
6. Calculates evaluation metrics
7. Saves detailed results
8. Applies the CI quality threshold

#### 5. CI/CD Quality Gate

`.github/workflows/ci.yml`

GitHub Actions automatically runs the test suite and LLM evaluation.

The pipeline requires the LLM judge to achieve at least **95% classification accuracy**.

If accuracy falls below the threshold, the workflow exits with a failure status.

This creates an automated quality gate that can prevent a regression in the evaluation system from being silently accepted.

### Evaluation Flow

For each test case:

```text
Test Case
    ↓
Dispatch Validator
    ↓
Actual Error Message
    ↓
Expected vs. Actual
    ↓
Claude LLM Judge
    ↓
PASS / FAIL
    ↓
Performance Metrics
```

The separation between deterministic validation and LLM evaluation makes it possible to test both the **system behavior** and the **quality of the AI-based evaluator** independently.

## Project Structure

```text
llm-as-a-judge/
│
├── app/
│   └── dispatch_validator.py
│
├── data/
│   └── dispatch_test_cases.json
│
├── judge/
│   ├── judge.py
│   ├── evaluate.py
│   └── check_claude.py
│
├── tests/
│   └── test_dispatch_validator.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .env
├── .gitignore
├── dispatch_evaluation_results.json
└── README.md
```

### Directory and File Descriptions

| Path                               | Purpose                                                                          |
| ---------------------------------- | -------------------------------------------------------------------------------- |
| `app/dispatch_validator.py`        | Contains the deterministic Dispatch event validation logic                       |
| `data/dispatch_test_cases.json`    | Contains the 50-case synthetic evaluation benchmark                              |
| `judge/judge.py`                   | Implements the Claude-based LLM-as-a-Judge                                       |
| `judge/evaluate.py`                | Runs the benchmark, calculates metrics, and enforces the CI quality gate         |
| `judge/check_claude.py`            | Used to verify the configured Claude API/model setup                             |
| `tests/test_dispatch_validator.py` | Deterministic unit tests for the Dispatch validator                              |
| `.github/workflows/ci.yml`         | GitHub Actions CI/CD workflow                                                    |
| `.gitignore`                       | Prevents secrets, virtual environments, and generated files from being committed |
| `dispatch_evaluation_results.json` | Detailed evaluation output generated by the evaluation runner                    |
| `README.md`                        | Project documentation                                                            |

### Separation of Responsibilities

The project intentionally separates responsibilities across components:

```text
app/
  → System under test

data/
  → Evaluation dataset

tests/
  → Deterministic software tests

judge/
  → LLM evaluation and benchmark metrics

.github/
  → CI/CD automation
```

This separation makes the project easier to maintain and allows the deterministic tests and LLM evaluation layer to evolve independently.
## Evaluation Methodology

The evaluation framework compares an expected validation message with the actual message generated by the deterministic Dispatch validator.

The goal is to determine whether both messages communicate the **same underlying validation rule**.

### Evaluation Process

For each test case, the evaluation runner:

1. Loads the synthetic event configuration.
2. Passes the configuration to the Dispatch validator.
3. Captures the actual validation error.
4. Provides the expected and actual messages to Claude.
5. Asks Claude to evaluate their semantic equivalence.
6. Records the evaluation scores and PASS/FAIL decision.
7. Compares the judge decision against the benchmark ground truth.
8. Calculates classification metrics.

### Evaluation Rubric

Claude evaluates the actual message using the following criteria:

| Criterion         | Description                                                      |
| ----------------- | ---------------------------------------------------------------- |
| **Correctness**   | Does the actual message communicate the correct validation rule? |
| **Relevance**     | Does the message address the specific event configuration?       |
| **Completeness**  | Does it preserve the important conditions of the expected rule?  |
| **Hallucination** | Does it introduce unsupported information or a different rule?   |
| **Overall Score** | Overall semantic similarity to the expected validation rule      |

Each criterion is evaluated on a **1–5 scale**.

The judge returns a structured JSON response containing:

```json
{
    "correctness": 5,
    "relevance": 5,
    "completeness": 5,
    "hallucination": 5,
    "overall_score": 5,
    "pass": true,
    "reason": "The messages communicate the same validation rule."
}
```

### PASS Criteria

A test case is classified as **PASS** when:

* The actual message is semantically equivalent to the expected validation rule.
* The important conditions of the rule are preserved.
* The message does not introduce a different validation rule.
* The overall evaluation score is at least **4**.

The judge is explicitly instructed not to consider messages equivalent merely because they:

* Describe the same general problem
* Refer to the same event type
* Mention the same field
* Have a similar root cause
* Both indicate that an event is invalid
* Concern the same general topic

The **validation rule itself must match**.

### Negative Test Cases

The benchmark intentionally includes incorrect messages to test whether the judge can reject superficially related but incorrect answers.

For example:

```text
Expected:
Precool cannot be set for Emergency events.

Actual:
Preheat cannot be set for Emergency events.
```

Both messages concern Emergency events and temperature-related configuration, but they validate **different fields**.

Therefore, the correct result is:

```text
FAIL
```

### Semantic Equivalence

The benchmark also includes cases where the wording differs but the validation rule is equivalent.

For example:

```text
Expected:
End time must be after start time.

Actual:
The event end time must occur after its start time.
```

The wording is different, but the underlying rule is identical.

Therefore, the correct result is:

```text
PASS
```

This combination of positive semantic-equivalence cases and negative cases helps evaluate whether the judge is distinguishing **meaning** rather than simply matching keywords.

## Benchmark Design & Results

The benchmark contains **50 synthetic test cases** designed to evaluate both the Dispatch validation logic and the ability of the LLM judge to distinguish semantic equivalence from incorrect validation messages.

### Benchmark Categories

The test cases include:

* Emergency event restrictions
* Scheduled event requirements
* Start and end time validation
* Event duration validation
* Precooling configuration
* Timing relationships
* Missing required fields
* Semantically equivalent messages
* Incorrect validation rules
* Unrelated or conflicting validation messages

### Positive Cases

The benchmark contains **29 cases expected to PASS**.

These include:

* Exact or near-exact matches
* Different wording with the same meaning
* Equivalent descriptions of the same validation rule

### Negative Cases

The benchmark contains **21 cases expected to FAIL**.

These cases intentionally provide incorrect messages, including messages that:

* Refer to the wrong field
* Refer to the wrong event type
* Describe a different validation condition
* Provide an unrelated validation rule
* Sound similar but do not express the same rule

### Results

The current benchmark produced the following results:

| Metric                  |     Result |
| ----------------------- | ---------: |
| Total Cases             |         50 |
| True Positives          |         29 |
| True Negatives          |         21 |
| False Positives         |          0 |
| False Negatives         |          0 |
| Classification Accuracy | **100.0%** |

### Confusion Matrix

|                 | Predicted PASS | Predicted FAIL |
| --------------- | -------------: | -------------: |
| **Actual PASS** |             29 |              0 |
| **Actual FAIL** |              0 |             21 |

The judge correctly classified all 50 benchmark cases.

In particular, the benchmark produced **zero false positives**, meaning that none of the deliberately incorrect validation messages were incorrectly approved by the judge.

### Interpretation

The results demonstrate that the current evaluation prompt and rubric correctly distinguish semantic equivalence from incorrect validation rules across this synthetic benchmark.

The **100% accuracy result applies specifically to these 50 benchmark cases** and should not be interpreted as proof that an LLM judge will always produce correct evaluations on unseen data.

Additional testing with larger, independently generated, and adversarial datasets would be required to establish stronger confidence in judge reliability.

## CI/CD Integration

The project uses **GitHub Actions** to automatically execute deterministic tests and LLM-based evaluation as part of the CI/CD pipeline.

### Workflow

```text
Developer pushes code
        ↓
GitHub Actions starts
        ↓
Install Python dependencies
        ↓
Run deterministic unit tests
        ↓
8 tests must pass
        ↓
Run 50-case LLM evaluation
        ↓
Claude evaluates validation messages
        ↓
Calculate judge performance
        ↓
Check 95% accuracy threshold
        ↓
Generate evaluation artifact
        ↓
       PASS
```

### GitHub Actions Jobs

The workflow contains two main jobs.

#### 1. Unit Tests

The first job runs the deterministic test suite:

```bash
PYTHONPATH=. pytest
```

The current test suite contains **8 unit tests** covering the Dispatch validation rules.

The LLM evaluation job depends on the unit tests passing.

This prevents the LLM evaluation from running when the underlying deterministic validation code is already failing.

#### 2. LLM Evaluation

After the unit tests pass, the second job executes:

```bash
PYTHONPATH=. python -m judge.evaluate
```

This runs all 50 benchmark cases and sends the expected and actual validation messages to Claude.

The Anthropic API key is stored securely as a **GitHub Actions Secret** and is injected into the workflow at runtime.

The API key is not stored in the source code.

### CI Quality Gate

The evaluation runner enforces a minimum judge accuracy threshold of:

```text
95%
```

The logic is:

```python
minimum_accuracy = 95.0

if accuracy < minimum_accuracy:
    raise SystemExit(1)
```

If the accuracy falls below the threshold, the evaluation exits with a non-zero status and the GitHub Actions workflow fails.

If the accuracy meets or exceeds the threshold, the workflow continues successfully.

### Evaluation Artifact

The evaluation runner saves detailed results to:

```text
dispatch_evaluation_results.json
```

The generated file contains information such as:

* Test case ID
* Event configuration
* Expected validation message
* Actual validation message
* LLM evaluation scores
* PASS/FAIL decision
* Judge reasoning

The file is uploaded by GitHub Actions as a workflow artifact for further inspection.

### Security

Secrets are handled through environment variables and GitHub Actions Secrets.

The repository excludes sensitive and generated files through `.gitignore`, including:

```text
.env
.venv/
dispatch_evaluation_results.json
```

This prevents the local API key and generated evaluation output from being committed to the repository.
