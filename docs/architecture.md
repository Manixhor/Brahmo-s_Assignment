# Architecture Notes

## Goal

Transform a pre-filtered candidate set into a context string that is:

- under a hard total token ceiling
- ordered for model usefulness
- safe by construction for critical constraints
- explainable in an interview setting

## Pipeline

1. Load seeded organization, user, patient, and 28 candidate nodes.
2. Normalize importance scores and generate composition rationale.
3. Assign each node an initial compression level from distance, except `CONSTRAINT` nodes which stay `FULL`.
4. Assemble nodes into the fixed 8-block layout.
5. Build the context string and count total tokens across:
   - system prompt reserve
   - context string
   - user message reserve
6. If over budget, iteratively compress the lowest-injection non-constraint node.
7. Stop when:
   - total fits under budget, or
   - every non-constraint has been omitted and only protected content remains

## Design choices

### Deterministic compression

The assessment is about budget-safe composition, not creative summarization. A deterministic engine is easier to reason about, test, and defend during review.

### Fixed block order

The model should always encounter high-safety and recent-decision context before incidental facts. Fixed block ordering makes that guarantee explicit.

### Constraint protection

`CONSTRAINT` is treated as a product-safety rule, not a formatting preference. If constraints alone exceed the budget, the output includes a review flag rather than silently compressing them.

### Conservative token fallback

If `tiktoken` is unavailable, the fallback tokenizer slightly overestimates typical usage. That makes local execution robust while preserving the spirit of preflight budget enforcement.

## Complexity

For `n` nodes:

- initial sorting and assembly: `O(n log n)`
- each compression pass: `O(n)` selection with small constants
- total passes are bounded by `3n` because each node has four states: `FULL`, `COMPRESSED`, `CONSTRAINT_ONLY`, `OMIT`

At the assessment scale of 28 nodes, this is comfortably fast and easy to inspect.

## Edge cases handled

- Budget already fits with all nodes in initial state
- Only constraints remain and budget still fails
- Empty blocks are omitted except the open-questions placeholder
- Nodes with out-of-range weights are clamped into valid bounds

## What I would build next

- FastAPI endpoint returning composition metadata
- React visualization wired to live composition output
- Per-block token allotment strategy
- Historical analytics showing which node categories are most often omitted
