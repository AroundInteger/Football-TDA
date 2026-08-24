# SUMMARY (JeS public summary)

**Word limit:** 550. **Current:** 489.  
**Source:** `../LaySummary.docx`. Plain English for expert assignment; this text is made publicly available.

## Context

When groups of agents compete inside a bounded space, they organise at several spatial scales at once. Local clusters, larger groupings and the envelope of the whole collection coexist, and each scale hides structure the others cannot see. The situation is like a map that must be read at street, neighbourhood and city zoom simultaneously. This project builds the mathematical tools to measure those levels together and to track how competitive pressure reshapes them. Football is the testbed because every player is continuously tracked on a fixed pitch. Other systems share the same organisational problem once their relevant boundary is identified: it may be imposed, as with a pitch, or arise from the agents themselves, as with a contested animal territory.

## The Challenge

Two obstacles block existing approaches.

The first is scale. Standard shape-analysis tools return a single measurement that conflates every organisational level into one picture, like a map locked to one zoom. Separating those levels in a principled way is a prerequisite for analysis, yet no established method exists.

The second is dependence. Most statistical tools assume consecutive observations are independent, as with coin flips. Competitive systems are not coin flips: each agent's movement responds to an opponent and constrains what happens next. Treating that record as independent observations yields invalid inference. New theory is required for the way competitive movement cascades through time and space.

## Aims and Objectives

The project builds the mathematical foundations for shape-based analysis of competitive collective systems, using professional football as a testbed where all players are tracked and domain experts can check the results. A 10-match pilot has shown that the framework recovers distinct organisational levels and that those levels respond to real match events. This grant scales that foundation across a full Championship season (~540 matches) through two research objectives.

First, establish whether the multi-level measurements are stably comparable across matches at population scale, and show that they capture information unavailable from conventional statistics. Second, prove mathematical guarantees that the method can detect when collective organisation undergoes a structural transition, with known error, rather than only describing the new state after it has occurred. Full-season results and theoretical foundations are compiled into an evidence pack for a follow-on Standard Grant that tests whether those guarantees transfer to a second bounded competitive system.

## Potential Applications and Benefits

This award delivers the football-validated theory and software. Transfer to another system is a later step, once interaction lengths are re-derived. The follow-on Standard Grant will test whether those guarantees transfer to spatial predator–prey dynamics, including cellular competition relevant to cancer biology through the team's mathematical-oncology expertise.

The primary output is a documented, containerised open-source package that computes multi-scale topological summaries from tracking data, released with a DOI. Swansea City AFC and StatsBomb co-develop the work: the club receives structural measures of pressing, formation gaps and defensive-line organisation, while the data partner receives a candidate feature set beyond conventional geometry. The evidence pack supports the follow-on Standard Grant.
