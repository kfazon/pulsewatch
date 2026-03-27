# SECRETS.md — .env Variable Registry (no values)

## Purpose
Single source of truth for which `.env` variables exist, what they do, and how to rotate them.

## Rules
- Never store secret VALUES in git or docs.
- Only record variable names + meaning.

## Registry
| env_var | description | where used | how to obtain | rotation / expiry | owner |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Rotation checklist
- Update `.env` on target environment
- Restart service if needed
- Verify via health check
- Update evidence (task report)
