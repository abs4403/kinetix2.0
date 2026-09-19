# KINETIX

Strength training and yoga in one place, with a built-in calorie meter.

- **Gym** — ten foundational exercises across the major muscle groups, each with coaching cues and a real demo video. Modern, dark, high-contrast design.
- **Yoga** — ten full-body asanas with Sanskrit names, benefits, and guided videos. Warm parchment, serif type, old practice-journal feel.
- **Calorie Meter** — a daily-needs calculator (Mifflin-St Jeor BMR/TDEE) and a session-burn calculator (MET-based), both reachable from the pill button in the top bar on every page.

## Tech stack

- **Backend:** Python 3 + Flask — renders the pages from JSON data files and exposes a small JSON API (`/api/exercises`, `/api/yoga`, `/api/bmr`, `/api/burn`, `/api/history`).
- **Frontend:** plain HTML (Jinja2 templates), CSS, and vanilla JavaScript — no build step, no frameworks.
- **Data:** `data/exercises.json` and `data/yoga.json` hold the exercise/pose libraries; `data/history.json` is created automatically to log calorie-meter entries.

## Project structure

```
kinetix/
├── app.py                  # Flask app: routes + JSON API
├── requirements.txt
├── data/
│   ├── exercises.json      # gym exercise library
│   └── yoga.json           # yoga pose library
├── templates/
│   ├── base.html           # shared shell: fonts, top bar, footer
│   ├── index.html          # landing page (split gym/yoga hero)
│   ├── gym.html
│   ├── yoga.html
│   └── calorie.html
└── static/
    ├── css/
    │   ├── base.css         # shared tokens + top bar
    │   ├── home.css
    │   ├── gym.css
    │   ├── yoga.css
    │   └── calorie.css
    └── js/
        ├── main.js               # category/focus filtering
        ├── video-modal.js        # gym video lightbox
        ├── yoga-video-modal.js   # yoga video lightbox
        └── calorie.js            # calculator logic + gauges
```

## Running locally

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

## Putting this on GitHub

```bash
git init
git add .
git commit -m "Initial commit: KINETIX"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

**Note on hosting:** this is a Flask (Python) app, so plain GitHub Pages — which only serves static files — won't run it. To make it live on the web, deploy it to a host that runs Python, such as Render, Railway, PythonAnywhere, or Fly.io (all have free tiers and a "deploy from GitHub repo" flow). If you specifically want something that lives on GitHub Pages, you'd need to pre-render the HTML and drop the Python API (the calculators would need to move entirely into `calorie.js`, which already has a client-side fallback for exactly this case).

## Editing the exercise/pose libraries

Add, remove, or edit entries directly in `data/exercises.json` / `data/yoga.json`. Each entry needs a YouTube `video_id` (the string after `v=` in a YouTube URL) — thumbnails and embeds are generated from that automatically, so there's nothing else to wire up.

## Credits

Demo video links point to their original creators on YouTube (channels including ATHLEAN-X, Buff Dudes, NASM, Bowflex, and Yoga With Adriene). This project doesn't host or claim ownership of that video content — it links out to it.
