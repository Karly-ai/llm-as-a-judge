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


# Save results
with open("dispatch_evaluation_results.json", "w") as f:
    json.dump(results, f, indent=4)


# Summary
passed = sum(
    1 for result in results
    if result["evaluation"]["pass"]
)

total = len(results)

pass_rate = passed / total * 100


print("\n" + "=" * 70)
print("DISPATCH EVALUATION SUMMARY")
print("=" * 70)

print(f"Passed:   {passed}/{total}")
print(f"Failed:   {total - passed}/{total}")
print(f"Pass Rate: {pass_rate:.1f}%")

print("\nResults saved to:")
print("dispatch_evaluation_results.json")