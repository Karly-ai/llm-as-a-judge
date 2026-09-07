def validate_event(event):
    errors = []

    event_type = event.get("event_type")
    pre_cool = event.get("pre_cool", False)
    pre_heat = event.get("pre_heat", False)

    # Emergency event validations
    if event_type == "EMERGENCY":

        if pre_cool and pre_heat:
            errors.append(
                "Precool and Preheat cannot be set for Emergency events."
            )

        elif pre_cool:
            errors.append(
                "Precool cannot be set for Emergency events."
            )

        elif pre_heat:
            errors.append(
                "Preheat cannot be set for Emergency events."
            )

    # Time validations
    start_time = event.get("start_time")
    end_time = event.get("end_time")

    if event_type == "SCHEDULED":

        if not start_time:
            errors.append(
                "Start time is required."
            )

        if not end_time:
            errors.append(
                "End time is required."
            )

        if start_time and end_time and end_time <= start_time:
            errors.append(
                "End time must be after start time."
            )

    # Precool timing validation
    pre_cool_start_time = event.get("pre_cool_start_time")

    if pre_cool and event_type == "SCHEDULED":

        if not start_time:
            errors.append(
                "Start time is required for precool."
            )

        elif pre_cool_start_time and pre_cool_start_time > start_time:
            errors.append(
                "Precool cannot start after the event start time."
            )

    # Duration validation
    duration = event.get("duration_minutes")

    if duration is not None and duration <= 0:
        errors.append(
            "Event duration must be greater than zero."
        )

    return errors


if __name__ == "__main__":

    event = {
        "event_type": "SCHEDULED",
        "start_time": "2026-09-05 14:00",
        "end_time": "2026-09-05 16:00",
        "pre_cool": True,
        "pre_heat": False,
        "duration_minutes": 60,
        "pre_cool_start_time": "2026-09-05 15:00"
    }

    errors = validate_event(event)

    print("Event:")
    print(event)

    print("\nValidation Errors:")

    for error in errors:
        print(f"- {error}")