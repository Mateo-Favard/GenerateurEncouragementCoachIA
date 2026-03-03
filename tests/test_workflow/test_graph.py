import tempfile
from pathlib import Path

from app.workflow.graph import build_coaching_graph
from tests.conftest import MockLLMProvider, MockTTSProvider


def test_graph_end_to_end():
    llm = MockLLMProvider()
    llm.load()
    tts = MockTTSProvider()
    tts.load()

    graph = build_coaching_graph(llm, tts)

    with tempfile.TemporaryDirectory() as tmp:
        result = graph.invoke({
            "exercises": ["20 jumping jacks", "15 squats"],
            "theme": "pirate",
            "duration_hint": "1 minute 30",
            "audio_path": Path(tmp) / "test.wav",
        })

    assert result.get("error") is None
    assert len(result["coaching_text"]) > 0
    assert result["tokens_used"] > 0
    assert result["audio_duration_seconds"] > 0


def test_graph_with_llm_error():
    """When LLM fails, graph should set error and skip TTS."""

    class FailingLLM(MockLLMProvider):
        def generate(self, prompt, max_tokens=2048):
            raise RuntimeError("LLM crashed")

    llm = FailingLLM()
    llm.load()
    tts = MockTTSProvider()
    tts.load()

    graph = build_coaching_graph(llm, tts)

    result = graph.invoke({
        "exercises": ["test"],
        "theme": "pirate",
    })

    assert result.get("error") is not None
    assert "LLM" in result["error"]
