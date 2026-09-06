from app.dispatch_validator import validate_event


def test_emergency_event_cannot_use_precool():
    event = {
        "event_type": "EMERGENCY",
        "pre_cool": True,
        "pre_heat": False
    }

    errors = validate_event(event)

    assert "Precool cannot be set for Emergency events." in errors


def test_emergency_event_cannot_use_preheat():
    event = {
        "event_type": "EMERGENCY",
        "pre_cool": False,
        "pre_heat": True
    }

    errors = validate_event(event)

    assert "Preheat cannot be set for Emergency events." in errors


def test_emergency_event_cannot_use_precool_and_preheat():
    event = {
        "event_type": "EMERGENCY",
        "pre_cool": True,
        "pre_heat": True
    }

    errors = validate_event(event)

    assert (
        "Precool and Preheat cannot be set for Emergency events."
        in errors
    )


def test_scheduled_event_requires_start_time():
    event = {
        "event_type": "SCHEDULED",
        "start_time": None,
        "end_time": "2026-09-05 14:00"
    }

    errors = validate_event(event)

    assert "Start time is required." in errors


def test_scheduled_event_requires_end_time():
    event = {
        "event_type": "SCHEDULED",
        "start_time": "2026-09-05 13:00",
        "end_time": None
    }

    errors = validate_event(event)

    assert "End time is required." in errors


def test_end_time_must_be_after_start_time():
    event = {
        "event_type": "SCHEDULED",
        "start_time": "2026-09-05 14:00",
        "end_time": "2026-09-05 13:00"
    }

    errors = validate_event(event)

    assert "End time must be after start time." in errors


def test_zero_duration_is_invalid():
    event = {
        "event_type": "SCHEDULED",
        "start_time": "2026-09-05 13:00",
        "end_time": "2026-09-05 14:00",
        "duration_minutes": 0
    }

    errors = validate_event(event)

    assert "Event duration must be greater than zero." in errors


def test_negative_duration_is_invalid():
    event = {
        "event_type": "SCHEDULED",
        "start_time": "2026-09-05 13:00",
        "end_time": "2026-09-05 14:00",
        "duration_minutes": -30
    }

    errors = validate_event(event)

    assert "Event duration must be greater than zero." in errors