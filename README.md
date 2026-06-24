# PAT Financial Explorer

Interactive treemap / YoY-compare / searchable-table explorer for กทท.'s consolidated financial data (FY2568–FY2569), inspired by [budget-explorer.peoplesparty.or.th](https://budget-explorer.peoplesparty.or.th).

Standalone HTML — no backend, no build step. Same PIN-gate as [PAT Fintrix](https://github.com/PDEE-Hub/Dashboard-Financial-69).

## Files

- `index.html` — the dashboard (open directly, or serve via GitHub Pages)
- `pat_data.js` — aggregated data, loaded by `index.html`
- `build_data.py` — regenerates `pat_data.js` from `../Financial Dashboard/Power BI_8 Months_69.xlsx` whenever the source Excel is refreshed

## Data scope

- Entities: `กทท.` (whole-org consolidated book), `ทกท.`/`ทลฉ.`/`ทรน.`/`ทชส.` (per-port books, compared side-by-side, not summed into กทท.'s total — see note in `build_data.py`)
- Years: FY2568 (full 12 months) + FY2569 (8 months, through พฤษภาคม)

## Updating monthly

1. Refresh `../Financial Dashboard/Power BI_8 Months_69.xlsx`
2. `python3 build_data.py` — regenerates `pat_data.js` and prints a sanity-check of net profit by entity
3. Commit + push both files
