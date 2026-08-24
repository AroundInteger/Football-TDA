# DATA MANAGEMENT PLAN

## Data Types and Volumes

**Input Data**:
- Broadcast tracking data: ~540 matches (full Championship season), ~150 sampled frames per match
- File format: CSV/JSON/JSONL with positional coordinates
- Total volume: ~50–100 GB raw data
- Processed data: ~20–40 GB

**Generated Data**:
- Persistence diagrams: ~80,000 files (JSON format, ~540 matches × ~150 frames)
- Topological features: ~1,600 time series (CSV format, per-match and per-scale)
- Persistence landscapes: ~1,600 functional representations (CSV/NumPy format)
- Statistical analyses: ~600 result files (CSV/JSON)
- Visualisations: ~2,000 figures (PNG/PDF)
- Total volume: ~20–30 GB

## Data Storage and Backup

**During Project**:
- Primary storage: Institutional research data storage (backed up daily)
- Working copies: Encrypted local drives
- Version control: Git repository for code and analysis scripts
- Backup frequency: Daily automated backups, weekly manual verification

**Long-Term Preservation**:
- Institutional data repository (10+ year retention)
- Zenodo for open data sharing (DOI assignment)
- GitHub for software and code (indefinite public access)

## Data Sharing and Access

**Open Data**:
- Aggregated topological features (fully anonymised): Public release
- Software and analysis code: Open-source release (MIT license)
- Methodology documentation: Public via institutional repository

**Restricted Data**:
- Raw positional tracking data: Subject to partnership agreements
- Match-specific results: Subject to club permissions
- Access on reasonable request for research purposes

**Timeline for Sharing**:
- Software release: Month 12 (project completion)
- Aggregated data: Month 12 (with publications)
- Detailed methodology: With paper publication(s)

**FAIR Principles Compliance**:
- **Findable**: DOIs, metadata, institutional repository
- **Accessible**: Open-source software, public documentation
- **Interoperable**: Standard formats (CSV, JSON, PDF)
- **Reusable**: Detailed documentation, clear licensing, reproducible workflows

