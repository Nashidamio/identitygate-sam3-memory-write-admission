# CVPR 2027 Paper Scope and Claim Ledger

Date: 2026-10-04

Status: WORKING PUBLICATION SCOPE.
This document constrains manuscript claims but does not alter any frozen
experimental conclusion or preregistration.

## Target

- Venue: CVPR 2027 main conference.
- Working title:
  When Should SAM 3 Write to Memory?
  A Controlled Study of Signal-Informed Memory Admission for
  Video Object Segmentation
- Scientific substrate:
  frozen SAM 3 VOS/PVS with closed-loop control over candidate
  memory admission.
- Locked research question:
  "What information should a memory-write gate use — quality signals,
  temporal signals, or identity signals?"

## Central paper framing

Memory-write gating is evaluated as a controlled signal-selection problem,
not merely as a modification that writes less often.

The paper asks which information is supported for memory admission while
controlling for write rate, leakage, and video-level statistical dependence.

## Primary supported positive claim

The strongest confirmatory positive result is the matched comparison of the
learned quality-temporal gate B2 against manual gate B1 on HARD TEST.

- B2 minus B1 POR@30 delta: +0.02964.
- Video-clustered BCa 95% CI: [0.00612, 0.06430].
- Realized write-rate difference: 0.00335.
- Matched-rate tolerance: 0.02.

Interpretation:
under the frozen evaluation protocol, learned quality-temporal signals
improve post-occlusion recovery relative to the matched manual policy.

## Identity-signal conclusion

The tested native SAM 3 pointer identity signals do not establish an
incremental recovery benefit.

The cleanest identity-family comparison is B3-R versus B3-S:

- POR@30 delta: 0.00000.
- Video-clustered BCa 95% CI: [-0.01129, 0.01431].
- The comparison is write-rate compatible.

B3-S versus B2 is not used as a clean causal identity comparison because
its realized write-rate difference exceeded the frozen matching tolerance.

Do not generalize this result to:
- identity information in general;
- external re-identification embeddings;
- learned identity representations;
- other VOS substrates.

## Native B0 boundary

B0 writes at every eligible opportunity and therefore operates at a
substantially different write rate from the gated systems.

B0 comparisons are descriptive unless a valid budget-matched design exists.

Do not use the headline claim:
"IdentityGate beats vanilla SAM 3."

## Exact-budget neutral-selector control

Exact-budget neutral-selector controls are retained as a first-class
evaluation result.

At the frozen Hard TEST operating points, the signal-informed policies do
not establish clear POR@30 superiority over arbitrary exact-budget neutral
schedules.

Interpretation:
write budget and admission timing are important confounds, and a gate should
not receive causal credit merely because it writes less often.

## Full-video segmentation-quality supplementary evidence

EXP055 is supplementary, post-defense, and nonconfirmatory.

Cohort:
- POSTDEFENSE_MIOU80.
- 80 outcome-independently sampled videos.
- 160 paired B0/B2 runs.
- 9,778 evaluable GT-visible non-conditioning object-frames.

Primary pooled object-frame mean IoU:
- B0: 0.7369431584723181.
- B2: 0.6781042863785702.
- B2 minus B0: -0.05883887209374783.
- Video-clustered BCa 95% CI:
  [-0.11845205735413418, 0.0016732381322542309].

Secondary video-balanced mean IoU:
- B0: 0.704008157300997.
- B2: 0.666728236623254.
- B2 minus B0: -0.037279920677743085.
- BCa 95% CI:
  [-0.099019818157226, 0.020909119806880407].

Interpretation:
the point estimates favor B0 for ordinary full-video mIoU, but both
confidence intervals include zero. EXP055 therefore establishes neither a
statistically reliable full-video mIoU improvement nor degradation for B2.

EXP055 does not modify the frozen confirmatory conclusions.

## Claims explicitly prohibited

Do not claim that:
- gating universally improves SAM 3;
- B2 is statistically superior to B0 under a matched write budget;
- native SAM 3 identity information is useless;
- identity signals in general do not help VOS;
- B3-S cleanly outperforms B2 due to identity;
- EXP055 proves that B2 degrades full-video segmentation quality;
- the post-defense EXP055 result is confirmatory TEST evidence;
- results generalize beyond the evaluated SAM 3 substrate and MOSEv2
  without new evidence.

## Intended contribution structure

1. A physically verified closed-loop memory-write intervention for a frozen
   SAM 3 VOS/PVS substrate.
2. A nested signal-family evaluation separating quality-temporal,
   self-identity, and competitor-relative identity information.
3. Leakage-controlled evaluation with matched write-rate requirements and
   video-clustered inference.
4. Exact-budget neutral controls showing why write frequency alone is not a
   sufficient explanation of policy quality.
5. A bounded empirical conclusion: quality-temporal evidence provides the
   strongest demonstrated basis for memory admission in the tested setting,
   while tested native pointer identity signals provide no established
   incremental recovery benefit.

## Publication discipline

- Negative and null results remain visible.
- No TEST retuning is permitted for manuscript improvement.
- No frozen experimental conclusion is rewritten for narrative convenience.
- Any new experiment must have an independently frozen protocol before
  outcome inspection.
- Manuscript wording must distinguish confirmatory evidence from
  supplementary post-defense evidence.
