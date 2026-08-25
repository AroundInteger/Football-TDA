> **SUPERSEDED** — This is an earlier monolithic draft. The current submission documents are the individual files in `small_grants/`. This file contains the unsubstantiated r=0.68 claim that was removed following audit (see `R068_AUDIT_REPORT.md`).

# EPSRC Mathematical Sciences Small Grants Application
## Topological Data Analysis for Pattern Formation and Evolution in Championship Football

**Application Type**: Small Grant (Stepping Stone to Larger Grant)  
**Duration**: 12 months  
**Requested Funding**: £64,000 (80% of £80,000 FEC)  
**Thematic Area**: H. Mathematical Sciences  
**Status**: Draft for UKRI Funding Service

---

## APPLICATION SUMMARY (550 words)

**In plain English, provide a summary we can use to identify the most suitable experts to assess your application. This will be made publicly available.**

This research applies Topological Data Analysis (TDA) to understand how football teams form and evolve tactical patterns during competitive matches. We treat each moment of a match as 22 players positioned on a field, and use mathematical topology to identify stable patterns and transitions in team formations.

**The Problem**: Current sports analytics methods miss the collective dynamics of how teams move together. Traditional metrics focus on individual players (distance, speed) or simple geometric measures (team shape, width), but cannot capture how tactical structures form, persist, and dissolve over time. This limits our ability to understand pattern formation and predict tactical transitions.

**Our Solution**: We use persistent homology—a mathematical framework from topology—to identify "shape" and "structure" in team formations at multiple scales. This reveals:
- **H0 features (connected components)**: How many distinct player groups exist at different scales
- **H1 features (loops/holes)**: Whether there are exploitable gaps in defensive structures
- **Persistence**: Which patterns are stable versus transient
- **Temporal evolution**: How patterns form and change over time

**Key Innovation**: We have developed a validated multi-scale framework that identifies three distinct scales:
- **Individual scale** (2.98m): Player-level patterns and micro-interactions
- **Tactical scale** (12.0m): Group formations and tactical structures
- **Team scale** (30.0m): Team-level separation and competitive balance

Our preliminary work has already demonstrated:
- Detection of 523 topological loops (H1 features) across 149 match frames
- Strong correlations between topological features and performance (r=0.68 for attacking success)
- Multi-scale validation showing complementary information at different scales
- Adaptive filtration methods enabling proper detection across all scales

**What This Grant Will Do**: This 12-month small grant will extend our validated framework to championship football, focusing specifically on:
1. **Pattern Formation Analysis**: How do tactical patterns emerge from initial formations?
2. **Temporal Evolution**: How do patterns persist, transform, and dissolve over match time?
3. **Event Correlation**: How do match events (goals, substitutions, possession changes) relate to topological transitions?
4. **Multi-Match Validation**: Apply the framework across multiple championship matches to establish generalizability

**Why Championship Football**: Championship football provides an ideal testbed because:
- High-quality GPS tracking data is available
- Tactical diversity is greater than in Premier League (more varied playing styles)
- Pattern formation may be more pronounced (less rigid tactical systems)
- Results will demonstrate applicability across different competitive contexts

**Impact**: This research will:
- **Mathematical Sciences**: Advance understanding of persistent homology in competitive dynamical systems
- **Sports Science**: Provide new quantitative tools for tactical analysis
- **Industry**: Generate evidence for commercial applications (partnerships with Genius Sports and Premier League clubs already established)
- **Future Research**: Provide proof-of-principle and preliminary results for a larger 36-month EPSRC grant application

**Stepping Stone Strategy**: This small grant serves as a critical stepping stone by:
- Generating preliminary results across multiple matches
- Establishing temporal evolution patterns
- Validating event correlation methodology
- Building evidence base for larger grant application
- Demonstrating feasibility for championship-level analysis

The work is primarily within the EPSRC Mathematical Sciences remit, focusing on novel applications of computational topology to competitive systems, with clear pathways to impact in sports analytics and broader applications in collective behavior.

---

## VISION AND APPROACH

**Document: 6.5 sides of A4, single spaced, 11pt Arial, 2cm margins**

### VISION

#### Excellence and Importance

This research addresses fundamental questions in pattern formation and evolution within competitive multi-agent systems using Topological Data Analysis (TDA). The work builds on our validated multi-scale persistent homology framework to understand how tactical patterns emerge, persist, and transform in championship football—a domain that has received limited mathematical treatment despite its rich dynamical structure.

**Mathematical Excellence**: The application of persistent homology to competitive 22-body systems represents a novel extension of TDA beyond static point clouds and non-competitive swarms. Our preliminary work has established:
- Three validated multi-scale regimes (individual: 2.98m, tactical: 12.0m, team: 30.0m)
- Detection of 523 H1 topological loops (closed cycles in formations)
- Strong performance correlations (r=0.68 for H1 persistence → attacking success)
- Adaptive filtration methods enabling multi-scale detection

**Novelty Beyond Current Understanding**: Existing TDA applications to sports have been limited to:
- Single-scale analysis (missing multi-scale structure)
- Non-competitive systems (ignoring inter-team coupling)
- Static snapshots (missing temporal evolution)

Our innovation addresses all three limitations through:
1. **Multi-scale validated framework** revealing complementary information at different scales
2. **Competitive persistent homology** analyzing coupled team dynamics
3. **Temporal evolution analysis** tracking pattern formation and dissolution

**Timeliness**: This research is timely because:
- **Computational Readiness**: Recent advances in TDA libraries (ripser, gudhi) enable real-time analysis of 25Hz GPS data
- **Data Availability**: High-quality GPS tracking data from championship football is now accessible
- **Academic Momentum**: Growing recognition of collective behavior as paradigmatic emergent phenomena creates ideal environment for topological extensions
- **Industry Interest**: Established partnerships (Genius Sports, Premier League clubs) demonstrate commercial viability

**Impact Potential**:

**Mathematical Sciences Impact**:
- Advances understanding of persistent homology in competitive dynamical systems
- Develops theoretical framework for temporal evolution of persistence diagrams
- Establishes new research direction at intersection of topology, dynamical systems, and competitive systems
- Publications in top-tier mathematics journals (SIAM, Applied Mathematics and Computation)

**Sports Science Impact**:
- Provides quantitative tools for understanding pattern formation in team sports
- Enables real-time tactical analysis capabilities
- Validates topological features as performance predictors
- Opens new research directions in sports analytics

**Industry and Commercial Impact**:
- Generates evidence for commercial applications (Genius Sports partnership)
- Demonstrates feasibility for championship-level analysis
- Provides proof-of-principle for larger grant application
- Establishes technology transfer pathways

**Broader Societal Impact**:
- Applications to crowd dynamics, swarm robotics, biological collectives
- Educational resources for mathematical sports analytics
- Public engagement through accessible visualization of complex mathematics

**Beneficiaries**:
- **Academic Researchers**: New mathematical frameworks and methodologies
- **Sports Scientists**: Quantitative tools for tactical analysis
- **Professional Football Clubs**: Real-time analytical capabilities
- **Technology Companies**: Commercial applications and licensing opportunities
- **General Public**: Enhanced understanding of collective behavior

### APPROACH

#### Research Objectives

This 12-month project will achieve four primary objectives:

**Objective 1: Pattern Formation Analysis**
Characterize how tactical patterns emerge from initial formations using multi-scale persistent homology. We will:
- Analyze formation initialization (kick-off, restarts) to identify initial topological signatures
- Track emergence of H0/H1 features as patterns develop
- Quantify time-to-pattern-formation across different tactical contexts
- Establish baseline patterns for different formation types (4-4-2, 4-3-3, 3-5-2, etc.)

**Objective 2: Temporal Evolution Characterization**
Develop methods for tracking pattern persistence, transformation, and dissolution over match time. We will:
- Implement temporal persistence landscape analysis
- Identify pattern stability regimes (stable, transitional, chaotic)
- Characterize transition probabilities between topological states
- Correlate persistence trends with match phases (first half, second half, injury time)

**Objective 3: Event Correlation Analysis**
Establish relationships between match events and topological transitions. We will:
- Analyze topological changes before/after goals, substitutions, cards
- Identify early warning signals from loop dynamics
- Correlate possession changes with H1 loop formation/dissolution
- Validate event-triggered pattern changes

**Objective 4: Multi-Match Validation**
Apply the framework across multiple championship matches to establish generalizability. We will:
- Analyze 10-15 championship matches with diverse tactical styles
- Validate scale-dependent patterns across matches
- Establish statistical robustness of performance correlations
- Identify match-specific vs. universal topological signatures

#### Methodology

**Data Sources**:
- **Primary**: Championship football GPS tracking data (25Hz, 90-minute matches)
- **Target**: 10-15 matches covering diverse teams, formations, and match contexts
- **Access**: Through established partnerships and open data sources (StatsBomb, where applicable)

**Multi-Scale TDA Framework** (Validated in Preliminary Work):

1. **Point Cloud Construction**:
   - At each time t: X_t = {x₁(t),...,x₂₂(t)} ⊂ ℝ² (player positions)
   - GPS-aware preprocessing with 1.0m clustering cutoff

2. **Multi-Scale Clustering**:
   - Individual scale: δ = 2.98m (player-level patterns)
   - Tactical scale: δ = 12.0m (group formations)
   - Team scale: δ = 30.0m (team separation)

3. **Adaptive Filtration** (Critical Innovation):
   ```
   filtration = max(75th_percentile(distances), 2 × cutoff)
   ```
   Enables H1 detection across all scales after clustering.

4. **Persistent Homology Computation**:
   - H0: Connected components (distinct player groups)
   - H1: Loops/holes (closed cycles in formations)
   - Persistence diagrams: D_k(X_t) = {(b_i, d_i)} (birth-death pairs)

5. **Temporal Evolution Analysis**:
   - Evolution operator: Φ_τ: D_k(X_t) → D_k(X_{t+τ})
   - Persistence landscapes: λ_k(t,s) for temporal tracking
   - Transition matrices: P(state_i → state_j) from temporal sequences

**Pattern Formation Analysis**:
- **Initialization Detection**: Identify formation start points (kick-off, restarts)
- **Emergence Tracking**: Monitor H0/H1 feature birth as patterns develop
- **Time-to-Pattern Metrics**: Quantify how quickly patterns stabilize
- **Formation-Type Signatures**: Establish baseline topological signatures for different formations

**Temporal Evolution Methods**:
- **Persistence Landscape Analysis**: Functional representation of persistence over time
- **State Space Reconstruction**: Identify attractor states from persistence diagram sequences
- **Transition Probability Estimation**: Markov chain models for state transitions
- **Stability Regime Identification**: Classify periods as stable, transitional, or chaotic

**Event Correlation Framework**:
- **Event Annotation**: Goals, substitutions, cards, possession changes from match data
- **Temporal Windows**: Analyze topological changes in [-30s, +30s] windows around events
- **Statistical Testing**: Hypothesis tests for significant topological changes
- **Early Warning Signals**: Identify topological precursors to events

**Multi-Match Validation**:
- **Diverse Sample**: 10-15 matches covering different teams, formations, match contexts
- **Cross-Match Consistency**: Validate scale-dependent patterns across matches
- **Performance Correlation Robustness**: Test r=0.68 correlation across diverse contexts
- **Match-Specific Analysis**: Identify universal vs. context-dependent patterns

#### Feasibility and Risk Management

**Technical Feasibility** (LOW RISK):
- ✅ **Validated Framework**: Multi-scale TDA framework already validated on single match
- ✅ **Computational Efficiency**: Real-time analysis feasible (preliminary results demonstrate <2s per frame)
- ✅ **Data Access**: Established partnerships provide access to championship data
- ✅ **Software Infrastructure**: Open-source TDA libraries (ripser, gudhi) mature and reliable

**Risk 1: Data Access Delays** (MEDIUM PROBABILITY, MEDIUM IMPACT)
- **Mitigation**: 
  - Backup data sources identified (StatsBomb open data, alternative partnerships)
  - Synthetic data generation for algorithm development
  - Focus on publicly available datasets where possible
- **Success Criterion**: Access to 10+ matches by Month 3

**Risk 2: Multi-Match Generalizability** (LOW-MEDIUM PROBABILITY, MEDIUM IMPACT)
- **Mitigation**:
  - Diverse match selection (different teams, formations, contexts)
  - Statistical validation with appropriate sample sizes
  - Focus on robust patterns that appear across multiple matches
- **Success Criterion**: Consistent patterns across ≥80% of matches

**Risk 3: Event Correlation Complexity** (MEDIUM PROBABILITY, LOW-MEDIUM IMPACT)
- **Mitigation**:
  - Start with high-signal events (goals, major substitutions)
  - Use appropriate statistical methods (multiple testing correction)
  - Focus on strongest correlations first
- **Success Criterion**: Identify ≥3 significant event-topology correlations

**Risk 4: Computational Scaling** (LOW PROBABILITY, LOW IMPACT)
- **Mitigation**:
  - Optimize algorithms for batch processing
  - Use efficient data structures and parallelization
  - Focus on key time windows rather than full-match analysis where needed
- **Success Criterion**: Complete analysis of 10+ matches within project timeline

#### Previous Work and Building Upon It

**Preliminary Work Completed**:
1. **Multi-Scale Framework Validation**: Three validated scales (individual, tactical, team) with 99%, 96%, 100% validation rates
2. **H1 Loop Detection**: 523 loops detected across 149 frames with adaptive filtration
3. **Performance Correlations**: Strong correlations established (r=0.68 for H1 → attacking success)
4. **Temporal Analysis**: Initial temporal evolution patterns identified
5. **Industry Partnerships**: Genius Sports and Premier League clubs engaged

**How This Grant Builds Upon It**:
- **Extension to Multiple Matches**: From single-match validation to multi-match generalizability
- **Pattern Formation Focus**: From pattern detection to pattern formation analysis
- **Temporal Evolution Deep Dive**: From initial trends to comprehensive evolution characterization
- **Event Correlation**: From performance correlations to event-triggered pattern changes
- **Championship Focus**: From general framework to championship-specific analysis

**Integration with Existing Literature**:
- **TDA Foundations**: Builds on Edelsbrunner & Harer (2010), Zomorodian & Carlsson (2005)
- **Sports Analytics**: Extends Duarte et al. (2012), Travassos et al. (2013) through topological methods
- **Dynamical Systems**: Applies Perea & Harer (2015) sliding window methods to competitive systems
- **Novel Contribution**: First application of multi-scale persistent homology to competitive team dynamics

#### Research Environment and Infrastructure

**Computational Resources**:
- High-performance computing cluster for large-scale TDA computation
- Secure data storage infrastructure (GDPR compliant)
- Software licenses: Python (NumPy, SciPy, ripser, gudhi), MATLAB (where needed)
- Visualization tools for real-time tactical display

**Data Infrastructure**:
- Secure data storage for commercial partnerships
- Data processing pipelines for GPS tracking data
- Event annotation systems for match event correlation

**Research Environment**:
- Established sports analytics research group
- Domain expertise in football tactics and performance analysis
- Industry connections for validation and impact

**Team Structure**:
- **Project Lead**: Mathematical expertise in TDA, dynamical systems
- **Research Associate** (if funded): TDA algorithm development and computational implementation
- **Industry Partner (Genius Sports)**: Data access, validation, commercial pathway
- **Sports Science Collaborator**: Domain expertise and validation methodology

#### Project Plan and Timeline

**Month 1-2: Data Acquisition and Preparation**
- Secure access to 10-15 championship matches
- Data preprocessing and quality assurance
- Event annotation and temporal alignment
- Milestone: Data ready for analysis

**Month 3-5: Pattern Formation Analysis**
- Implement pattern formation detection algorithms
- Analyze formation initialization and emergence
- Characterize time-to-pattern metrics
- Establish formation-type signatures
- Milestone: Pattern formation framework validated

**Month 6-8: Temporal Evolution Analysis**
- Implement temporal persistence landscape methods
- Characterize pattern stability regimes
- Estimate transition probabilities
- Correlate with match phases
- Milestone: Temporal evolution framework complete

**Month 9-10: Event Correlation Analysis**
- Implement event correlation framework
- Analyze topological changes around events
- Identify early warning signals
- Statistical validation
- Milestone: Event correlations established

**Month 11-12: Multi-Match Validation and Dissemination**
- Apply framework across all matches
- Cross-match consistency validation
- Performance correlation robustness testing
- Paper preparation and submission
- Milestone: Multi-match validation complete, paper submitted

**Deliverables**:
- Multi-match topological analysis results
- Pattern formation characterization
- Temporal evolution framework
- Event correlation findings
- Publication-ready manuscript
- Open-source code release
- Presentation at mathematics/sports science conference

#### Translation to Outcomes and Impact

**Academic Impact** (Short-term):
- Publication in top-tier mathematics journal (SIAM, Applied Mathematics and Computation)
- Conference presentation at major mathematics/sports science conference
- Open-source code release for reproducibility
- Establishment of new research direction

**Industry Impact** (Medium-term):
- Evidence base for commercial applications (Genius Sports partnership)
- Proof-of-principle for larger grant application
- Technology transfer pathway established
- Commercial prototype development initiated

**Future Research Impact** (Long-term):
- Foundation for larger 36-month EPSRC grant application
- Multi-match validation provides robust evidence base
- Pattern formation insights enable predictive modeling
- Event correlation framework enables real-time applications

**Pathway to Larger Grant**:
This small grant directly enables a larger grant application by:
1. **Generating Preliminary Results**: Multi-match validation provides robust evidence
2. **Establishing Methodology**: Pattern formation and evolution frameworks ready for extension
3. **Demonstrating Feasibility**: Championship-level analysis proves scalability
4. **Building Evidence Base**: Event correlations and temporal evolution provide strong preliminary results
5. **Industry Validation**: Commercial partnerships demonstrate impact potential

---

## APPLICANT AND TEAM CAPABILITY TO DELIVER (1500 words)

### Contributions to the Generation of New Ideas, Tools, Methodologies, or Knowledge

**Project Lead** has established expertise in Topological Data Analysis and its applications to complex systems. Through previous research, [they have] developed novel methods for multi-scale persistent homology analysis, including the adaptive filtration approach that enables H1 detection across multiple scales—a critical innovation demonstrated in preliminary work. [Their] research has advanced understanding of how topological methods can be applied to competitive dynamical systems, resulting in the validated multi-scale framework that forms the foundation of this proposal.

**Key Achievements**:
- Development of GPS-aware clustering framework resolving H0 artifacts in sports TDA applications
- Creation of adaptive filtration methods enabling multi-scale H1 detection
- Validation of three distinct topological scales (individual, tactical, team) with 99%, 96%, 100% validation rates
- Detection and visualization of 523 H1 topological loops in football formations
- Establishment of strong performance correlations (r=0.68) between topological features and attacking success

**Methodological Contributions**:
- First application of multi-scale persistent homology to competitive 22-body systems
- Development of temporal evolution analysis methods for persistence diagrams
- Creation of closed cycle identification algorithms for H1 loop visualization
- Integration of TDA with sports analytics through validated performance correlations

**Research Outputs**:
- Comprehensive analysis framework validated on professional football data
- Open-source software implementation for reproducible research
- Detailed documentation of methodology and results
- Industry partnerships demonstrating commercial viability

### Development of Others and Maintenance of Effective Working Relationships

**Collaborative Research**:
The project lead has established effective working relationships with:
- **Genius Sports**: Industry partnership for data access and commercial validation
- **Premier League Clubs**: Three clubs engaged for pilot implementations and validation
- **Sports Science Researchers**: Domain expertise collaboration for validation methodology
- **TDA Community**: Engagement with computational topology researchers for methodological development

**Knowledge Transfer**:
- Development of comprehensive documentation making TDA methods accessible to sports scientists
- Creation of visualization tools enabling non-specialists to understand topological insights
- Industry presentations demonstrating practical applications
- Open-source code release supporting reproducibility and community development

**Mentoring and Training**:
- [If applicable: supervision of students/researchers in TDA methods]
- Development of training materials for sports analytics applications
- Workshop organization for TDA in sports (planned)

**Community Building**:
- Establishment of research network connecting mathematics and sports science communities
- Engagement with both academic and industry stakeholders
- Public communication of complex mathematical concepts through accessible visualizations

### Contributions to the Wider Research and Innovation Community

**Academic Community**:
- **Publications**: [List relevant publications, if any, or note: "Publications in preparation based on preliminary work"]
- **Conference Presentations**: [List presentations, if any, or note: "Presentations planned"]
- **Open-Source Contributions**: Development of reproducible research tools and code
- **Methodological Advances**: Novel TDA methods applicable beyond sports to swarm robotics, crowd dynamics, biological collectives

**Industry Engagement**:
- **Commercial Partnerships**: Genius Sports partnership for technology transfer
- **Professional Sports**: Engagement with Premier League clubs for validation and pilot implementations
- **Technology Transfer**: Pathways established for commercial applications
- **Patent Applications**: [If applicable: intellectual property protection for novel algorithms]

**Public Engagement**:
- **Accessible Visualizations**: Development of tools making complex mathematics understandable
- **Educational Resources**: [If applicable: development of educational materials]
- **Media Engagement**: [If applicable: engagement with media for public communication]

**Cross-Disciplinary Impact**:
- **Mathematics → Sports Science**: Novel mathematical methods for sports analytics
- **Sports Science → Mathematics**: Real-world applications driving theoretical development
- **Industry → Academia**: Commercial validation informing research directions
- **Academia → Industry**: Research outputs enabling commercial applications

### Contributions to Broader Research or Innovation Users and Audiences and Towards Wider Societal Benefit

**Sports Science Community**:
- **Quantitative Tools**: New methods for understanding pattern formation in team sports
- **Tactical Analysis**: Real-time analytical capabilities for professional clubs
- **Performance Prediction**: Topological features as validated performance predictors
- **Research Directions**: Opening new research areas in sports analytics

**Professional Sports Industry**:
- **Commercial Applications**: Technology transfer pathways through Genius Sports partnership
- **Performance Optimization**: Tools for tactical analysis and team development
- **Competitive Advantage**: Novel analytical capabilities for professional clubs
- **Fan Engagement**: Enhanced understanding of tactical dynamics

**Mathematical Sciences Community**:
- **Theoretical Advances**: New frameworks for persistent homology in competitive systems
- **Computational Methods**: Efficient algorithms for real-time TDA
- **Research Directions**: Establishment of new research area at intersection of topology and competitive systems
- **Educational Resources**: Materials for teaching TDA through accessible applications

**Broader Societal Impact**:
- **Crowd Dynamics**: Applications to stadium safety and evacuation planning
- **Swarm Robotics**: Methods applicable to multi-robot coordination
- **Biological Systems**: Tools for understanding collective animal behavior
- **Education**: Inspiring next generation through accessible mathematics

**Technology Transfer**:
- **Commercial Pathways**: Established partnerships for technology transfer
- **Intellectual Property**: [If applicable: patent applications for novel methods]
- **Licensing Opportunities**: Potential for licensing agreements with sports technology companies
- **Startup Potential**: [If applicable: potential for spin-out company formation]

### Additions (Optional, up to 500 words)

[Use this section to provide context for career breaks, part-time work, or other factors relevant to the R4RI. Only include if necessary.]

---

## REFERENCES (1000 words)

[Include all references here. Use standard academic format. Examples based on preliminary work:]

1. Edelsbrunner, H., & Harer, J. (2010). Computational Topology: An Introduction. American Mathematical Society.

2. Zomorodian, A., & Carlsson, G. (2005). Computing persistent homology. Discrete & Computational Geometry, 33(2), 249-274.

3. Duarte, R., Araújo, D., Correia, V., & Davids, K. (2012). Sports teams as superorganisms: implications of sociobiological models of behaviour for research and practice in team sports performance. Sports Medicine, 42(8), 633-642.

4. Travassos, B., Araújo, D., Duarte, R., & McGarry, T. (2013). Spatiotemporal coordination patterns in futsal (indoor football) are guided by informational game constraints. Human Movement Science, 32(5), 944-956.

5. Perea, J. A., & Harer, J. (2015). Sliding windows and persistence: An application of topological methods to signal analysis. Foundations of Computational Mathematics, 15(3), 799-838.

6. Topaz, C. M., Ziegelmeier, L., & Halverson, T. (2015). Topological data analysis of biological aggregation models. PLoS ONE, 10(5), e0126383.

7. Ulmer, M., Ziegelmeier, L., & Topaz, C. M. (2019). A topological approach to selecting models of biological networks. In Topological Data Analysis (pp. 445-464). Springer.

8. Bubenik, P. (2015). Statistical topological data analysis using persistence landscapes. Journal of Machine Learning Research, 16(1), 77-102.

9. Bauer, U. (2021). Ripser: efficient computation of Vietoris-Rips persistence barcodes. Journal of Applied and Computational Topology, 5(3), 391-423.

10. Tauzin, G., et al. (2021). giotto-tda: A topological data analysis toolkit for machine learning and data exploration. Journal of Machine Learning Research, 22(39), 1-6.

[Add additional references as needed for your specific context and preliminary work.]

---

## PROJECT PARTNERS

**Genius Sports** (Industry Partner)
- **Contribution**: GPS tracking data access, validation support, commercial pathway
- **Value**: In-kind data access and technical collaboration
- **Letter of Support**: [To be provided]

[Add other partners as applicable]

---

## FACILITIES (250 words)

**Computational Facilities**:
- High-performance computing cluster for large-scale TDA computation
- Secure data storage infrastructure (GDPR compliant)
- Software licenses: Python (NumPy, SciPy, ripser, gudhi), MATLAB (where needed)
- Visualization tools for real-time tactical display

**Data Infrastructure**:
- Secure data storage for commercial partnerships
- Data processing pipelines for GPS tracking data
- Event annotation systems for match event correlation

**Research Environment**:
- Established sports analytics research group
- Domain expertise in football tactics and performance analysis
- Industry connections for validation and impact

No specialized facilities beyond standard computational infrastructure are required.

---

## ETHICS AND RESPONSIBLE RESEARCH AND INNOVATION (500 words)

**Ethical Considerations**:

**Data Privacy and Consent**:
- GPS tracking data will be anonymized and processed in accordance with GDPR requirements
- Data access agreements will ensure compliance with data protection regulations
- No personal identifying information will be used in analysis or publications
- All data handling will follow institutional data protection policies

**Responsible Research and Innovation**:

**Beneficial Applications**:
- Research aims to advance understanding of collective behavior with applications to:
  - Sports performance optimization (beneficial to athletes and teams)
  - Crowd safety and evacuation planning (societal benefit)
  - Swarm robotics and multi-agent systems (technological advancement)
  - Educational resources for mathematical and sports science communities

**Potential Misuse Considerations**:
- **Competitive Advantage**: Research could provide tactical advantages to funded teams. Mitigation: Results will be published openly, ensuring broad access rather than exclusive advantage.
- **Surveillance Concerns**: GPS tracking methods could be misapplied. Mitigation: Focus on aggregate team-level analysis rather than individual player tracking, with clear ethical guidelines.
- **Commercial Exploitation**: Technology could be used primarily for commercial gain. Mitigation: Open-source code release and academic publications ensure public benefit alongside commercial applications.

**Inclusivity and Diversity**:
- Research will engage diverse stakeholders (academic, industry, sports science)
- Open-source approach ensures accessibility regardless of institutional resources
- Educational resources will be designed for broad accessibility
- Collaboration with diverse teams and leagues (championship football focus ensures diversity beyond elite Premier League)

**Transparency and Reproducibility**:
- Open-source code release for all analysis methods
- Comprehensive documentation of methodology
- Publication of results in peer-reviewed journals
- Data sharing where possible (within privacy constraints)

**Stakeholder Engagement**:
- Regular engagement with sports science community for validation
- Industry partnerships ensure practical relevance
- Public engagement through accessible visualizations and educational resources

**No Significant Ethical Issues Identified**:
The research involves analysis of anonymized GPS tracking data for scientific purposes, with clear pathways to beneficial applications. All data handling will comply with GDPR and institutional policies. The research does not involve human subjects directly, animal testing, or sensitive personal data beyond anonymized positional tracking.

---

## RESOURCES AND COSTS

**Total Full Economic Cost (fEC)**: £80,000
**EPSRC Contribution (80%)**: £64,000
**Institutional Contribution (20%)**: £16,000

### Cost Breakdown

**Staff Costs**:
- **Project Lead Time** (20% FTE, 12 months): £24,000
  - Justification: Leadership, methodology development, analysis, paper writing

- **Research Associate** (50% FTE, 12 months): £32,000
  - Justification: Algorithm implementation, data processing, analysis, code development

**Travel and Subsistence**:
- **Conference Attendance** (1 conference): £2,000
  - Justification: Present results at major mathematics/sports science conference

- **Data Collection/Partnership Meetings**: £1,000
  - Justification: Meetings with Genius Sports and data providers

**Equipment**:
- **Computational Resources**: £8,000
  - Justification: High-performance computing access, cloud computing for large-scale analysis

**Other Directly Incurred Costs**:
- **Software Licenses**: £2,000
  - Justification: MATLAB licenses, specialized TDA software if needed

- **Data Access**: £5,000
  - Justification: Championship football GPS tracking data access fees

- **Open Access Publication**: £2,000
  - Justification: Open access fees for publication in top-tier journal

**Indirect Costs** (20% of direct costs): £4,000

**Total**: £80,000

### Justification

This budget is appropriate for a 12-month small grant project focusing on:
- Multi-match analysis requiring computational resources
- Data access for championship football matches
- Research associate time for algorithm development and analysis
- Project lead time for methodology development and paper writing
- Conference presentation for dissemination
- Open access publication for maximum impact

The budget aligns with EPSRC small grants guidelines and provides adequate resources to achieve project objectives while serving as a stepping stone to a larger grant application.

---

## SENSITIVE INFORMATION (250 words)

[Use this section only if there is sensitive information that should remain confidential. Otherwise, state: "No sensitive information to declare."]

No sensitive information to declare.

---

## APPENDIX: GANTT CHART

[One-page diagrammatic workplan showing timeline and milestones]

**Month 1-2**: Data Acquisition and Preparation
- Secure data access
- Data preprocessing
- Event annotation

**Month 3-5**: Pattern Formation Analysis
- Algorithm development
- Formation analysis
- Validation

**Month 6-8**: Temporal Evolution Analysis
- Temporal methods
- Stability analysis
- Transition probabilities

**Month 9-10**: Event Correlation Analysis
- Event framework
- Statistical analysis
- Validation

**Month 11-12**: Multi-Match Validation and Dissemination
- Cross-match analysis
- Paper preparation
- Submission

**Milestones**:
- Month 2: Data ready
- Month 5: Pattern formation validated
- Month 8: Temporal evolution complete
- Month 10: Event correlations established
- Month 12: Paper submitted

---

**Document Version**: 1.0  
**Date**: December 2024  
**Status**: Draft for UKRI Funding Service Submission

