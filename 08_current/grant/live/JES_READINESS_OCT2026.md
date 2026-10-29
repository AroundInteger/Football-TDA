# JeS readiness audit — 7 Oct 2026

UK English. Run before paste/submit. Harness Track C.

## Automated counts (markdown; re-count in JeS after paste)

| Field | File | Words (rough) | Limit | Status |
|---|---|---:|---:|---|
| Public summary | `01_Summary.md` | 550 (`## Context` → end, headings included) | 550 | OK — re-count in JeS after paste |
| R4RI | `03_Applicant_and_Team_Capability.md` | ~913 (HTML comment stripped) | 1,000 | OK |
| V&A body | `02_Vision_and_Approach_REV4.md` | ~1,619 (`## Vision` → `## References`) | ~1,600 + 3 pages | **Re-measure in Word/JeS** (EC pass was 1,600 on 17 Sep) |
| References | `04_References.md` | 29 numbered entries | 1,000 | OK |

## Paste-ready

- [x] REV4 HTML revision block removed (archived to `archive/REV4_revision_header_oct2026.md`).
- [ ] Other live files still have paste hints in HTML comments (`01`, `03`, `05`–`08`) — do not paste those comment blocks.
- [x] Paste order documented: `JES_PASTE_SEQUENCE.md`.
- [x] Gantt figure present: `grant_figure_gantt.png`.
- [x] **SCAFC letter received** (`Project Partners/`, Daniel Morris, 15 Oct 2026). [ ] Export/upload PDF `APP98322 Project partner` if not yet filed.

## Staff / costs cross-check (7 Oct 2026)

- [x] `TIMELINE.md` ↔ `06_Resources_and_Costs.md` ↔ `Costs/IPA_799_16Oct_lock.md`: PL 0.10 · PcL 0.05 · RA Months 5–10 · **£96,918** staff fEC · ATMCS 13 travel **£2,150** (PL only, 21 Oct planner); unused headroom **£932** · dates 1 Mar 2027–29 Feb 2028 · no LK/GP. Workbook: `Budget 16 10 26 IPA 799.xlsx`; travel: `Travel budget planner 21 10 26 IPA 799.xlsx`.

## Human gates (not in repo)

- [ ] Finance JeS lines match workbook (RO sign-off)
- [ ] NV Co-I confirmation; SCAFC project-partner PDF upload (letter received; see `Project Partners/`)
- [ ] Research Office / HoS approval
- [ ] JeS dry-run

## Paper A (parallel)

- Nelly C1–C5 in TeX; `sync_to_paper.py` PASS; `paper_A_JACT/main.pdf` and `arXiv_Paper_A/main.pdf` built 7 Oct (`arXiv_Paper_A/figures` → symlink to `paper_A_JACT/figures`).
