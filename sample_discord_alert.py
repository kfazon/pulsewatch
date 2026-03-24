"""Send a sample PulseWatch Discord alert using DISCORD_WEBHOOK_URL."""

from __future__ import annotations

import os

from alerts.discord import send_alert


def main() -> None:
    webhook = os.getenv("DISCORD_WEBHOOK_URL", "").strip()
    if not webhook:
        raise SystemExit("DISCORD_WEBHOOK_URL is not set")

    sample_summary = {
        "category": "product",
        "importance": 0.82,
        "summary": "Detected major product page update: new enterprise pricing tier and CTA wording changes.",
    }
    send_alert(webhook_url=webhook, summary=sample_summary, target_url="https://competitor.example.com")
    print("Sample Discord alert sent successfully")


if __name__ == "__main__":
    main()
