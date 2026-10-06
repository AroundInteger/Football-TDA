# DATA MANAGEMENT PLAN

<!-- Paste from "Data types and volumes". Dates follow TIMELINE.md.
     Sharing rules match 07_Ethics_and_Responsible_Innovation.md.
     2 Oct 2026. Sole project partner: Swansea City AFC.
     StatsBomb supplies data under the club's commercial agreement. -->

Sharing dates follow the locked timeline. Restricted files and permitted deposits follow the ethics statement.

## Data types and volumes

**Input (restricted).** Championship broadcast tracking and tactical labels for about 540 matches, supplied by Swansea City Association Football Club (Swansea City AFC) under the club's commercial agreement with StatsBomb. Files are positional coordinates, stored as comma-separated values (CSV) or JavaScript Object Notation (JSON). Raw volume is about 50–100 GB. StatsBomb is the data supplier. Swansea City AFC is the sole project partner.

**Generated.** At one frame per second the pipeline writes barcodes, persistence landscapes and vectorised summaries at each accepted scale. Season-scale processing is about 1,600 CPU-hours of the Project Lead's 5,000-hour Supercomputing Wales allocation. Archives are stored per match, compressed. Derived volume is about 20–40 GB, plus figures.

**Code.** A containerised Python pipeline (Ripser, GUDHI and giotto-tda), held under version control.

## Storage and backup

During the award, working data sit on institutional research storage with daily backup. Working copies are encrypted. Code is in Git. Raw tracks are kept for the award plus the institutional retention period for restricted research data, then securely deleted. Code, the pre-registration and permitted aggregates are deposited for at least ten years, in the institutional repository and, where the agreement allows, on Zenodo.

## What can be shared

| Asset | Access | Date |
|---|---|---|
| Open Science Framework (OSF) pre-registration of both objectives | Public | Month 2 |
| Containerised pipeline (Apptainer or Docker) | Public, with a digital object identifier (DOI) | Month 10 working release; Month 12 archival DOI on Zenodo |
| Aggregated topological summaries, with no recoverable player identity | Public, subject to the partner agreement | Month 12, with the full-season paper |
| Methodology documentation | Public | With the papers (methodology in Months 1–2; results in Month 11) |
| Raw tracking and named-match feeds | Project team only, under the Swansea City AFC agreement | Not for public release |

A synthetic 22-agent example with a known loop structure ships with the container, so the method can be run without proprietary tracks.

## FAIR

Deposits are findable through DOIs and metadata, and accessible as open software and permitted aggregates. They are interoperable as CSV or JSON with documented schemas. They are reusable under a stated licence, with pinned dependencies and a pass-or-fail example. Raw tracks remain closed by contract. This plan does not promise their release.

## Stewardship

The Project Lead (PL) is the data steward. The Research Associate (Months 5–10) maintains provenance hashes and the barcode and landscape store. At Month 10 that store and the container pass to the PL with the evidence-pack handover.
