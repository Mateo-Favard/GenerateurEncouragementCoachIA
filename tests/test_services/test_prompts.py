from app.services.llm.prompts import build_coaching_prompt


def test_build_coaching_prompt():
    messages = build_coaching_prompt(
        exercises=["20 jumping jacks", "15 squats"],
        theme="pirate",
        duration_hint="1 minute 30",
    )

    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    assert "pirate" in messages[1]["content"]
    assert "20 jumping jacks" in messages[1]["content"]
    assert "15 squats" in messages[1]["content"]
    assert "1 minute 30" in messages[1]["content"]
