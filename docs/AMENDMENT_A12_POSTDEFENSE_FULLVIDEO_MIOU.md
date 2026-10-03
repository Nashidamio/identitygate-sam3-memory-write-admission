# Amendment A12 - Post-Defense Full-Video Segmentation Evaluation

Date: 2026-10-04

Status: FROZEN WHEN THE COMMIT INTRODUCING THIS FILE IS COMMITTED TO main

## 1. Motivation

Defense feedback requested a direct measurement of whether selective memory
writing improves ordinary end-to-end segmentation/tracking quality relative
to vanilla frozen SAM 3, rather than relying only on the recovery-specific
POR@30 endpoint.

This amendment adds a supplementary post-defense evaluation. It does not
alter, replace, reinterpret, or rerun the frozen EXP053/EXP054 confirmatory
TEST campaign.

## 2. Compared methods

Only the following frozen methods are compared:

- B0: vanilla frozen SAM 3.
- B2: frozen learned quality-plus-temporal gate.

B2 uses the already-frozen threshold tau = 0.1.

No retraining, threshold search, calibration, feature change, or architecture
change is permitted.

## 3. Supplementary cohort

Candidate population:

- the 1,170-video EXP044 primary eligible population.

Excluded before sampling:

- 40 Fresh DEV videos;
- 80 HARD_TEST80 videos;
- 40 REPRESENTATIVE_TEST40 videos.

The three sets are mutually disjoint and all belong to the primary eligible
population.

This leaves 1,010 untouched eligible videos.

EXP055 will uniformly sample 80 videos without replacement from these 1,010
videos using deterministic random seed 55.

Selection is outcome-independent. No SAM or gate prediction may be inspected
before the 80-video membership is frozen.

## 4. Full-video segmentation metric

For every selected video, every tracked object, and every non-conditioning
frame:

- frame 0 is excluded because it is initialized directly from the GT prompt;
- an object-frame is evaluable only when the target is GT-visible;
- prediction is the binary tracker mask already produced by the frozen
  tracking pipeline;
- Jaccard / IoU is:

    intersection(prediction, target_GT)
    /
    union(prediction, target_GT)

The primary supplementary point estimate is the mean IoU across all evaluable
GT-visible object-frames.

Also report a video-balanced mean obtained by first averaging evaluable
object-frame IoUs within each video and then averaging across videos.

## 5. Comparison and uncertainty

The supplementary contrast is:

    mean_IoU(B2) - mean_IoU(B0)

The same 80 videos are used for both methods.

Uncertainty must preserve video clustering using a paired video-clustered
bootstrap with 50,000 replicates.

Both point estimate and 95% confidence interval must be reported.

## 6. Claim boundary

EXP055 is supplementary post-defense evidence.

It is not preregistered confirmatory TEST evidence and must not replace or
modify the frozen POR@30 conclusions from EXP053/EXP054.

A positive, null, or negative result must all be reported.

The result may support only the bounded statement about full-video
segmentation quality for frozen B0 versus frozen B2 on this supplementary
MOSEv2 cohort.
