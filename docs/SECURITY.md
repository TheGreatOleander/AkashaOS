# Security Guidelines

This document outlines best practices for handling sensitive information when working with **AkashaOS**.

## 🔑 Secret Management

- **Do not commit secrets** (tokens, API keys, private keys) into the repository.
- Secrets are already ignored via `.gitignore` (`*.gpg`, `.env`, `.key`, etc.).
- Use a secure storage method for tokens:
  - **Crypto Coffer** (GPG-encrypted file) unlocked manually when needed.
  - OS-native keychain (macOS Keychain, Windows Credential Manager, Linux keyrings).
  - GitHub CLI (`gh auth login`) for safe token management.

## 🔒 Recommended Workflow

1. Store your GitHub token in an encrypted file outside the repo (e.g., `~/.akasha_secrets.gpg`).
2. Unlock it only when needed:
   ```bash
   unlock_akasha
   ```
   This will export the token temporarily to your environment.
3. Never place unencrypted secrets in the repository folder.

## 🛡️ CI / GitHub Actions

- GitHub Actions should use repository **secrets** configured in the repo settings, never hardcoded.
- Access tokens and deployment keys must be rotated regularly.

## 🚨 If a Secret is Leaked

1. **Revoke it immediately** in GitHub → Settings → Developer Settings → Personal Access Tokens.
2. Generate a new token and update your local coffer.
3. Force-push a history rewrite if the secret was committed (use `git filter-repo` or `BFG Repo Cleaner`).

---
By following these practices, we ensure **AkashaOS** stays secure while fostering collaboration.
