# ETHICS AND RESPONSIBLE INNOVATION

Aligned to `VA_230826_reconstructed.docx` §6 (risk) and §7 (host data-governance). Data are anonymised professional tracking records, not a new collection from human participants.

## Identification

1. **Privacy and commercial data.** Championship tracking and tactical labels are provided under the Swansea City AFC–StatsBomb agreement. Raw positions are not ours to release.
2. **Open science versus contract.** Methods, code and aggregated topological summaries can be open; raw tracks cannot.
3. **Dual use.** Individual-player surveillance, re-identification, and physical-performance attribution to named players are out of scope (§9). Released analyses are squad-level aggregates.
4. **Independence.** Club partnership must not determine which organisational states are reported.

## Management

**Anonymisation.** Provider feeds replace person identifiers with generic labels. Publications use squad-level summaries. Team names appear only with partner permission; otherwise “Team A/B”.

**Legal basis.** Processing of anonymised positional data for scientific research (UK GDPR / DPA 2018). No direct recruitment; no new personal data collected by the project.

**Security.** Swansea University GDPR-compliant storage; access limited to the named team; processing on institutional HPC. Retention: project duration plus institutional research-data period, then secure deletion of restricted files.

**Open outputs.** Containerised pipeline with DOI (Zenodo, Month 12); OSF pre-registration (Month 2); aggregated barcodes/landscapes without recoverable player identity. MIT (or equivalent) licence on software.

**Dual use (V&A §9).** The pipeline will not be developed or documented as a named-player monitoring tool. Change-point and fingerprint outputs are organisational (formation, pressing structure, coverage), not individual. Any later commercial use is assessed against this restriction.

**Environment.** Compute is ~1,600 CPU-hours on existing Supercomputing Wales allocation; no new hardware.

## Oversight

Ethics review via Swansea University before data processing beyond the existing pilot. Fast-track is appropriate: anonymised secondary data, no participant contact. The PI is accountable; Co-Is and the Research Office provide compliance support. Quarterly check that outputs remain squad-level.
