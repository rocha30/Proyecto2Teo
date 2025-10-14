from __future__ import annotations

from .models import Node


def normalize_sentence(s: str) -> list[str]:
    # Reemplaza puntuación por espacios y normaliza a minúsculas
    punct = ",.;:!?\"'()[]{}"
    s = s.strip().lower()
    for ch in punct:
        s = s.replace(ch, ' ')
    toks = [t for t in s.split() if t]
    return toks


def pretty_tree(node: Node | None, words: list[str]) -> str:
    if node is None:
        return ""
    if node.token is not None:
        return f"({node.sym} {node.token})"
    left = pretty_tree(node.left, words) if node.left else ""
    right = pretty_tree(node.right, words) if node.right else ""
    if right:
        return f"({node.sym} {left} {right})"
    else:
        return f"({node.sym} {left})"
