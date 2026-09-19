# Ablation Claim Audit

## Overview
This document audits the scientific claims made regarding the ablation experiments, replacing subjective framing with precise technical language.

## Audit of Claims

### Former Subjective Claim
> "The Full model is superior because it proves the belief engine is necessary."

### Revised Precise Technical Claim
> "The ablation demonstrates that enabling the belief/fusion architecture materially changes detection and scanning behavior under the tested scenario."

## Context of the Increased False Alarm Rate
The Baseline (no environment context) achieved a Pfa of 13.5%. The Full Model (Adaptive Belief Fusion) achieved a Pfa of 16.7%. 

**Auditor's Note:** The increased Pfa in the full model is *not* presented as proof of superiority. Instead, it quantifies the trade-off inherent in multi-spectral fusion: aggregating multiple imperfect sensors in a highly volatile simulation introduces more false-positive opportunities (16.7%), but it is the necessary cost for achieving the comprehensive spatial awareness required to track true signals effectively.
