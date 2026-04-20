# Morning Edition

A daily self-publishing magazine. Every morning at 7am, an agent fetches the front pages of Hacker News and a handful of curated subreddits, picks ten stories matching one reader's taste, writes a short editorial dek on each, and renders them as a single self-contained HTML file with ten distinct editorial spreads (hero, alert-stamp, midnight, academic drop-cap, terminal, swiss poster, typographic collage, newspaper column, manifesto, big-stat finish).

**Live:** [henryblanchard.github.io/morning-edition](https://henryblanchard.github.io/morning-edition/)

Each issue is a static HTML file in `magazines/YYYY-MM-DD.html`. No build step. Fraunces + Inter via Google Fonts. One file, one issue, one shareable URL.

## Stack
- `fetch_stories.py` — dependency-free Python fetcher (Hacker News API + Reddit JSON endpoints)
- A Claude scheduled task fires at 07:00 local, runs the fetcher, curates, designs, writes, commits, and pushes
- GitHub Pages serves the folder at root

## Running by hand

```bash
python3 fetch_stories.py
# then open stories.json, curate 10 stories, render magazines/YYYY-MM-DD.html
```

Built by Henry Blanchard with Claude.
