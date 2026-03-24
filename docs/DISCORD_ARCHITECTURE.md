# PulseWatch — Discord Multi-User Architecture

## Overview

PulseWatch uses **per-user Discord webhooks** for digest delivery. Each user configures their own private Discord channel webhook, ensuring complete privacy and team-readiness.

## Design Principles

1. **Privacy-first** — Users only see their own competitor data
2. **Simplicity** — No complex OAuth flows or Discord bot permissions
3. **Team-ready** — Users can invite teammates to their private channel

## Architecture

### Per-User Webhook Model

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│ Landing page│ ──► │ User signup  │ ──► │ Dashboard       │
│ pulsewatch  │     │ + Discord URL│     │ (add targets)   │
│ .top        │     └──────────────┘     └────────┬────────┘
└─────────────┘                                    │
                                                   ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│ Private      │ ◄── │ Discord API  │ ◄── │ Scheduler       │
│ Discord DM   │     │ (webhook)    │     │ (cron daily)    │
│ / Channel    │     └──────────────┘     └────────┬────────┘
└─────────────┘                                    │
                                                   ▼
                                          ┌─────────────────┐
                                          │ Scrape → Diff → │
                                          │ LLM summarize   │
                                          └─────────────────┘
```

### User Flow

1. **Signup** → User registers with email + password (or OAuth)
2. **Connect Discord** → User creates a Discord webhook in their server/channel and pastes URL
3. **Add Targets** → User adds competitor URLs to monitor
4. **Daily Digest** → Our system sends AI-summary to user's webhook

### Discord Webhook Setup (User Experience)

```
1. Open Discord
2. Right-click on your channel → Edit Channel → Integrations
3. Create Webhook → Copy Webhook URL
4. Paste URL in PulseWatch dashboard
5. Done — you now receive daily digests
```

### What Users See

Each user receives a **daily digest** in their configured Discord channel:

```
┌─────────────────────────────────────────────────────┐
│ 🔍 PulseWatch Daily Digest — Mar 24, 2026          │
├─────────────────────────────────────────────────────┤
│                                                     │
│ 📦 competitor-a.com                                │
│ • [PRICING] Removed "20% off" banner               │
│ • [CAREERS] New job: Senior DevOps Engineer         │
│ • Importance: ████████░░ 8/10                      │
│                                                     │
│ 📦 competitor-b.com                                │
│ • [PRODUCT] Added "AI Features" page                │
│ • Importance: ██████░░░░ 6/10                      │
│                                                     │
│ 📊 Your monitored: 5 targets | Changes today: 2    │
│                                                     │
│ 👆 View full report → pulsewatch.top/dashboard     │
└─────────────────────────────────────────────────────┘
```

## Privacy Model

| Data | Visible To |
|------|------------|
| Competitor URLs | User only |
| Change summaries | User only |
| Daily digests | User only |
| Team invites | User + invited members |

**PulseWatch team NEVER sees user data.**

## Database Schema (Conceptual)

```sql
users (
  id,
  email,
  password_hash,
  created_at
)

user_discord_webhooks (
  id,
  user_id,
  webhook_url,        -- encrypted
  webhook_name,       -- e.g., "#marketing-competitors"
  created_at
)

monitoring_targets (
  id,
  user_id,
  url,
  label,
  last_checked,
  last_change,
  created_at
)

change_logs (
  id,
  target_id,
  change_summary,
  importance_score,
  detected_at
)
```

## Security Considerations

1. **Webhook URLs encrypted at rest** — AES-256
2. **No Discord bot required** — Uses Discord's built-in webhook API
3. **Rate limiting** — Max 1 digest per user per day (configurable)
4. **Data isolation** — Row-level security in database

## Implementation Notes

### Discord Webhook API

```python
import requests

def send_digest(webhook_url: str, digest: dict):
    payload = {
        "embeds": [{
            "title": f"🔍 PulseWatch Daily — {digest['date']}",
            "description": digest['summary'],
            "color": 5814783,  # Blue
            "fields": [
                {"name": t['label'], "value": t['changes'], "inline": True}
                for t in digest['targets']
            ],
            "footer": {"text": "PulseWatch — Never miss a move"}
        }]
    }
    requests.post(webhook_url, json=payload)
```

### Webhook URL Validation

```python
import re

def is_valid_discord_webhook(url: str) -> bool:
    pattern = r'^https://discord(?:(?:app)?\.com/api)?/webhooks/\d+/.+$'
    return bool(re.match(pattern, url))
```

## Alternatives Considered

| Approach | Pros | Cons |
|----------|------|------|
| **Per-user webhook (chosen)** | Simple, private, no OAuth | User must create webhook |
| Discord OAuth bot | Native Discord experience | Complex auth, permission issues |
| Email → Discord bridge | Familiar | Loses real-time, extra step |
| Shared community server | Community building | Privacy concerns |

## FAQ

**Q: What if user doesn't have a Discord server?**  
A: They can create a free personal server in < 1 minute.

**Q: Can teammates see the same digest?**  
A: Yes — add them to the Discord channel with the webhook. They all see the same digest.

**Q: How do we prevent webhook abuse?**  
A: Webhooks are per-user, rate-limited, and URLs are encrypted.

**Q: What about enterprise users with no Discord?**  
A: Email digest option available as future tier (not MVP).

---

*Architecture v1.0 — 2026-03-24*
