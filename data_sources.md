# Data Sources

## Important note

This assessment project uses synthetic demonstration data shaped from the assessment brief. It is intentionally not built from live patient records or proprietary hospital data.

## Clinical and domain content provenance

### Source categories used

- The assessment narrative itself
- General, well-known clinical safety patterns used only for demo realism
- Synthetic expansions written for the composition-engine showcase

### Node-by-node sourcing approach

| Node group | Source | Notes |
|---|---|---|
| Global `CONSTRAINT` nodes | Assessment story + synthetic elaboration | Includes examples like anticoagulation-safe analgesia, sedation sign-off, DVT continuity, and red-flag escalation. These were created to demonstrate protected high-priority context handling. |
| Active patient `CONSTRAINT` nodes | Assessment story + synthetic elaboration | Includes patient-specific NSAID avoidance and follow-up monitoring rules. |
| `DECISION` nodes | Synthetic | Created to simulate recent consultant, nursing, pharmacy, and physiotherapy decisions for the 8-block assembly demo. |
| `FACT` nodes | Synthetic | Created to simulate patient condition, post-op status, symptoms, and low-priority operational facts for compression behavior. |
| `ANTI_PATTERN` nodes | Synthetic | Created to demonstrate composition guardrails and explainability. |
| `REVIEW_REQUIRED` or stale-review nodes | Synthetic | Created to exercise stale-flag behavior and human-review pathways. |

## Why synthetic data was used

- The assessment asks for a working composition system, not a validated clinical decision-support product.
- Synthetic data avoids privacy concerns and keeps the submission safe to share publicly in a Git repository.
- The main engineering value here is deterministic token budgeting, block ordering, constraint protection, and explainable compression.

## What is not claimed

- This repository does not claim medical correctness or production-readiness for any treatment recommendation.
- This repository does not use real hospital records, real patient data, or proprietary BRAHMO knowledge nodes.
- The seeded nodes are demonstration inputs for system behavior only.

## If asked during the demo

Recommended explanation:

> I used synthetic clinical-style nodes because the assessment is evaluating the composition engine, not live medical-data sourcing. I documented that clearly, kept the rules realistic enough to test safety-sensitive prioritization, and avoided implying this is production clinical guidance.
