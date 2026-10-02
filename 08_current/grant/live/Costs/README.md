# Finance costing (source of truth)

**File:** `Budget 02 10 26 IPA 799 v2.xlsx` (Finance export, 2 October 2026).

This folder holds the institutional spreadsheet only. JeS narrative figures in `../06_Resources_and_Costs.md`, `../03_Applicant_and_Team_Capability.md` (Resources and delivery paragraph), and `../TIMELINE.md` must match this file after every Finance revision.

## Sync after a new spreadsheet

From `08_current/grant/live/Costs/`:

```bash
python3 extract_jes_totals.py "Budget 02 10 26 IPA 799 v2.xlsx"
```

Paste the printed staff table and totals into `06_Resources_and_Costs.md`, then update the **Resources and delivery (JeS)** sentence in `03_Applicant_and_Team_Capability.md` and the cost lock line in `TIMELINE.md`.

**Superseded:** `Budget 26 08 26 INF799 v3.xlsx` (August 2026).
