import logging
import re

import httpx

from app.services.llm.base import LLMProvider, LLMResponse

logger = logging.getLogger(__name__)

_OPENROUTER_BASE = "https://openrouter.ai/api/v1"


class OpenRouterProvider(LLMProvider):
    def __init__(
        self,
        api_key: str,
        model: str = "minimax/minimax-01",
        temperature: float = 0.7,
    ):
        self._api_key = api_key
        self._model = model
        self._temperature = temperature
        self._client: httpx.Client | None = None

    def load(self) -> None:
        logger.info("Initializing OpenRouter client | model=%s", self._model)
        self._client = httpx.Client(
            base_url=_OPENROUTER_BASE,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
            timeout=120.0,
        )
        logger.info("OpenRouter client ready")

    def generate(self, prompt: str, max_tokens: int = 2048) -> LLMResponse:
        if not self._client:
            raise RuntimeError("Provider not loaded")

        messages = _chatml_to_messages(prompt)
        resp = self._client.post(
            "/chat/completions",
            json={
                "model": self._model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": self._temperature,
            },
        )
        resp.raise_for_status()
        data = resp.json()

        text = data["choices"][0]["message"]["content"].strip()
        tokens_used = data.get("usage", {}).get("completion_tokens", 0)
        return LLMResponse(text=text, tokens_used=tokens_used)

    def unload(self) -> None:
        if self._client:
            self._client.close()
            self._client = None
            logger.info("OpenRouter client closed")

    @property
    def is_loaded(self) -> bool:
        return self._client is not None


def _chatml_to_messages(prompt: str) -> list[dict[str, str]]:
    messages = []
    for m in re.finditer(r"<\|im_start\|>(\w+)\n(.*?)<\|im_end\|>", prompt, re.DOTALL):
        role, content = m.group(1), m.group(2).strip()
        if role != "assistant":
            messages.append({"role": role, "content": content})
    return messages
