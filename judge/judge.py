import json
import os

from dotenv import load_dotenv
from anthropic import Anthropic


load_dotenv()

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)


def evaluate_answer(question, expected_answer, actual_answer):

    prompt = f"""
You are an expert QA evaluator judging an AI customer-support chatbot.

Evaluate the chatbot response.

QUESTION:
{question}

EXPECTED ANSWER:
{expected_answer}

ACTUAL ANSWER:
{actual_answer}

Evaluate these criteria from 1 to 5:

1. correctness
Does the response provide accurate information?

2. relevance
Does the response directly answer the customer's question?

3. completeness
Does the response contain the important information from the expected answer?

4. hallucination
Does the response introduce unsupported information?
5 means no hallucination.

5. overall_score
Overall quality of the response.

PASS/FAIL:
Pass if overall_score >= 4.
Fail if overall_score < 4.

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

    return json.loads(result)


if __name__ == "__main__":

    question = "How long does standard shipping take?"

    expected_answer = (
        "Standard shipping takes 5-7 business days."
    )

    actual_answer = (
        "Standard shipping takes 2-3 business days."
    )

    evaluation = evaluate_answer(
        question,
        expected_answer,
        actual_answer
    )

    print("\nEVALUATION:")
    print(json.dumps(evaluation, indent=4))