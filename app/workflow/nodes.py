import logging
from pathlib import Path

from app.models.workflow import CoachingWorkflowState
from app.services.llm.base import LLMProvider
from app.services.llm.prompts import build_coaching_prompt
from app.services.tts.base import TTSProvider

logger = logging.getLogger(__name__)


def make_generate_text_node(llm: LLMProvider, max_tokens: int = 2048):
    def generate_text(state: CoachingWorkflowState) -> dict:
        logger.info(
            "Generating coaching text | theme=%s exercises=%d",
            state["theme"],
            len(state["exercises"]),
        )
        messages = build_coaching_prompt(
            exercises=state["exercises"],
            theme=state["theme"],
            duration_hint=state.get("duration_hint", "1 minute 30"),
        )
        prompt = _messages_to_chatml(messages)
        try:
            response = llm.generate(prompt, max_tokens=max_tokens)
            logger.info("Text generated | tokens=%d len=%d", response.tokens_used, len(response.text))
            return {"coaching_text": response.text, "tokens_used": response.tokens_used}
        except Exception as e:
            logger.error("LLM generation failed: %s", e)
            return {"error": f"LLM error: {e}"}

    return generate_text


def make_synthesize_audio_node(tts: TTSProvider):
    def synthesize_audio(state: CoachingWorkflowState) -> dict:
        text = state.get("coaching_text", "")
        if not text:
            return {"error": "No text to synthesize"}

        output_path = state.get("audio_path", Path("/tmp/audiocoach/output.wav"))
        logger.info("Synthesizing audio | text_len=%d output=%s", len(text), output_path)

        try:
            result = tts.synthesize(text, output_path)
            logger.info(
                "Audio synthesized | duration=%.1fs sample_rate=%d",
                result.duration_seconds,
                result.sample_rate,
            )
            return {
                "audio_path": result.audio_path,
                "audio_duration_seconds": result.duration_seconds,
                "sample_rate": result.sample_rate,
            }
        except Exception as e:
            logger.error("TTS synthesis failed: %s", e)
            return {"error": f"TTS error: {e}"}

    return synthesize_audio


def _messages_to_chatml(messages: list[dict[str, str]]) -> str:
    parts = []
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        parts.append(f"<|im_start|>{role}\n{content}<|im_end|>")
    parts.append("<|im_start|>assistant\n")
    return "\n".join(parts)
