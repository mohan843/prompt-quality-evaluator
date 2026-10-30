"""Score generative-AI prompts with an interpretable quality rubric."""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from typing import Sequence

WORD_RE = re.compile(r"[a-zA-Z0-9']+")
CRITERIA = ("specificity", "context", "constraints", "output_format", "examples")


@dataclass(frozen=True)
class PromptReport:
    score: int
    label: str
    strengths: tuple[str, ...]
    suggestions: tuple[str, ...]


def words(text: str) -> list[str]:
    return WORD_RE.findall(text.lower())


def has_any(text: str, phrases: Sequence[str]) -> bool:
    lowered = text.lower()
    return any(phrase in lowered for phrase in phrases)


def evaluate(prompt: str) -> PromptReport:
    if not prompt.strip():
        raise ValueError("Prompt must not be empty")
    tokens = words(prompt)
    points = {criterion: 0 for criterion in CRITERIA}
    if len(tokens) >= 12:
        points["specificity"] = 2
    elif len(tokens) >= 6:
        points["specificity"] = 1
    if has_any(prompt, ("background", "context", "for a", "audience", "because")):
        points["context"] = 2
    if has_any(prompt, ("must", "do not", "limit", "under", "include", "avoid")):
        points["constraints"] = 2
    if has_any(prompt, ("json", "table", "bullet", "format", "steps", "columns")):
        points["output_format"] = 2
    if has_any(prompt, ("example", "sample", "like this", "input:", "output:")):
        points["examples"] = 2
    score = round(sum(points.values()) / (len(CRITERIA) * 2) * 100)
    label = "excellent" if score >= 80 else "strong" if score >= 60 else "developing" if score >= 40 else "basic"
    suggestions = tuple(f"Add {criterion.replace('_', ' ')}." for criterion, value in points.items() if value == 0)
    strengths = tuple(criterion.replace("_", " ") for criterion, value in points.items() if value == 2)
    return PromptReport(score, label, strengths, suggestions)


def compare(prompts: Sequence[str]) -> list[PromptReport]:
    return [evaluate(prompt) for prompt in prompts]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate the quality of a generative-AI prompt.")
    parser.add_argument("prompt")
    args = parser.parse_args()
    report = evaluate(args.prompt)
    print(f"Prompt quality: {report.score}/100 ({report.label})")
    print("Strengths: " + (", ".join(report.strengths) if report.strengths else "None yet"))
    print("Suggestions: " + (" ".join(report.suggestions) if report.suggestions else "None — ready to test"))
