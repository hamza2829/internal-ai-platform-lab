"""Deterministic guardrails for the demonstration app; not a security boundary."""
import re

PERSONAL_DATA = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b|\b(?:\+?\d[\d ()-]{7,}\d)\b")
CONFIDENTIAL = re.compile(r"\b(?:CONFIDENTIAL|SECRET|INTERNAL ONLY)\b", re.IGNORECASE)
RISKY_ACTION = re.compile(r"\b(?:send|publish|delete|refund|transfer|approve|purchase)\b", re.IGNORECASE)
UNSAFE_OUTPUT = re.compile(r"\b(?:guaranteed medical cure|password is)\b|api[_ -]?key\s*[:=]", re.IGNORECASE)


def inspect_input(text: str) -> list[str]:
    flags = []
    if PERSONAL_DATA.search(text):
        flags.append("personal_data")
    if CONFIDENTIAL.search(text):
        flags.append("confidential_marker")
    return flags


def risky_action(text: str) -> bool:
    return bool(RISKY_ACTION.search(text))


def filter_output(text: str) -> tuple[str, list[str]]:
    if UNSAFE_OUTPUT.search(text):
        return "Output withheld by a responsible AI filter. Please review the request and try again.", ["unsafe_output"]
    return text, []
