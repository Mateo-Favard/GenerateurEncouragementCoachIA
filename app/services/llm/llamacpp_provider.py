import logging

from llama_cpp import Llama

from app.services.llm.base import LLMProvider, LLMResponse

logger = logging.getLogger(__name__)


class LlamaCppProvider(LLMProvider):
    def __init__(
        self,
        model_path: str,
        n_ctx: int = 4096,
        n_threads: int = 4,
        temperature: float = 0.7,
    ):
        self._model_path = model_path
        self._n_ctx = n_ctx
        self._n_threads = n_threads
        self._temperature = temperature
        self._model: Llama | None = None

    def load(self) -> None:
        logger.info("Loading LLM model from %s", self._model_path)
        self._model = Llama(
            model_path=self._model_path,
            n_ctx=self._n_ctx,
            n_threads=self._n_threads,
            verbose=False,
        )
        logger.info("LLM model loaded successfully")

    def generate(self, prompt: str, max_tokens: int = 2048) -> LLMResponse:
        if not self._model:
            raise RuntimeError("Model not loaded")

        result = self._model(
            prompt,
            max_tokens=max_tokens,
            temperature=self._temperature,
            stop=["<|im_end|>", "<|im_start|>"],
        )

        text = result["choices"][0]["text"].strip()
        text = self._clean_output(text)
        tokens_used = result["usage"]["completion_tokens"]
        return LLMResponse(text=text, tokens_used=tokens_used)

    @staticmethod
    def _clean_output(text: str) -> str:
        import re

        # Remove Qwen3 <think>...</think> blocks
        text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
        # Remove any remaining XML-like tags
        text = re.sub(r"<[^>]+>", "", text)
        # Remove markdown artifacts: **, *, #, -, bullet points
        text = re.sub(r"\*{1,2}", "", text)
        text = re.sub(r"^#{1,4}\s+", "", text, flags=re.MULTILINE)
        text = re.sub(r"^\s*[-•]\s+", "", text, flags=re.MULTILINE)
        text = re.sub(r"^\s*\d+[\.\)]\s+", "", text, flags=re.MULTILINE)
        # Remove bracketed stage directions [applause], (pause), etc.
        text = re.sub(r"\[.*?\]", "", text)
        text = re.sub(r"\(.*?\)", "", text)
        # Collapse whitespace
        text = re.sub(r"\n{2,}", "\n", text)
        text = re.sub(r"  +", " ", text)
        return text.strip()

    def unload(self) -> None:
        if self._model:
            del self._model
            self._model = None
            logger.info("LLM model unloaded")

    @property
    def is_loaded(self) -> bool:
        return self._model is not None
