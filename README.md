# StockVision AI V2 (zero-budget static research tool)

## What works
- Search India NSE and US NASDAQ/NYSE company directories (best-effort; incomplete coverage possible).
- Company profile with source link; optional dated price snapshot; no fabricated live prices.
- Local-only financial CSV import and Revenue CAGR, Profit CAGR, ROE, P/E, Debt/Equity calculations.
- GitHub Actions refreshes public symbol directories daily (best effort).

## Deploy to existing GitHub Pages repository
1. Back up the existing repository. Upload **contents of this ZIP** to repository root (not the containing folder). Merge with existing files; ensure `index.html`, `app.js`, `scripts/`, `data/`, `.github/workflows/deploy.yml` are in root.
2. In Settings > Pages, choose GitHub Actions.
3. In `.github/workflows/`, **disable/delete old `static.yml` and `jekyll-docker.yml` workflows** so only `deploy.yml` publishes Pages. Prefer a separate branch/backup first.
4. Commit. Actions > StockVision V2 Deploy > Run workflow if needed.
5. When green, open `https://USERNAME.github.io/REPO/`.

## Data sources and limits
- US symbol lists: NASDAQ Trader official directories, refreshed periodically. These include exchange-listed securities, not necessarily every operating company.
- India NSE: NSE archived equity CSV; can fail due to network restrictions. BSE-only stocks are **not** covered.
- No real-time or delayed price feed is included. `data/quotes.json` is intentionally empty until an authorized provider supplies data with display rights. Quote object example: `{"quotes":{"US:AAPL":{"price":123.45,"currency":"$","asof":"2026-10-25T15:00:00Z","provider":"Licensed feed"}}}`. Only publish quotes if licensing permits redistribution.
- No paid AI model, automated financial-statement ingestion, or investment recommendations. Financials are supplied by users in CSV. Financial ratios assume consistent units; simplified ROE uses ending equity.
- Upstream data may be stale, partial or inaccessible; scheduled Actions are best effort and may be delayed.

## Testing
`python3 scripts/update_directory.py` to refresh symbol list when network access is available. Run `python3 -m http.server 8000` in this folder and open http://localhost:8000/.
