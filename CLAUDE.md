# Morning Edition

A daily self-publishing magazine. Each morning at 7am a scheduled Claude task fetches Hacker News + Reddit, curates 10 stories matching Henry's taste, designs a single self-contained HTML magazine with 10 distinct editorial spreads, saves it to `magazines/YYYY-MM-DD.html`, and pushes to GitHub Pages.

## Stack
- Plain HTML (one file per issue, self-contained — fonts via Google Fonts CDN)
- Python 3 `fetch_stories.py` for data gathering
- Scheduled daily at 7am local time via `scheduled-tasks` MCP
- Hosted on GitHub Pages (repo: `henryblanchard/morning-edition`)

## Henry's taste (the curation brief)
Lean IN: AI tools/releases, internal lab progress toward AGI, maths/physics, creative software, weird science, anything directly actionable for an entrepreneur/educator building AI courses.

Lean OUT: US/UK party politics, culture-war drama, crypto price chatter, celebrity gossip.

Flag with 🎯 any story directly applicable to Henry's work: GWAI cohorts, AI education, founder tooling, no-code/automation, course design, financial advice, workshops.

## File layout
```
morning-edition/
├── CLAUDE.md               # this file
├── fetch_stories.py        # fetches HN + Reddit → stories.json
├── stories.json            # temp data, regenerated each morning
├── index.html              # archive landing page
├── magazines/              # daily issues
│   └── YYYY-MM-DD.html
└── .gitignore
```

## Design brief (for each issue)
- Fraunces (display) + Inter (body), both from Google Fonts
- 10 stories, each a distinct full-viewport editorial spread
- Spread types to rotate through: hero cover, dark/midnight, rose-alert-stamp, terminal, academic drop-cap, big-stat finish, swiss poster, newspaper column, typographic collage, manifesto
- Every spread has a different background colour + numeral treatment
- No font below 18px anywhere. Body copy 20–24px, display type 80–400px
- Self-contained in one HTML file (embedded CSS, no local assets)
- Each story includes: number, headline, dek/blurb (Claude-written editorial summary — NOT the raw title), source + link, 🎯 flag if applicable

## How the daily task runs
See `/Users/henryblanchard/.claude/scheduled-tasks/morning-edition/SKILL.md` for the full prompt that fires at 7am.

Flow:
1. `python3 fetch_stories.py` → `stories.json` (HN top 30 + 5 curated subreddits)
2. Read `stories.json`, curate 10 per taste brief
3. Design + write `magazines/YYYY-MM-DD.html`
4. Update `index.html` to list the new issue at the top
5. `git add`, `git commit`, `git push` → Pages redeploys in ~1 min

## Live URL
https://henryblanchard.github.io/morning-edition/
