# CVPR Template Provenance

Date: 2026-10-04

Status: PROVISIONAL

This repository does not currently claim to contain the official CVPR 2027
author kit.

For layout, page-pressure, and compile preparation, the paper temporarily
uses a pinned snapshot of the official CVPR/ICCV/3DV author-kit repository:

- Upstream: https://github.com/cvpr-org/author-kit.git
- Pinned commit: 291758547e923160eb4d37079b7b9f0dfce82355
- Upstream commit date: 2026-05-27T18:26:46-07:00
- Upstream commit subject: teaser w/ strip and preamble tweaks (#65)

At the time of freezing this snapshot, the upstream README explicitly listed
the latest CVPR update as CVPR 2026, the template main.tex identified itself
as the CVPR 2026 paper template, and cvpr.sty declared a 2026 IEEE CVPR
package. Therefore this snapshot MUST NOT be described as the official CVPR
2027 template.

Purpose of this provisional snapshot:
- establish reproducible LaTeX formatting;
- expose page-pressure and figure-placement issues early;
- enable compile and submission-package QA before the official CVPR 2027
  author kit is available.

Replacement rule:
When the official cvpr-org/author-kit repository explicitly publishes a
CVPR 2027 version, add that version in a new commit, record its exact upstream
commit and hashes, migrate the paper, and rerun compile/layout/submission QA.
Do not rewrite the history of this provisional snapshot.

The manuscript main.tex was not migrated as part of the provenance-freeze
step.
