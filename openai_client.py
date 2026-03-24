"""Thin OpenAI client wrapper for PulseWatch summarization."""

from __future__ import annotations

import os
import time

from openai import OpenAI, RateLimitError


DEFAULT_MODEL = "stepfun/step-3.5-flash:free"
DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"


def get_api_key() -> str:
    """Return API key from OPENROUTER_API_KEY (preferred) or OPENAI_API_KEY (fallback)."""
    api_key = os.getenv("OPENROUTER_API_KEY", os.getenv("OPENAI_API_KEY", "")).strip()
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY or OPENAI_API_KEY is not set")
    return api_key


def summarize_diff_json(prompt: str, *, api_key: str | None = None, model: str = DEFAULT_MODEL) -> str:
    """Call OpenAI and return raw JSON text response.

    Retries up to 2 additional times on rate limits.
    """
    key = api_key or get_api_key()
    client = OpenAI(api_key=key, base_url=DEFAULT_BASE_URL)

    retries = 2
    for attempt in range(retries + 1):
        try:
            response = client.responses.create(
                model=model,
                input=prompt,
            )
            return response.output_text
        except RateLimitError:
            if attempt >= retries:
                raise
            time.sleep(1 + attempt)

    raise RuntimeError("Unreachable")
