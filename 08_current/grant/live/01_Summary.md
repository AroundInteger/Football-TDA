# SUMMARY (JeS public summary) adervisorial


**Word limit: 550.** Paste the four sections below, including the headings (540 body words + 10 heading words = 550). Do not paste this header block. **Current:** 540 body / 550 with headings.

**Source:** `../LaySummary.docx`. Plain English for expert assignment; this text is made publicly available.

## Context

Two football teams compete by reshaping each other's organisation across several spatial scales at once: a pair pressing, a unit holding a line, and the space a team covers. Structure at one scale need not be visible at another. A local grouping can vanish in the whole-team view, and a gap in the team's shape can be invisible among local clusters. Without separating those levels, a small regrouping and a team-wide change look the same. Telling them apart needs every player's position, at every moment, inside the pitch. A snapshot cannot show whether a cluster formed, held or dissolved, and a missing player can make a gap or cluster an artefact. Continuous tracking supplies that complete record, and coaches can check the measurements against the match.

This is the general problem of groups competing inside a bounded space, and football is where it can be measured and verified. This project builds the tools to measure those levels together and to track how competitive pressure reshapes them. The same problem arises in other bounded settings, such as a contested animal territory.

## The Challenge

Two obstacles block existing approaches.

The first is scale. Standard shape-analysis tools return a single measurement that mixes every organisational level into one picture, like a map locked to one zoom. Separating those levels is a prerequisite for analysis, yet no established method exists.

The second is dependence. Most statistical tools assume consecutive observations are independent, as with coin flips. Competitive systems are not coin flips: each agent's movement responds to the other group and constrains what happens next. Treating that record as independent observations understates uncertainty. New theory is required for the way competitive movement cascades through time and space.

## Aims and Objectives

The project builds the mathematical foundations for shape-based analysis of competitive collective systems. These are groups of agents that share a bounded domain, each coordinating internally while responding to an opponent. A ten-match pilot recovers distinct organisational levels that respond to real match events. This grant scales that work across a Championship season (540 matches).

First, establish whether the multi-level measurements are stable enough to compare across matches at population scale, and show they capture information unavailable from team length, width and hull area.

Second, prove mathematical guarantees that the method can detect when collective organisation undergoes a structural transition, with a known error, rather than only describing the new state after it has occurred.

## Potential Applications and Benefits

This project will deliver football-validated theory and software: a scale-separated analysis that accounts for competitive dependence (successive observations are not independent). The primary output is a documented open-source package that computes multi-scale shape summaries from tracking data, released with a digital object identifier (DOI). Swansea City Association Football Club and StatsBomb co-develop the work. The club receives checkable structural measures of pressing, formation gaps and defensive-line organisation. StatsBomb receives features beyond conventional geometry.

The same organisational problem, competing groups inside a bounded domain, appears in spatial predator–prey dynamics, including competition between tumour cells and immune cells. A second later target is competitive logistics with autonomous-fleet coordination. Neither is a deliverable of this award: transfer is a later step, once interaction lengths are re-derived. Full-season results and theory form an evidence pack for a follow-on Standard Grant, through mathematical-oncology collaborations specific to that programme.
