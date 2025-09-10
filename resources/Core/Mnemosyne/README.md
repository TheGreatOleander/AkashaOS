# Knowledge Spiral v0.9

A local-first, privacy-minded prototype for a human ⇄ AI **Knowledge Spiral**:
- Capture ideas, questions, proposals
- Auto-structure with simple NLP (keywords/intents)
- Link related ideas in a force-directed graph
- Per-node voting (benefit / effort / risk) -> consensus score
- Export/import room JSON to share or back up

## Quickstart (dev)

Requirements: Node 18+ and npm.

1. Install:
```bash
npm install
```

2. Dev server:
```bash
npm run dev
```
Open the printed `localhost` URL.

3. Build:
```bash
npm run build
npm run preview
```

## Notes
- This is a minimal Vite React prototype. For production:
  - Add real UI components (shadcn/ui or MUI) and Tailwind CSS build.
  - Optionally integrate Yjs for CRDT real-time sync.
  - Sanitize exported JSON before sharing if you need to remove voter IDs.

## Files of interest
- `src/KnowledgeSpiral.jsx` — main component (graph, ledger, voting)
- `src/App.jsx` — mounts the component
- `index.html`, `vite.config.js`, `package.json` — project scaffolding

