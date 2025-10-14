from __future__ import annotations
from collections import defaultdict
import time

from .models import Grammar, Node
from .models import is_nonterminal


class CYKParser:
    def __init__(self, grammar: Grammar):
        self.G = grammar
        # Índices de acceso rápido
        self.term_index = defaultdict(set)   # a -> {A | A→a}
        self.bin_index = defaultdict(set)    # (B,C) -> {A | A→B C}
        for p in self.G.productions:
            if len(p.right) == 1 and not is_nonterminal(p.right[0]):
                self.term_index[p.right[0]].add(p.left)
            elif len(p.right) == 2 and all(is_nonterminal(x) for x in p.right):
                self.bin_index[(p.right[0], p.right[1])].add(p.left)

    def parse(self, tokens: list[str]):
        n = len(tokens)
        if n == 0:
            return False, [], None, 0.0
        table: list[list[dict[str, list[Node]]]] = [[defaultdict(list) for _ in range(n)] for _ in range(n)]
        t0 = time.perf_counter()
        # Base: longitud 1
        for i, a in enumerate(tokens):
            for A in self.term_index.get(a, set()):
                node = Node(A, i, i, token=a)
                table[i][i][A].append(node)
        # Longitud >=2
        for span in range(2, n + 1):
            for i in range(0, n - span + 1):
                j = i + span - 1
                for k in range(i, j):
                    left_cells = table[i][k]
                    right_cells = table[k + 1][j]
                    if not left_cells or not right_cells:
                        continue
                    for B, nodesB in left_cells.items():
                        for C, nodesC in right_cells.items():
                            for A in self.bin_index.get((B, C), set()):
                                for nb in nodesB:
                                    for nc in nodesC:
                                        table[i][j][A].append(Node(A, i, j, left=nb, right=nc))
        elapsed = (time.perf_counter() - t0) * 1000.0
        root_nodes = table[0][n - 1].get(self.G.start, [])
        accepted = len(root_nodes) > 0
        root = root_nodes[0] if accepted else None
        return accepted, table, root, elapsed
