import json

from app.dispatch_validator import validate_event
from judge.judge import evaluate_answer


# Load Dispatch test cases
with open("data/dispatch_test_cases.json", "r") as f:
    test_cases = json.load(f)


results = []

for test_case in test_cases:

    test_id = test_case["id"]
    expected_error = test_case["expected_error"]

    # Validate event
    errors = validate_event(test_case)

    # Get the first actual validation error
    if errors:
        actual_error = errors[0]
    else:
        actual_error = "No validation error."

    # Ask Claude to evaluate the error message
    evaluation = evaluate_answer(
        question=f"Validate this Dispatch event configuration: {test_case}",
        expected_answer=expected_error,
        actual_answer=actual_error
    )

    result = {
        "id": test_id,
        "event": test_case,
        "expected_error": expected_error,
        "actual_error": actual_error,
        "evaluation": evaluation
    }

    results.append(result)

    print("\n" + "=" * 70)
    print(f"Test Case: {test_id}")
    print(f"Expected: {expected_error}")
    print(f"Actual:   {actual_error}")
    print(f"Score:    {evaluation['overall_score']}")
    print(f"Pass:     {evaluation['pass']}")


# Save detailed results
with open("dispatch_evaluation_results.json", "w") as f:
    json.dump(results, f, indent=4)


# --------------------------------------------------
# Judge performance metrics
# --------------------------------------------------

true_positives = 0
true_negatives = 0
false_positives = 0
false_negatives = 0

for result in results:

    test_id = result["id"]
    judge_pass = result["evaluation"]["pass"]

    # Cases 1-16 and 22-34 are designed to PASS.
    # Cases 17-21 and 35-50 are deliberately designed to FAIL.
    expected_pass = (1 <= test_id <= 16) or (22 <= test_id <= 34)

    if expected_pass and judge_pass:
        true_positives += 1

    elif not expected_pass and not judge_pass:
        true_negatives += 1

    elif not expected_pass and judge_pass:
        false_positives += 1

    elif expected_pass and not judge_pass:
        false_negatives += 1


total = len(results)

correct_predictions = true_positives + true_negatives

accuracy = correct_predictions / total * 100


print("\n" + "=" * 70)
print("LLM JUDGE PERFORMANCE")
print("=" * 70)

print(f"Total Cases:       {total}")
print(f"True Positives:    {true_positives}")
print(f"True Negatives:    {true_negatives}")
print(f"False Positives:   {false_positives}")
print(f"False Negatives:   {false_negatives}")
print(f"Judge Accuracy:    {accuracy:.1f}%")

# CI quality gate
minimum_accuracy = 95.0

if accuracy < minimum_accuracy:
    print(
        f"\nCI FAILED: Judge accuracy {accuracy:.1f}% "
        f"is below the required {minimum_accuracy:.1f}%."
    )
    raise SystemExit(1)

print(
    f"\nCI PASSED: Judge accuracy {accuracy:.1f}% "
    f"meets the required {minimum_accuracy:.1f}%."
)