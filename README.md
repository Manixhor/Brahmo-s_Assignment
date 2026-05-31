# BRAHMO's Assessment

A polished assessment submission for "Make Every Token Count": a deterministic composition engine that converts candidate nodes into a structured, budget-safe context string for AI injection.

## Why this version is strong

- Counts all three token sources before composition output is used: system prompt, assembled context, and user reserve
- Preserves all `CONSTRAINT` nodes at full fidelity, even under heavy budget pressure
- Uses fixed 8-block ordering so safety and decision context always appear before low-priority facts
- Shows graceful degradation through iterative compression instead of naive truncation
- Includes tests, demo scenarios, architecture notes, and sample data for the evaluator
- Includes [data_sources.md](/Users/mani/Documents/Blizo/data_sources.md:1) documenting provenance of the clinical-style demo data for BRAHMO's assessment

## Project layout

```text
.
├── README.md
├── data_sources.md
├── docs/
│   └── architecture.md
├── data/
│   └── seed_data.json
├── requirements.txt
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── styles.css
├── tests/
│   └── test_composition.py
└── backend/
    ├── demo.py
    └── composition/
        ├── __init__.py
        ├── block_assembler.py
        ├── budget_fitter.py
        ├── compressor.py
        ├── context_builder.py
        ├── importance_scorer.py
        ├── models.py
        └── token_counter.py
```

## Quick start

```bash
python3 -m unittest discover -s tests
python3 backend/demo.py --budget 4000
python3 backend/demo.py --budget 2000 --json
```

To open the lightweight frontend preview:

```bash
cd frontend
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

## Demo script

### Scenario 1: Full pipeline

```bash
python3 backend/demo.py --budget 4000
```

What to call out:

- 28 candidates enter the pipeline
- Compression starts from lowest injection weight non-constraints
- Protected constraints remain `FULL`
- Final total fits under the hard ceiling

### Scenario 2: Constraint protection

```bash
python3 backend/demo.py --budget 2600 --show-protected
```

What to call out:

- Distance does not override `CONSTRAINT` safety
- Non-constraints are compressed and omitted first
- If only constraints remain and budget is still exceeded, the system raises a human-review flag

### Scenario 3: Retrieval vs injection

```bash
python3 backend/demo.py --budget 4000 --focus N-G01 N-O05
```

What to call out:

- `retrieval_weight` answers "should this be present in the candidate set?"
- `injection_weight` answers "how much token space should this node get?"
- Important facts can still be omitted if they are low-value for injection

### Scenario 4: Budget adaptation

```bash
python3 backend/demo.py --budget 2000
```

What to call out:

- More nodes move through `FULL -> COMPRESSED -> CONSTRAINT_ONLY -> OMIT`
- Composition degrades gracefully
- Constraints remain fully preserved

## Hiring-focused talking points

- The engine is deterministic and auditable, which is safer than asking an LLM to decide what to trim
- Compression is traceable pass by pass, making debugging and product review easier
- The code handles the hardest edge case explicitly: protected constraints alone can exceed the budget
- The frontend is intentionally lightweight; the core engineering value is in correctness, explainability, and safety

## Notes

- `tiktoken` is optional. If installed, it is used automatically. Otherwise the app falls back to a conservative heuristic tokenizer so the project still runs in a clean environment.
- The seeded dataset is synthetic but shaped to match the assessment narrative.
- For submission, include a Loom video with audio and send the repository link as a new email to `rohitha@astroum.ai`.
# Brahmo-s_Assignment
