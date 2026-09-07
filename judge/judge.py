import json
import os

from dotenv import load_dotenv
from anthropic import Anthropic


load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise RuntimeError(
        "ANTHROPIC_API_KEY is not set."
    )

client = Anthropic(api_key=api_key)


def evaluate_answer(question, expected_answer, actual_answer):

    prompt = f"""
You are an expert QA evaluator for a smart thermostat demand-response
event validation system.

Your task is to determine whether the ACTUAL validation error represents
the SAME validation rule as the EXPECTED validation error.

IMPORTANT:
Do NOT judge the messages as merely describing the same general problem,
invalid event, or root cause.

The validation rule itself must match.

For example:

EXPECTED:
"Precool cannot be set for Emergency events."

ACTUAL:
"Emergency events do not support precooling."

These are semantically equivalent because both prohibit precooling
specifically for Emergency events.

However:

EXPECTED:
"Precool cannot be set for Emergency events."

ACTUAL:
"Start time is required."

These are NOT equivalent.

They represent different validation rules.

Another example:

EXPECTED:
"End time must be after start time."

ACTUAL:
"Event duration must be greater than zero."

These may both involve event timing, but they are NOT automatically
equivalent because they validate different fields and different rules.

Evaluate the following:

QUESTION:
{question}

EXPECTED VALIDATION ERROR:
{expected_answer}

ACTUAL VALIDATION ERROR:
{actual_answer}

Evaluate these criteria from 1 to 5:

1. correctness
Does the actual error represent the same validation rule as the expected
error?

2. relevance
Does the actual error address the same validation condition?

3. completeness
Does the actual error preserve the important constraint, field, event type,
and condition from the expected error?

4. hallucination
Does the actual error introduce unsupported information?
5 means no hallucination.

5. overall_score
Overall quality of the semantic match.

SEMANTIC EQUIVALENCE RULES:

A PASS requires that the expected and actual messages refer to the same
validation rule.

Pay particular attention to:

- event type
- field being validated
- condition triggering the validation
- allowed/disallowed behavior
- timing relationship
- numeric constraint
- required vs optional fields

Do NOT mark two messages as equivalent merely because:

- they both indicate an invalid event
- they have a similar root cause
- they concern the same general topic
- they both concern time
- they both concern precooling
- one problem could indirectly cause another problem

If the validation rule is different, the result MUST be FAIL.

PASS only when:
1. The validation rule is semantically equivalent, AND
2. overall_score >= 4.

Return ONLY a JSON object.
Do not use markdown.
Do not use ```json.
Do not include any text before or after the JSON.

The JSON must have exactly these fields:

{{
    "correctness": 1,
    "relevance": 1,
    "completeness": 1,
    "hallucination": 1,
    "overall_score": 1,
    "pass": false,
    "reason": "Brief explanation"
}}
"""

    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.content[0].text.strip()

    print("\nRAW CLAUDE RESPONSE:")
    print(result)

    try:
        evaluation = json.loads(result)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Claude returned invalid JSON: {result}"
        ) from error

    required_fields = {
        "correctness",
        "relevance",
        "completeness",
        "hallucination",
        "overall_score",
        "pass",
        "reason"
    }

    missing_fields = required_fields - evaluation.keys()

    if missing_fields:
        raise ValueError(
            f"Claude response is missing fields: {missing_fields}"
        )

    return evaluation


if __name__ == "__main__":

    question = """
    Emergency event with precool enabled.
    """

    expected_answer = (
        "Precool cannot be set for Emergency events."
    )

    actual_answer = (
        "Emergency events do not support precooling."
    )

    evaluation = evaluate_answer(
        question,
        expected_answer,
        actual_answer
    )

    print("\nEVALUATION:")
    print(json.dumps(evaluation, indent=4))