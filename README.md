# Paws in the Park — game, support and privacy

Static Russian and English pages for the Paws in the Park iOS beta.

Public routes:
- `/`: Russian game and support page
- `/en/`: English game and support page
- `/privacy/`: Russian privacy policy
- `/en/privacy/`: English privacy policy
- `/editor/`: browser park editor (Russian interface), templates and `.potlevel` import/export

Edit `content/site.json`, `content/ru.json` and `content/en.json`; run `python3 scripts/build.py`. Only an owner-approved email may be added. When it is empty, the site provides GitHub issue and TestFlight feedback routes; no example address is published.

Preview with `python3 -m http.server 8770 --bind 127.0.0.1 --directory docs`. GitHub Pages publishes `main → /docs`. The TestFlight link must be a real public invitation for the external test group. Review status in the site configuration must match Apple; availability is not claimed while the beta is awaiting approval.

The template and navigation follow the existing `travinov/llmdict-support` project. Text, app icon and paper/park colors are specific to Paws in the Park. This repository contains website files only; no game source, player data, credentials, signing files or internal invitations.

The support pages use no external fonts, analytics, forms, cookies or localStorage. The email-copy control is a progressive enhancement; links and navigation work without JavaScript. The editor needs JavaScript and saves maps and imported images locally in IndexedDB/localStorage. It does not upload them; moving to another origin requires `.potlevel` export/import.

Build the editor from the private game workspace with `python3 distribution/github-pages/build_editor.py` (from its root). This runs the TypeScript check and Vite production build with base `/piss-on-trees-support/editor/`, copies only the public build into `PublicSite/docs/editor/`, and records SHA-256 hashes in `release-manifest.json`. The public repository does not require Node at runtime. Publish the reviewed changes to `main`; the existing Pages source remains `/docs`.
