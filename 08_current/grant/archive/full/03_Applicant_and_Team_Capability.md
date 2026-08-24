# APPLICANT AND TEAM CAPABILITY TO DELIVER

<!-- Working inventory of PI grants, papers, and codes-to-confirm: PI_Research_Background.md.
     Remaining EPSRC reference codes and exact roles to be inserted by the PI. -->

## Contributions to the Generation of New Ideas, Tools, Methodologies, or Knowledge

The Principal Investigator, Dr Rowan Brown, is Senior Lecturer in Biomedical Engineering at Swansea University (MPhys, first class, 2000; PhD, 2004). For more than fifteen years the PI has developed data-driven mathematical methods that recover ensemble organisation from individual-agent measurements — first in large cellular populations, then in spatially structured biological networks, and now in competitive multi-agent systems, including professional sport. This Small Grant continues that programme: the same microstate-to-macrostate question, posed for a 22-player competitive point cloud and answered with multi-scale persistent homology.

**Prior funded research (selected).** As PI: EPSRC Mobility Fellowship (EP/G037841/1, 2008–09) and First Grant (EP/M000621/1, 2014–15) on ensemble behaviour in cellular systems, with GE Healthcare and Professor Tamás Vicsek (collective motion); instrumented mouthguard quantification of rugby head load (Sports and Wellbeing Analytics / Welsh Government, 2020/21); and training-load analytics with Swim Wales (2024/25). As Co-I: Office of Naval Research Global programme on hetero-swarm robotics (2021/22); Welsh Institute of Performance Science (Sport Wales); data-science applications with the English Institute of Sport. Earlier investigator work on nanoparticle tracking (EP/H008683/1) and clot-network geometry (EP/L024799/1) established pipelines on high-volume spatial time-series. First-author algorithms for random fractal aggregates appeared in *Physica D* (2010). Collaborative outputs include *Nature Nanotechnology* (2011), *Nature Methods* (2014) and *Nature Communications* (2019).

**Most relevant prior outputs (PI)**:

1. Brown MR, et al. Flow-based cytometric analysis of cell cycle via simulated cell populations. *PLoS Computational Biology* 2010; 6(4): e1000741 — ensemble models from individual measurements.
2. Brown MR, et al. Fractal discrimination of random fractal aggregates and its application in biomarker analysis for blood coagulation. *Chaos, Solitons & Fractals* 2012 — geometric characterisation of spatial networks.
3. Brown R, Scott G, Kilduff L. Relative Advantage: quantifying performance in noisy competitive settings. Preprint 2025 — with Co-I Kilduff; competitive systems as a measurement domain.

**Technical innovations (this programme)**:

- Measurement-aware clustering resolving H0 artefacts in spatial TDA
- Adaptive filtration enabling multi-scale H1 detection
- Closed-cycle identification for geometric realisation of H1 generators
- Temporal persistence landscapes for dynamical analysis

Validation across 10 matches is detailed in Vision and Approach. The analysis framework is implemented in Python (Ripser, GUDHI, giotto-tda), achieving <2 s per typical frame on Supercomputing Wales; an open-source release is planned.

## Development of Others and Maintenance of Effective Working Relationships

**Current doctoral supervision**: The PI is first supervisor to six full-time doctoral students working on Championship match-outcome analytics (EPSRC DTP with Swansea City AFC), an EPSRC studentship with the UK Sports Institute (UKSI), spatiotemporal rugby and football analytics, international swimming performance prediction, uncertainty in head-acceleration signals, and digital twins for talent identification with Team INEOS; and second supervisor to a doctoral student on responsible AI in government security operations.

**Research Associate development plan**: The Research Associate receives structured training in advanced TDA, statistical inference, and scientific programming, with co-authorship, conference dissemination, and involvement in Standard Grant preparation. Supervision includes weekly meetings and monthly progress reviews.

**Concrete RA deliverables**: The RA post (1.0 FTE, Months 2–10) has three time-stamped deliverables aligned with Objectives 1–3:

- **D1 — Full-season barcode database (Month 7)**: reproducible store of H0 and H1 diagrams at both validated scales for all ~540 Championship matches, with provenance hashes (O1).
- **D2 — Landscape library (Month 8)**: module computing persistence landscapes, Fréchet means, and CUSUM statistics at both scales (O3 landscape-module milestone). Tactical-fingerprint results (O2) and O3 outputs follow at Month 9, against the Month-2 OSF pre-registration.
- **D3 — Handover pack (Month 10)**: documented pipeline, figures, tables, and prose snippets transferred to the PI for the Month-12 O4 Standard Grant evidence pack.

**Equality, diversity and inclusion**: RA recruitment follows Swansea University's EDI code of practice, with anonymised shortlisting, a diverse interview panel (minimum two genders and at least one external or industry member), and advertising through venues that include under-represented-group networks (e.g. Piscopia, BWM, LMS).

**Collaborative research**: Data access and validation combine championship club partnerships (UK) with Genius Sports (UK) and Borussia Dortmund (Germany, former-student pathway). Co-Investigator Professor Liam Kilduff provides sport and exercise science expertise for tactical interpretation; Co-Investigator Professor Gibin Powathil provides mathematical-biology and mathematical-oncology expertise that underpins planned translation to adversarial biomedical systems in the follow-on Standard Grant.

## Contributions to the Wider Research and Innovation Community

**Academic and open-science contributions**: The programme publishes methodological advances for computational topology, presents at leading venues (including SIAM and applied topology meetings), and contributes open-source software to the TDA ecosystem. Methods developed for sport are designed to transfer to other competitive multi-agent settings where spatial coordination is scientifically informative.

**Innovation partnerships and translation**: Existing partnerships with Swansea City AFC, the UK Sports Institute, Sport Wales (WIPS), and Team INEOS provide a pathway through professional sport. The ONR hetero-swarm programme evidences the same multi-agent methods beyond sport.

**Cross-domain relevance and public engagement**: Beyond football, the same analytical lens adapts to other bounded competitive systems wherever domain-validated scales exist; the priority translation targets for the follow-on Standard Grant are adversarial spatial systems in the health sector (for example tumour–immune competition, underpinned by Co-I Powathil's mathematical-oncology expertise) and the economic and security sector (for example competitive logistics and autonomous-fleet coordination). Public engagement is supported by intuitive visualisations of sophisticated mathematics through sport, and by educational outreach that shows applied mathematics addressing concrete problems.

## Contributions to Broader Research or Innovation Users and Towards Wider Societal Benefit

**Mathematical sciences**: This work strengthens the UK mathematical sciences base by providing validated multi-scale persistent homology workflows for competitive systems, efficient computation suitable for large-scale time-series, and educational materials that illustrate persistent homology in realistic applications. The outcome is practical progress in computational topology with clear methodological lineage.

**Broader users, societal benefit, and industry impact**: Wider users include organisations seeking coordination metrics in multi-agent settings (robotics, logistics, crowd safety). Societal benefits include safer management of crowded environments, economic value through sports analytics uptake, and educational inspiration through accessible advanced mathematics. The PI has previously translated a geometric index of spatial structure (incipient-clot fractal dimension) into a clinically interpretable biomarker of clotting outcome, including in patients with venous thromboembolism — direct precedent for turning topological summaries into practitioner-facing tools.
