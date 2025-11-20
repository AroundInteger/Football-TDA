# EPSRC Mathematical Sciences Grant Application
## Data Management Plan

**Application Title:** Topological Data Analysis for Dynamic Team Behaviour: Mathematical Foundations for Sports Analytics

---

## DATA TYPES AND VOLUMES

### Primary Data Types

**GPS Tracking Data:**
- Format: 25Hz positional coordinates (x, y) for 22 players
- Volume: ~500MB per match (90 minutes × 25Hz × 22 players × 8 bytes)
- Total for 300 matches: ~150GB
- Source: SecondSpectrum/Genius Sports partnership

**Computed Persistence Diagrams:**
- Format: Birth-death pairs for H₀ and H₁ features
- Volume: ~10MB per match (2,250 frames × 4KB average)
- Total for 300 matches: ~3GB
- Generated: Through VR filtration computation

**Analysis Results:**
- Format: Statistical summaries, correlations, tactical state classifications
- Volume: ~5MB per match
- Total for 300 matches: ~1.5GB
- Generated: Through topological analysis pipeline

**Software and Algorithms:**
- Format: Python/MATLAB code, documentation, test datasets
- Volume: ~100MB (version controlled)
- Generated: Throughout project development

**Total Data Volume:** ~155GB for complete dataset

---

## DATA STORAGE AND BACKUP

### Primary Storage

**Institutional Research Data Repository:**
- Location: [Your Institution] Research Data Management system
- Access: Project team members only
- Backup: Daily automated backups
- Retention: 10 years minimum (EPSRC requirement)
- Compliance: GDPR compliant, ISO 27001 certified

**Commercial Data Storage:**
- Location: Secure encrypted storage (AES-256 encryption)
- Access: Restricted to PI and designated researchers
- Backup: Real-time replication to secondary site
- Retention: As per partnership agreement (minimum 3 years)
- Compliance: Commercial data protection standards

### Backup Strategy

**Daily Backups:**
- Incremental backups of all project data
- Off-site storage at secondary institutional location
- Verification of backup integrity

**Long-term Archival:**
- Annual migration to archival storage systems
- Checksum verification for data integrity
- Multiple copies across different storage media

---

## DATA SHARING AND ACCESS

### Open Access Components

**Algorithms and Software:**
- Repository: GitHub (MIT license)
- Access: Public repository with documentation
- Components: Core TDA algorithms, visualisation tools, analysis pipelines
- Timeline: Released within 6 months of completion

**Anonymised Data Sample:**
- Content: 10 representative matches with player identities removed
- Format: Standardised CSV format with metadata
- Access: Institutional repository with DOI
- Timeline: Released within 12 months of project completion

**Publications and Results:**
- Format: Open access publications (EPSRC requirement)
- Repository: Institutional repository
- Access: Public with embargo periods as required
- Timeline: Immediate upon publication

### Restricted Access Components

**Commercial GPS Data:**
- Access: Project team only
- Sharing: Prohibited under partnership agreement
- Embargo: 3 years from project completion
- Exception: Anonymised statistical summaries may be shared

**Proprietary Algorithms:**
- Access: Project team and industry partners
- Sharing: Subject to IP protection strategy
- Embargo: Until patent applications filed
- Exception: Open source versions released after IP protection

---

## DATA PRESERVATION

### Long-term Preservation

**Minimum Retention Period:** 10 years (EPSRC requirement)

**Preservation Strategy:**
- Migration to archival storage systems
- Format standardisation (CSV, JSON for data; Python/MATLAB for code)
- Documentation of data formats and processing methods
- Regular integrity checks

**Metadata Standards:**
- Dublin Core metadata for datasets
- Detailed technical documentation for algorithms
- User guides and tutorials for software tools
- Version control for all code releases

### Digital Object Identifiers (DOIs)

**Assigned DOIs:**
- Complete anonymised dataset
- Software releases
- Major publications
- Technical reports

**DOI Management:**
- Through institutional DOI service
- Persistent links maintained indefinitely
- Regular validation of DOI resolution

---

## ETHICAL CONSIDERATIONS

### Data Privacy and Protection

**Player Privacy:**
- All player identities removed from shared datasets
- Positional data aggregated to prevent individual identification
- Consent obtained through club-level agreements
- GDPR compliance maintained throughout

**Commercial Sensitivity:**
- Tactical insights protected under partnership agreements
- Competitive advantage information embargoed
- Statistical summaries only shared publicly
- Industry partner approval required for any external sharing

### Research Ethics Approval

**Institutional Approval:**
- [Your Institution] Research Ethics Committee approval obtained
- Regular ethics review throughout project
- Compliance with institutional data protection policies

**Commercial Ethics:**
- Partnership agreements include ethical use clauses
- Fair play principles maintained
- No exploitation of individual players or teams
- Positive contribution to sport emphasised

---

## DATA QUALITY AND INTEGRITY

### Quality Assurance

**Data Validation:**
- Automated checks for GPS data completeness
- Validation of coordinate ranges and player counts
- Detection and correction of measurement errors
- Statistical analysis of data quality metrics

**Processing Verification:**
- Independent verification of TDA computations
- Cross-validation with alternative methods
- Reproducibility testing across different systems
- Documentation of all processing steps

### Version Control

**Code Management:**
- Git version control for all software
- Tagged releases for major milestones
- Branch management for experimental features
- Collaborative development protocols

**Data Versioning:**
- Timestamped versions of all datasets
- Change logs for data modifications
- Rollback capability for erroneous changes
- Audit trail for all data access

---

## RESOURCES AND INFRASTRUCTURE

### Computational Resources

**High-Performance Computing:**
- Institutional HPC cluster access
- GPU acceleration for TDA computations
- Parallel processing for large-scale analysis
- Cloud computing backup for peak loads

**Storage Infrastructure:**
- Primary: Institutional research storage (10TB allocated)
- Secondary: Commercial cloud storage (5TB allocated)
- Archival: Long-term tape storage (unlimited)
- Backup: Automated replication systems

### Personnel Responsibilities

**Data Manager:** Postdoctoral Research Associate
- Daily data management and quality assurance
- Implementation of backup and sharing protocols
- Documentation and metadata creation
- Liaison with institutional data services

**Technical Lead:** Principal Investigator
- Overall data strategy and policy compliance
- Industry partnership data agreements
- Long-term preservation planning
- Ethics and legal compliance oversight

---

## COMPLIANCE AND MONITORING

### Regulatory Compliance

**EPSRC Requirements:**
- Open access publication compliance
- Data sharing obligations met
- Long-term preservation maintained
- Regular reporting on data management

**Institutional Policies:**
- Research data management policy compliance
- Information security standards maintained
- Intellectual property protection
- Commercial partnership agreements honoured

### Monitoring and Review

**Regular Reviews:**
- Quarterly data management review
- Annual preservation strategy assessment
- Continuous compliance monitoring
- Stakeholder feedback integration

**Success Metrics:**
- Data integrity maintained (100% target)
- Sharing obligations met (100% target)
- Access requests handled efficiently (<48 hours)
- Long-term preservation successful (10+ years)

This comprehensive data management plan ensures responsible handling of sensitive commercial data whilst maximising the research impact through appropriate sharing and preservation strategies.
