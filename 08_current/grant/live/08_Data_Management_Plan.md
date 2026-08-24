# DATA MANAGEMENT PLAN

Aligned to `VA_230826_reconstructed.docx` §5 and §7. Sharing dates follow `TIMELINE.md`.

## Data types and volumes

**Input (restricted).** Championship broadcast tracking and tactical labels for ~540 matches, via the Swansea City AFC–StatsBomb agreement. CSV/JSON positional coordinates. Raw volume ~50–100 GB.

**Generated (project).** At 1 Hz the pipeline writes barcodes, persistence landscapes and vectorised summaries per scale (§8). Season-scale processing is ~1,600 CPU-hours of the 5,000-hour Supercomputing Wales allocation. Per-match archives (compressed), not one JSON file per historical 150-frame subsample. Derived volume ~20–40 GB plus figures.

**Code.** Containerised Python (Ripser, GUDHI, giotto-tda); version-controlled.

## Storage and backup

During the award: institutional research storage (daily backup), encrypted working copies, Git for code. Long-term: institutional repository (10+ years); Zenodo DOI for software and permitted aggregates; GitHub for the public codebase.

## What can be shared

| Asset | Access | Date |
|---|---|---|
| OSF pre-registration (O1/O2 plan) | Public | **Month 2** |
| Containerised pipeline (Apptainer/Docker) | Public, DOI | **Month 10** working release; **Month 12** archival DOI (Zenodo) |
| Aggregated topological summaries (no recoverable player identity) | Public, subject to partner agreement | **Month 12**, with the full-season paper |
| Methodology documentation | Public | With papers (methodology Months 1–2; results Month 11) |
| Raw tracking and named-match feeds | Restricted to the project team under the SCAFC–StatsBomb agreement | Not for public release |

A synthetic 22-agent exemplar with known loop structure ships with the container so the method can be run without proprietary tracks.

## FAIR

Findable (DOIs, metadata); accessible (open software and aggregates); interoperable (CSV/JSON, documented schemas); reusable (licence, pinned dependencies, pass/fail exemplar). Raw tracks remain non-open by contract; the DMP does not promise their release.

## Stewardship

PI is data steward. RA (Months 2–10) maintains hashes and the barcode/landscape store (D1–D2). At Month 10 the store and container pass to the PI with the evidence-pack handover.
