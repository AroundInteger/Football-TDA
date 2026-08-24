# KEY CHANGES FROM PREVIOUS DRAFT

## Major Revisions

1. **Data Access Honesty**:
   - Clear statement of current broadcast data access
   - Aspirational GPS data framed appropriately
   - Contingency plan if GPS access not secured
   - Removed over-confident claims about GPS data

2. **Performance Correlation Removed**:
   - r=0.68 claim removed entirely following audit (see `../R068_AUDIT_REPORT.md`), found to be unsubstantiated by real analysis data
   - Replaced with validated findings: scale complementarity, temporal evolution (+18.8% tactical persistence), and cross-domain conflict topology evidence
   - Performance correlation now stated as a research objective (Objective 4), not a preliminary finding
   - Removed quantum/physics terminology entirely

3. **Championship Justification Strengthened**:
   - Clear statement of project partner rationale
   - Data access pathway explained
   - Commercial relevance articulated
   - Removed weak "tactical diversity" claim

4. **Publication Status Realistic**:
   - "In preparation" clearly stated with percentages complete
   - Timeline for submission given
   - No exaggeration of publication status
   - Target journals specified

5. **Budget and Team Revised**:
   - Budget maximised to £100k FEC (£80k EPSRC contribution)
   - RA extended to 9 months (from 6 months) to maximise project capacity
   - Timeline adjusted for 9-month RA contribution
   - PI time commitment maintained at 20% FTE
   - Work packages aligned with available person-months

6. **Validation Focus Enhanced**:
   - Multi-match validation front and centre
   - Statistical robustness emphasised
   - Appropriate caution about generalisability
   - Clear success criteria for each objective

7. **Risk Management Improved**:
   - GPS data access risk explicitly addressed
   - Contingency plans for all major risks
   - Timeline triggers specified
   - Realistic assessment of probabilities

## Technical Corrections

- Removed all "quantum" terminology (replaced with "topological")
- Strengthened mathematical framing throughout
- Added core TDA theory references
- Clarified scale-specific validation rates
- Specified statistical methods (FDR correction, permutation tests)

## Structural Improvements

- Clearer objectives with specific aims and success criteria
- Detailed methodology section with all algorithms specified
- Comprehensive budget justification
- Realistic timeline matching 9-month RA contribution (extended from 6 months to maximise budget)
- Complete data management plan

---

## Revision 4, Post-Paper Validation Update (March 2026)

1. **Preliminary Results Substantially Strengthened**:
   - Single-match validation → 10-match validation (10 SkillCorner broadcast tracking matches)
   - 382 single-match H1 loops → 4,515 H1 loops across 1,500 analysis frames
   - New: real event correlation (104,722 event–topology pairs across 10 matches)
   - New: Wilcoxon rank-sum and permutation tests for temporal dynamics
   - New: sensitivity analysis, complementarity analysis (Spearman, Fisher's), linkage comparison

2. **Temporal Claim Corrected**:
   - Removed "+19% tactical persistence increase", paper shows direction is match-specific, not universal
   - Temporal variability acknowledged matter-of-factly as expected given tactical diversity
   - Statistical tests now support the corrected interpretation

3. **Objectives Reframed (Previous Objectives 1 and 4 Largely Complete)**:
   - Old Obj 1 (multi-match validation) → done in preliminary work
   - Old Obj 4 (event-topology relationships) → initial results in preliminary work
   - New Obj 1: Full-season scaling (~540 matches)
   - New Obj 2: Tactical fingerprinting (baseline topological signatures per formation)
   - New Obj 3: Persistence landscape dynamics (stability regimes, transitions)
   - New Obj 4: Standard Grant preparation (strategic output)

4. **Paper Status Updated**:
   - Paper 1: ArXiv preprint [1], submitted before grant application
   - Paper 2: In preparation (cross-domain conflict application)
   - Paper 3: Planned during grant (full-season results)

5. **Honest Mathematical Framing**:
   - Positioned as applied computational topology, not fundamental mathematical innovation
   - Framework described as practical methods for multi-scale persistent homology
   - Cross-domain claims appropriately caveated

6. **Budget Adjusted**:
   - RA extended from 6 months to 9 months (Months 2–10)
   - Total fEC approximately £100,000 (subject to institutional costing)
   - Timeline adjusted for 9-month RA contribution

7. **Software Stack Updated**:
   - MATLAB removed (codebase archived, fully migrated to Python)
   - Modular Python framework with shared data loaders and TDA utilities

---

**Document Version**: 4.0 (Post-Validation Update)  
**Date**: March 2026  
**Status**: Ready for final review and submission  
**Action Required**: 
  - Submit Paper 1 to ArXiv
  - Confirm institutional fEC costing for 9-month RA
  - Secure Genius Sports letter of support (or adjust data access section accordingly)
  - Confirm Borussia Dortmund collaboration interest and potential letter of support

