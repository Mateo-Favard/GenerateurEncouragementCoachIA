import pytest


@pytest.mark.asyncio
async def test_coach_returns_wav(client):
    response = await client.post(
        "/api/v1/coach",
        json={
            "exercises": ["20 jumping jacks", "15 squats"],
            "theme": "pirate",
        },
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/wav"
    # WAV files start with RIFF header
    assert response.content[:4] == b"RIFF"


@pytest.mark.asyncio
async def test_coach_validation_empty_exercises(client):
    response = await client.post(
        "/api/v1/coach",
        json={
            "exercises": [],
            "theme": "pirate",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_coach_validation_missing_theme(client):
    response = await client.post(
        "/api/v1/coach",
        json={
            "exercises": ["20 jumping jacks"],
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_coach_validation_theme_too_short(client):
    response = await client.post(
        "/api/v1/coach",
        json={
            "exercises": ["20 jumping jacks"],
            "theme": "a",
        },
    )
    assert response.status_code == 422
