# FLARE_SPEC v0.1

Format: `#flare:<name>[?pub=1&meta=...]`

## Fields
- **name**: alphanumeric slug (e.g., cinnamon_rain)
- **pub**: 0/1 (default 0)
- **meta**: optional key=value pairs

## Signed Claims
Optional HMAC or GPG signature when broadcasting across bridges.

## Privacy
- Default: private, stored locally.
- Crossing bridges requires explicit user consent.
