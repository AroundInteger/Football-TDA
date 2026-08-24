# ETHICS AND RESPONSIBLE INNOVATION

## Identification and Evaluation of Ethical and RRI Considerations

This research involves analysis of anonymised positional tracking data from professional football matches. We have identified the following ethical and responsible research and innovation (RRI) considerations:

**Primary Ethical Considerations**:
1. **Data Privacy and Protection**: Ensuring player and team data privacy while enabling research
2. **Data Re-use and Open Science**: Balancing open science principles with data protection requirements
3. **Commercial Applications**: Ensuring research benefits extend beyond commercial interests
4. **Methodological Transparency**: Maintaining reproducibility while protecting proprietary data sources
5. **Dual Use Concerns**: Ensuring methods are not misused for surveillance or negative applications

**RRI Considerations**:
1. **Accessibility**: Making mathematical methods and tools accessible to broader research community
2. **Environmental Impact**: Minimising computational resource consumption
3. **Societal Benefit**: Ensuring applications prioritise public safety and societal good
4. **Stakeholder Engagement**: Maintaining transparent relationships with industry partners

## Management of Ethical and RRI Considerations

### Data Privacy and Protection Management

**Anonymisation Strategy**: All data used in this research is pre-anonymised by data providers (Statsbomb, Genius Sports). Player identifiers are replaced with generic position labels (e.g., "Player 1", "Player 2") with no linkage to personal identities. Team identifiers are retained for tactical analysis but can be further anonymised if required for publication.

**Data Security**: All data will be stored on Swansea University's secure, GDPR-compliant infrastructure (100TB secure storage). Access is restricted to project team members only, with encrypted storage and secure transfer protocols. Data processing occurs on institutional HPC cluster with appropriate access controls.

**Data Retention and Disposal**: Data will be retained for the project duration plus standard institutional retention period (typically 7 years for research data). After this period, data will be securely deleted in accordance with institutional data protection policies. No personal data will be retained beyond necessary project duration.

### Data Re-use Strategy

**Open Science Approach**: While raw tracking data cannot be publicly released due to commercial agreements, we will:
- Release fully anonymised, aggregated analytical outputs (persistence diagrams, pattern signatures) that enable reproducibility without requiring raw data
- Provide comprehensive methodology documentation enabling replication with alternative data sources
- Release open-source software (Python code) implementing all analytical methods
- Publish detailed methodological descriptions in open access publications

**Data Sharing Agreements**: All data access is governed by formal agreements with:
- Swansea City AFC (via SCAFC-Statsbomb partnership)
- Statsbomb (broadcast tracking data)
- Genius Sports/Oval (GPS data, if secured)

These agreements specify permitted uses, data handling requirements, and restrictions on redistribution. Research outputs will comply with all agreement terms while maximising scientific value.

**Enabling Future Re-use**: Analytical methods and software will be designed for use with any compatible tracking data, enabling other researchers to apply methods to their own datasets. Documentation will include data format specifications and preprocessing requirements.

## Legal and Ethical Considerations for Data Collection, Release, and Storage

### Consent and Legal Basis

**Legal Basis for Processing**: Data processing is conducted under legitimate research interest (GDPR Article 6(1)(f)) and scientific research exemption (GDPR Article 9(2)(j)). Data is collected by third-party providers (Statsbomb, Genius Sports) who have appropriate legal bases for data collection from broadcast/performance monitoring.

**Consent**: As anonymised positional data with no personal identifiers, explicit consent is not required. However, we maintain transparency through:
- Clear communication with data providers about research purposes
- Publication of research objectives and methods
- Industry partner engagement ensuring alignment with data use expectations

**Third-Party Data**: All data is obtained through established commercial partnerships. We do not collect data directly from individuals, ensuring compliance with data protection regulations through contractual agreements with data providers.

### Confidentiality

**Confidentiality Measures**:
- All data stored on secure, access-controlled institutional systems
- Project team members bound by institutional data protection policies and confidentiality agreements
- No sharing of raw data beyond project team
- Aggregated outputs only shared in publications, with no identifiable information

**Team and Match Confidentiality**: While team identities may be retained for tactical analysis, we will:
- Seek permission from partners before publishing team-specific findings
- Use generic identifiers (e.g., "Team A", "Team B") in publications where appropriate
- Ensure no commercially sensitive tactical information is disclosed without consent

### Anonymisation

**Anonymisation Approach**: 
- Player-level anonymisation: Generic position identifiers only (no names, jersey numbers, or personal characteristics)
- Team-level anonymisation: Team names can be anonymised for publication if required
- Match-level anonymisation: Match dates and specific fixtures can be anonymised while retaining temporal and contextual information necessary for analysis

**Anonymisation Verification**: All data outputs for publication will be reviewed to ensure no re-identification is possible. Aggregated statistics and pattern signatures contain no identifiable information.

### Security

**Technical Security Measures**:
- Encrypted data storage (AES-256 encryption at rest)
- Secure data transfer (TLS/SSL protocols)
- Access control: Role-based access restricted to project team
- Regular security audits of institutional infrastructure
- Secure backup procedures with encrypted backups

**Organisational Security**:
- All team members receive data protection training
- Compliance with Swansea University Information Security Policy
- Regular review of data access logs
- Incident response procedures for any data breaches

### Other Ethical Considerations

**Fairness and Non-Discrimination**: Research focuses on collective tactical patterns rather than individual player performance, avoiding potential discrimination or bias. Analysis methods are applied uniformly across all teams and matches.

**Transparency**: Research methods, limitations, and assumptions will be clearly documented in publications. Any potential biases in data collection or analysis will be explicitly acknowledged.

**Accountability**: Principal Investigator takes responsibility for ethical conduct. Regular review of ethical considerations throughout project. Institutional ethics approval obtained before project commencement.

## Formal Information Standards Compliance

**GDPR (General Data Protection Regulation)**: Full compliance with GDPR requirements:
- Lawful basis for processing (research exemption)
- Data minimisation (only necessary data collected)
- Purpose limitation (data used only for specified research purposes)
- Storage limitation (data retained only for necessary duration)
- Security of processing (appropriate technical and organisational measures)

**Data Protection Act 2018**: Compliance with UK data protection legislation, including:
- Processing in accordance with data protection principles
- Rights of data subjects (where applicable)
- Data breach notification procedures

**UKRI Data Policy**: Compliance with UKRI data management requirements:
- Data Management Plan (see Section 08)
- Open access to research outputs
- Data sharing where possible and appropriate
- Long-term preservation of research data

**Institutional Policies**: Compliance with Swansea University:
- Information Security Policy
- Data Protection Policy
- Research Ethics Policy
- Research Data Management Policy

**FAIR Data Principles**: Where possible, research outputs will follow Findable, Accessible, Interoperable, and Reusable (FAIR) principles:
- **Findable**: Metadata and documentation for all outputs
- **Accessible**: Open-source software and methodology available
- **Interoperable**: Standard formats and clear specifications
- **Reusable**: Comprehensive documentation enabling replication

## Responsible Innovation Framework

### Open Science and Accessibility

**Open-Source Software**: All analytical code will be released under open-source license (MIT or similar) on GitHub, enabling:
- Full methodological transparency
- Community contribution and improvement
- Application to other domains and datasets
- Educational use

**Open Access Publications**: All publications will be open access (funded through institutional UKRI block grants), ensuring:
- Maximum dissemination of research findings
- Accessibility to researchers globally
- Cross-disciplinary engagement
- Public benefit from publicly funded research

**Methodology Documentation**: Comprehensive documentation including:
- Detailed algorithmic descriptions
- Parameter specifications and justifications
- Validation procedures and results
- Limitations and assumptions

### Societal Benefit and Public Engagement

**Prioritising Public Good**: Research applications prioritise:
- Public safety (crowd management, emergency response)
- Environmental benefits (traffic management, resource optimisation)
- Scientific advancement (open methods, reproducible research)
- Educational value (public engagement, teaching resources)

**Commercial Balance**: While industry partnerships provide data access, research outputs remain:
- Scientifically rigorous and independent
- Accessible to broader research community
- Focused on fundamental understanding rather than proprietary applications
- Transparent about limitations and assumptions

### Environmental Sustainability

**Computational Efficiency**: 
- Optimised algorithms minimising computational requirements
- Efficient use of institutional HPC resources (shared infrastructure)
- Code optimisation reducing energy consumption
- No dedicated hardware requiring additional energy resources

**Resource Minimisation**: 
- Leveraging existing institutional infrastructure
- Efficient data storage and processing
- Minimising redundant computations
- Open-source approach enabling community optimisation

### Dual Use and Misuse Prevention

**Positive Applications Focus**: Research explicitly focuses on:
- Understanding collective behaviour for positive applications
- Public safety and emergency planning
- Scientific understanding of complex systems
- Educational and research applications

**No Surveillance Development**: Research does not involve:
- Development of tracking or surveillance technologies
- Individual identification or profiling
- Behavioural monitoring of individuals
- Privacy-invasive applications

**Ethical Framework**: Any future commercial applications will be evaluated against:
- Public benefit criteria
- Privacy and data protection requirements
- Transparency and accountability standards
- Responsible innovation principles

## Ethics Approval and Oversight

**Institutional Ethics Review**: Ethics approval will be obtained through Swansea University's Research Ethics Committee prior to project commencement. Fast-track approval expected (4-week turnaround) given:
- Use of anonymised, pre-existing data
- No direct interaction with human participants
- Established data protection protocols
- Low-risk research design

**Ongoing Ethical Review**: Regular review of ethical considerations throughout project:
- Quarterly review of data handling procedures
- Assessment of any new ethical issues arising
- Compliance monitoring with data protection requirements
- Stakeholder engagement on ethical considerations

**Accountability**: Principal Investigator maintains overall responsibility for ethical conduct, with support from:
- Institutional Research Ethics Committee
- Data Protection Officer
- Research Office compliance support
- Co-Investigators providing oversight

This comprehensive approach ensures all ethical and RRI considerations are identified, evaluated, and appropriately managed throughout the project lifecycle.
