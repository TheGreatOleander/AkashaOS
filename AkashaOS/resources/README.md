# AkashaOS — AetherBox (Cloud-ready)

> A living, symbiotic OS for human ↔ AI collaboration — open, modular, and cloud-friendly.
> Hacker eyecandy edition: sleek, visual heartbeat UI + cloud run workflow.

## Quickstart (local)
```bash
unzip AkashaOS_cloudified.zip
cd AkashaOS
docker build -t akashaos:local .
docker run --rm -p 8080:8080 akashaos:local
```

Then visit `http://localhost:8080` to see the heartbeat UI.

## Contribute
- Add modules under `/modules` or `Core`, `Creative_Human` as your persona.
- Use `.env` for secrets. Never commit real keys.
- See `TODO.md` for coding quests to expand AkashaOS.

## Cloud
- The included GitHub Actions workflow will build and run a short container on push to `main` and upload the run log.

## New: Codex, Temple, Veil, Curiosity
- **Codex**: esoteric scrolls + glyph tools.
- **Temple**: debate steps + celestial calendar.
- **Veil**: mentor nudges (coding, crafts) + truths.
- **Curiosity**: sparks + bridges across fields.
