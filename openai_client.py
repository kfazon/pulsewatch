"""Thin OpenAI client wrapper for PulseWatch summarization."""

from __future__ import annotations

import os
import time

from openai import OpenAI, RateLimitError


DEFAULT_MODEL = "gpt-4o-mini"


def get_api_key() -> str:
    """Return OPENAI_API_KEY from environment or raise a clear error."""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set")
    return api_key


def summarize_diff_json(prompt: str, *, api_key: str | None = None, model: str = DEFAULT_MODEL) -> str:
    """Call OpenAI and return raw JSON text response.

    Retries up to 2 additional times on rate limits.
    """
    key = api_key or get_api_key()
    client = OpenAI(api_key=key)

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
