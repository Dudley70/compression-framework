# Already Compressed Test Case

## Original Document (Already Compressed)

Auth API: JWT tokens, bcrypt hash, rate limits.

Endpoints:
- /auth: login/logout
- /users: CRUD ops
- /admin: mgmt panel

Config: DB_URL, SECRET_KEY, OAuth settings.

Security: MFA, encryption, logging.

## "Compressed" Version (Attempted Further Compression)

Auth: JWT, bcrypt, limits.

Routes:
- /auth: login
- /users: ops
- /admin: panel

Config: URLs, keys, OAuth.

Security: MFA, encrypt, logs.

## Expected Results

- **Pre-check**: FAIL (original score ≥ 0.8 - already compressed)
- **Entity Preservation**: N/A (pre-check failure stops processing)
- **Minimal Benefit**: N/A (pre-check failure)
- **Semantic Similarity**: N/A (pre-check failure)
- **Overall**: REFUSE (already compressed, refuse before attempting further compression)