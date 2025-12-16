from types import SimpleNamespace
from typing import Optional

_API_KEY: Optional[str] = None


def configure(api_key: str):
    """Configure the (fallback) generative client with an API key."""
    global _API_KEY
    _API_KEY = api_key


class GenerativeModel:
    """A tiny fallback model implementation used when the official
    `google.generativeai` package is not available.

    It returns a SimpleNamespace with a `text` attribute containing a helpful
    message so the rest of the application continues to work offline.
    """

    def __init__(self, name: str = "fake-model"):
        self.name = name

    def generate_content(self, prompt: str):
        msg = (
            "[local-fallback] GenerativeModel is not installed. "
            "Install the official `google-generativeai` package and set "
            "`GOOGLE_API_KEY` to enable real model responses.\n\n"
            "Prompt received:\n" + (prompt[:1000] + "..." if len(prompt) > 1000 else prompt)
        )
        return SimpleNamespace(text=msg)
