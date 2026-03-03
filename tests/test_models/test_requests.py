import pytest
from pydantic import ValidationError

from app.models.requests import CoachingRequest


def test_valid_request():
    req = CoachingRequest(
        exercises=["20 jumping jacks", "15 squats"],
        theme="pirate",
    )
    assert req.duration_hint == "1 minute 30"


def test_empty_exercises():
    with pytest.raises(ValidationError):
        CoachingRequest(exercises=[], theme="pirate")


def test_theme_too_short():
    with pytest.raises(ValidationError):
        CoachingRequest(exercises=["test"], theme="a")


def test_too_many_exercises():
    with pytest.raises(ValidationError):
        CoachingRequest(exercises=[f"ex{i}" for i in range(11)], theme="pirate")
