import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class AIClient:
    """Handles AI calls for improving documentation text."""

    def __init__(self, provider: str = "openai", model: str = "gpt-4o-mini"):
        self.provider = provider
        self.model = model
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY missing in .env")
        self.client = OpenAI(api_key=api_key)

    def improve_doc(self, code: str, draft: str) -> str:
        """Ask the model to rewrite or expand a docstring."""
        prompt = (
            f"You are a concise technical writer.\n\n"
            f"Given this code:\n"
            f"```python\n{code}\n```\n\n"
            f"and its current docstring/summary:\n"
            f'"""{draft}"""\n\n'
            f"Rewrite or expand it into a clear, professional summary (2–4 sentences max).\n"
            f"Return only the improved text, with no extra commentary."
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[AI error] {e}")
            return draft
