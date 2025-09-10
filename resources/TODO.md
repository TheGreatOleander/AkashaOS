# TODO.md — AkashaOS Coding Quests ⚔️

## Core Foundations
- [ ] **Module Loader** → Python script that scans `/modules` and auto-imports detected files.
- [ ] **Config Manager** → Replace hard-coded tokens with `.env` + loader.
- [ ] **Bootstrap Script** → Unified `akasha init` to set up environment, install deps, and guide user.

## Human ↔ AI Symbiosis
- [ ] **Lore ↔ Code Bridge** → Parse `.md` lore files into structured config (so mythology drives function).
- [ ] **Conversation Memory** → SQLite/Postgres-backed journal for storing chats, ideas, and decisions.
- [ ] **Story-Driven Config** → Natural-language `.md` configs that are machine-readable.

## API & Sensor Array
- [ ] **Weather Sensor** → Simple script to fetch real-time weather API.
- [ ] **GitHub Whisperer** → Module that watches repo events and “narrates” them.
- [ ] **System Pulse** → Local CPU/memory monitoring exposed as AkashaOS “vitals.”
- [ ] **IoT Listener** → Basic MQTT or HTTP listener for sensors.

## AI Collectives
- [ ] **Model Router** → Central function that delegates tasks to different LLMs (OpenAI, local, etc.).
- [ ] **Consensus Mode** → Multiple archetypes give responses, merged into one output.
- [ ] **Dream Logs** → Save AI outputs as `.md` journals → future runs can reuse them.

## Growth & Symbiosis
- [ ] **Plugin Creator** → CLI tool (`akasha new module`) scaffolds a new organ.
- [ ] **Web Portal** → GitHub Pages site that renders lore + docs beautifully.
- [ ] **Contribution Ritual** → Template for PRs framed as mythos additions.
