# StockVision AI — ₹0 Public Beta

A real deployable, **static** financial-analysis website for GitHub Pages. No paid API, server, database, user account or AI service required. Source code is MIT-style usable by the owner; no external market dataset redistribution is bundled.

## Features
- Responsive English/Marathi interface, sample fictional company, browser CSV import.
- Revenue / profit CAGR, profit YoY, ROE, EPS, manual-price P/E, debt/equity, operating cash flow, free cash flow.
- Rule-based risk observations, SVG history chart, year-by-year source links.
- Local-only import (no upload), input validation, HTTPS source URL enforcement, no `innerHTML` injection.
- Tests and GitHub Pages deployment workflow.

## Run locally
Requires Python 3 or Node.js 20+.

```bash
python -m http.server 8000 --directory site
# open http://localhost:8000
```

To test:
```bash
npm test
```

## Publish free on GitHub Pages
1. Create a **public GitHub repository** (e.g. `stockvision-ai`).
2. Upload **all files and folders** in this project, including `.github/workflows/deploy.yml`, to the repository's `main` branch.
3. In repository **Settings → Pages**, choose **GitHub Actions** as build/deployment source.
4. Open **Actions** and confirm the deploy workflow succeeded. Site URL will typically be `https://YOUR-USERNAME.github.io/stockvision-ai/`.
5. Replace `site/data/DEMO.csv` or add other **licensed or permission-cleared** CSVs. The default selector includes DEMO only; adding multiple preset companies requires editing `site/index.html` and loading the matching path in `site/app.js`. Users can already import any properly formatted CSV locally.

## Data contract
`year,revenue,profit,debt,equity,operating_cash_flow,capex,shares,source_url`
All financial amounts are **₹ crore**, shares are **crore shares**; one source URL per financial year. At least two years, max 30, positive equity and shares, and HTTPS URLs. Use **consistent annual consolidated vs standalone basis**. User is responsible for source accuracy, restatements, stock splits, units, and permissions.

## What this is NOT
- No live stock quotes, licensed market feed, automatic company data collection, real AI model, fair value, ROCE, buy/sell calls, login, user storage, or automatic IPO updates.
- `DEMO` is fictional and must never be mistaken for a real listed company.
- This is an **educational beta**, not verified financial advice or SEBI-registered research.

## Public launch checklist
- Obtain rights to distribute any datasets or market prices; do not scrape/republish third-party commercial data without permission.
- Add contact details, privacy notice, terms and limitations before broad promotion; if adding analytics/cookies, disclose appropriately.
- Have an India-qualified compliance professional review any future paid stock research, buy/sell ratings, personalized advice or subscriptions.
- Verify all financial numbers and data freshness; identify original exchange filings and correction procedures.
- For real AI, use a **server-side** API gateway and usage limits. Never embed an OpenAI API key in browser code or a public repository.

## Why static hosting?
GitHub Pages hosts static sites at zero incremental infrastructure cost for eligible repositories, subject to GitHub's limits and terms. This is a real public website, not a promise of free unlimited financial-data APIs or AI inference. GitHub Pages suitability for a commercial SaaS should be rechecked before monetization.
