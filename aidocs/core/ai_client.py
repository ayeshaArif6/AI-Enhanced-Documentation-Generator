from typing import Optional

class AIClient:
    """Phase 2: implement LLM calls (OpenAI/Gemini/Claude)."""
    def __init__(self, provider: str = "openai", api_key: Optional[str] = None):
        self.provider = provider
        self.api_key = api_key

    def improve_doc(self, code: str, draft: str) -> str:
        """Return an improved docstring/description from model (stub)."""
        return draft  # no-op for Phase 1
