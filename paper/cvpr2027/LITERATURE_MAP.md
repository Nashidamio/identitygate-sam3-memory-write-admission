# CVPR 2027 Literature and Citation Map

Date: 2026-10-04

Status: WORKING CITATION CONTROL ARTIFACT.

Purpose:
map already-verified reference identities to the scientific roles needed by
the CVPR manuscript without reopening completed literature audits.

This file does not establish novelty by absence of prior work.

## Citation discipline

- Do not re-audit papers already marked audited unless contradictory evidence
  appears.
- Do not fill missing authors, venue, or bibliographic fields from memory.
- A reference enters references.bib only after its exact bibliographic metadata
  is transferred from an audited source or independently verified.
- A reference enters the final bibliography only if the manuscript actually
  cites it.
- Do not use "first", "no prior work", or equivalent novelty language from
  this map alone.

## Mandatory substrate and dataset citations

### SAM3

Citation key: SAM3
Exact title: SAM 3: Segment Anything with Concepts
Identifier: arXiv:2511.16719
Paper role: frozen segmentation/tracking substrate.
Required distinction:
the paper uses SAM 3 VOS/PVS, not SAM 3.1 Multiplex.
Bibliographic status:
IDENTITY_VERIFIED / AUTHORS_AND_FINAL_VENUE_METADATA_OPEN.

### MOSEv2

Citation key: MOSEv2
Exact title:
MOSEv2: A More Challenging Dataset for Video Object Segmentation in Complex Scenes
Identifier: arXiv:2508.05630
Paper role: primary evaluation dataset.
Audit status: ALREADY_AUDITED.
Bibliographic status:
TITLE_AND_IDENTIFIER_VERIFIED / AUTHORS_AND_FINAL_VENUE_METADATA_OPEN.

## Core memory-selection related work

### QDMN

Citation key: QDMN
Exact title: Learning Quality-aware Dynamic Memory for Video Object Segmentation
Identifier: arXiv:2207.07922
Audit status: ALREADY_AUDITED.
Scientific role:
learned quality-aware memory control in pre-foundation-model VOS.
Safe comparison:
supports the premise that learned signals can govern candidate memory quality.
Do not claim:
that QDMN answers the frozen-SAM-3 quality-versus-identity question.

### DAM4SAM

Citation key: DAM4SAM
Exact title: Distractor-Aware Memory-Based Visual Object Tracking
Identifier: arXiv:2509.13864
Audit status: ALREADY_AUDITED.
Scientific role:
distractor-aware and structured memory as an explicit tracking design problem.
Safe comparison:
shows that SAM-family memory governance and distractor handling have prior art.
Do not claim:
that the paper reproduces DAM4SAM or that memory governance is absent from
prior work.

### SENTRY

Citation key: SENTRY
Exact title:
SENTRY: SAM2-Enhanced Neighbor-Aware and Temporally Reasoned Memory for Visual Tracking
Identifier: arXiv:2606.24449
Audit status: ALREADY_AUDITED.
Scientific role:
training-free trajectory/cycle-style candidate validation before memory use.
Safe comparison:
supports write-oriented reliability validation as a contemporary design axis.
Distinction:
our study compares signal families under a frozen controlled protocol rather
than adopting SENTRY trajectory/geometric validation.

### SAM3-DMS

Citation key: SAM3-DMS
Exact title:
SAM3-DMS: Decoupled Memory Selection for Multi-target Video Segmentation of SAM3
Identifier: arXiv:2601.09699
Audit status: ALREADY_AUDITED.
Scientific role:
per-object confidence/reliability-based memory selection in a SAM 3 setting.
Safe comparison:
closest reliability-oriented contemporary SAM 3 neighbor.
Required boundary:
B5 is a thesis-internal DMS-lite write-side comparator and is not an exact
reproduction of SAM3-DMS.

### RethinkingMemory

Citation key: RethinkingMemory
Exact title: Rethinking Memory Design in SAM-Based Visual Object Tracking
Identifier: arXiv:2512.22624
Audit status: ALREADY_AUDITED.
Scientific role:
memory architecture and memory-policy choices in SAM-generation trackers.
Safe comparison:
supports memory policy as an independent design axis.
Distinction:
our paper fixes the SAM 3 substrate and studies information available to the
write-admission decision.

## Temporal and reliability supporting work

### SAMURAI

Citation key: SAMURAI
Exact title:
SAMURAI: Adapting Segment Anything Model for Zero-Shot Visual Tracking with Motion-Aware Memory
Identifier: arXiv:2411.11922
Identity status: VERIFIED.
Scientific role:
motion-aware / temporal evidence for memory selection.
Distinction:
training-free heuristic neighbor rather than the supervised signal-family
comparison used here.
Bibliographic status:
AUTHORS_AND_FINAL_VENUE_METADATA_OPEN.

### OAMVOS

Citation key: OAMVOS
Exact title: OAMVOS:2nd Report for 5th PVUW MOSE Track
Identifier: arXiv:2604.22837
Audit status: ALREADY_AUDITED.
Scientific role:
reliability / occlusion-aware heuristic neighbor and provenance context for
the manual B1 design.
Required boundary:
B1 is not described as a reproduction of OAMVOS.

## Identity-aware and competitor-reasoning work

### AOT

Citation key: AOT
Exact title: Associating Objects with Transformers for Video Object Segmentation
Identifier: arXiv:2106.02638 / NeurIPS 2021
Identity status: VERIFIED.
Scientific role:
object-specific identity representation and identity-aware propagation.
Bibliographic status:
AUTHORS_METADATA_OPEN.

### DeAOT

Citation key: DeAOT
Exact title:
Decoupling Features in Hierarchical Propagation for Video Object Segmentation
Identifier: arXiv:2210.09782 / NeurIPS 2022
Identity status: VERIFIED.
Scientific role:
identity-aware propagation background.
Bibliographic status:
AUTHORS_METADATA_OPEN.

### AOST

Citation key: AOST
Exact title: Scalable Video Object Segmentation with Identification Mechanism
Identifier: arXiv:2203.11442 / TPAMI
Identity status: VERIFIED.
Scientific role:
identification mechanism in VOS.
Bibliographic status:
AUTHORS_AND_FINAL_YEAR_METADATA_OPEN.

### ReMeDI-SAM3

Citation key: ReMeDI-SAM3
Exact title:
Memory-Enhanced SAM3 for Occlusion-Robust Surgical Instrument Segmentation
Identifier: arXiv:2512.16880
Identity status: VERIFIED.
Scientific role:
recent identity / memory / occlusion-aware supporting neighbor.
Bibliographic status:
AUTHORS_AND_FINAL_VENUE_METADATA_OPEN.

### SurgSLOT

Citation key: SurgSLOT
Exact title:
SurgSLOT: Segment Anything in Surgical Videos via Semantic Long-term Tracking
Identifier: arXiv:2511.16618v2
Audit status: ALREADY_AUDITED.
Scientific role:
semantic identity / long-term tracking supporting neighbor.

### CMR

Citation key: CMR
Exact title:
Competitive Memory Readout for Robust Video Object Segmentation:
2nd Place Technical Report for the MOSEv2 Track of the 8th LSVOS Challenge
Identifier: arXiv:2608.22064
Audit status: ALREADY_AUDITED.
Scientific role:
competitor-relative evidence and relational identity reasoning.
Required distinction:
primarily a memory-readout neighbor, not the same write-admission mechanism.

### VOS-Agent

Citation key: VOS-Agent
Exact title:
VOS-Agent: The 1st Place Solution for the 8th LSVOS Challenge (MOSEv2 Track)
Identifier: arXiv:2608.12721
Audit status: ALREADY_AUDITED.
Scientific role:
recent MOSEv2/VOS supporting context.

## General VOS background candidates

These identities are verified, but each should be retained in the final CVPR
bibliography only if the corresponding background sentence remains in the
compressed paper.

### STM

Citation key: STM
Exact title: Video Object Segmentation Using Space-Time Memory Networks
Identifier: ICCV 2019
Identity status: VERIFIED.
Paper-use status: BACKGROUND_CANDIDATE.

### STCN

Citation key: STCN
Exact title:
Rethinking Space-Time Networks with Improved Memory Coverage for Efficient Video Object Segmentation
Identifier: NeurIPS 2021
Identity status: VERIFIED.
Paper-use status: BACKGROUND_CANDIDATE.

### MiVOS

Citation key: MiVOS
Exact title:
Modular Interactive Video Object Segmentation:
Interaction-to-Mask, Propagation and Difference-Aware Fusion
Identifier: CVPR 2021
Identity status: VERIFIED.
Paper-use status: BACKGROUND_CANDIDATE.

### XMem

Citation key: XMem
Exact title:
XMem: Long-Term Video Object Segmentation with an Atkinson-Shiffrin Memory Model
Identifier: arXiv:2207.07115
Identity status: VERIFIED.
Paper-use status: BACKGROUND_CANDIDATE.

### Cutie

Citation key: Cutie
Exact title: Putting the Object Back into Video Object Segmentation
Identifier: arXiv:2310.12982 / CVPR 2024
Identity status: VERIFIED.
Paper-use status: BACKGROUND_CANDIDATE.

## Paper positioning supported by the audited literature

Safe high-level positioning:

The paper is a controlled explanatory study of memory-write information under
a fixed SAM 3 substrate. It compares the incremental value of
quality-temporal, self-identity, and competitor-relative identity information
under an explicit write-budget protocol.

The literature establishes that:
- learned quality-aware memory control exists;
- temporal and motion-based memory selection exists;
- distractor-aware and structured memory mechanisms exist;
- trajectory/cycle-based validation exists;
- SAM 3 reliability-based memory selection exists;
- identity-aware propagation and competitor-relative reasoning exist.

Therefore the paper must not claim that memory filtering, identity-aware
tracking, or SAM-family memory management is itself new.

## Metadata work remaining before references.bib

OPEN_METADATA:
- exact authors for all entries;
- final venue/year where the audited project assets do not already preserve it;
- canonical BibTeX formatting;
- publication-vs-arXiv preference for entries with both forms.

No field above may be filled from memory.


## Metadata correction A1 - ReMeDI-SAM3 title

Date: 2026-10-04

Status: VERIFIED METADATA CORRECTION.

New external evidence from the official arXiv record for identifier
2512.16880 contradicts the earlier title preserved in the project reference
resolution seed.

SUPERSEDED title:
Memory-Enhanced SAM3 for Occlusion-Robust Surgical Instrument Segmentation

VERIFIED current arXiv title:
ReMeDI: Refined Memory for Disambiguation of Identities with SAM3 in Surgical Segmentation

VERIFIED authors:
Valay Bundele; Mehran Hosseinzadeh; Hendrik P.A. Lensch.

Identifier:
arXiv:2512.16880.

Current arXiv version inspected:
v2, revised 2026-03-08.

Scientific role is unchanged:
ReMeDI-SAM3 remains a supporting identity / memory / occlusion-aware
neighbour. This correction changes bibliographic metadata only and does not
alter any thesis experimental conclusion or novelty claim.

For references.bib and manuscript citations, use the VERIFIED current arXiv
title above rather than the superseded project-seed title.
