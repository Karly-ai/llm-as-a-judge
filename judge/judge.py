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
You are an expert QA engineer evaluating validation error messages
for a smart thermostat demand-response event configuration system.

Your job is to determine whether the ACTUAL validation error is
semantically equivalent to the EXPECTED validation error.

Do NOT require the wording to be identical.

For example:

EXPECTED:
"Precool cannot be set for Emergency events."

ACTUAL:
"Emergency events do not support precooling."

These mean the same thing and should PASS.

However:

EXPECTED:
"Precool cannot be set for Emergency events."

ACTUAL:
"Precool duration must be greater than zero."

These describe different validation rules and should FAIL.

Consider the meaning of the validation rule, not just matching words.

QUESTION / EVENT:
{question}

EXPECTED VALIDATION ERROR:
{expected_answer}

ACTUAL VALIDATION ERROR:
{actual_answer}

Evaluate the ACTUAL validation error using these criteria.

1. correctness
Does the actual error represent the same validation rule as the expected error?

2. relevance
Does the actual error relate directly to the event configuration?

3. completeness
Does the actual error communicate the important constraint expressed
by the expected error?

4. hallucination
Does the actual error introduce unsupported or unrelated information?
5 means no hallucination.

5. overall_score
Give an overall quality score from 1 to 5.

PASS/FAIL RULE:
Pass ONLY when the actual error is semantically equivalent to the
expected error and overall_score is at least 4.

Return ONLY valid JSON.

Do not use markdown.
Do not use ```json.
Do not include text before or after the JSON.

The JSON must contain exactly these fields:

{{
    "correctness": 1,
    "relevance": 1,
    "completeness": 1,
    "hallucination": 1,
    "overall_score": 1,
    "pass": true,
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