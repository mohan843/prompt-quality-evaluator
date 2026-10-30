# Prompt Quality Evaluator

An interpretable generative-AI utility that scores prompts against a practical rubric for specificity, context, constraints, output format, and examples.

## Overview

A well-structured prompt gives a language model enough context to produce useful, consistent output. This project turns common prompt-engineering guidance into a small, explainable evaluator that returns a score, label, strengths, and actionable suggestions.

## Problem statement

Given a prompt, identify missing quality signals and estimate whether it is basic, developing, strong, or excellent for generative-AI use.

## Features

- Five-dimension prompt rubric.
- Deterministic, transparent scoring from 0 to 100.
- Actionable suggestions for missing dimensions.
- CLI and comparison helper for prompt experiments.
- Standard-library-only implementation and tests.

## Technology stack

- Python 3.10+
- Generative-AI prompt engineering
- Text tokenization and rule-based feature extraction
- `argparse`, `dataclasses`, and `re`
- `unittest` for automated testing

## Installation

```bash
git clone https://github.com/mohan843/prompt-quality-evaluator.git
cd prompt-quality-evaluator
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

No third-party runtime dependencies are required.

## Execution

```bash
python evaluator.py "Summarize this article."
```

Detailed prompt example:

```bash
python evaluator.py "You are a data analyst. Given the sales context, explain changes for a manager. Return a JSON table, use only supplied data, keep it under 200 words, and show one example."
```

## Testing

```bash
python -m unittest discover -s tests -v
```

## Sample output

```text
Prompt quality: 0/100 (basic)
Strengths: None yet
Suggestions: Add specificity. Add context. Add constraints. Add output format. Add examples.
```

## Limitations and responsible use

This is a deterministic teaching tool, not a measure of model performance or a guarantee of output quality. Different models and tasks need different prompt structures. Treat the score as a checklist and validate prompts empirically.

## Future improvements

- Add task-specific rubrics for coding, extraction, and image generation.
- Learn weights from human-rated prompt/output pairs.
- Add semantic coverage using embeddings.
- Support prompt versioning and A/B evaluation.
- Add model-specific recommendations and privacy checks.
