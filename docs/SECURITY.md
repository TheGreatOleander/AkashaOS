# 🔐 Security Guidelines

Never commit secrets (tokens, passwords, keys) into the repo.  
Use environment variables or secure secret stores instead.

If a secret leaks:
1. Revoke it immediately.  
2. Rotate to a new one.  
3. Report it to maintainers.  

AkashaOS follows a **no-secrets-in-repo** policy.
