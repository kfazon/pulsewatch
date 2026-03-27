# ACCESS.md — Environment Access (no secrets)

## Purpose
How to access environments (local/VPS), where `.env` lives, and how to troubleshoot access.

## Environments
### Local
- Repo path: 
- `.env` path: 

### VPS / Server
- Host/IP: (allowed)
- SSH user: (allowed)
- SSH port: (allowed)
- SSH method: key-based (never paste private keys)
- Connect command example:
  - `ssh <user>@<host> -p <port>`

## .env policy
- Secrets live in `.env` files only.
- `.env` must be gitignored.
- Document required variable NAMES in `docs/SECRETS.md`.

## Troubleshooting
- Common SSH errors + fixes
- Where logs live
