from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict


def is_nonterminal(X: str) -> bool:
    return X and X[0].isupper()


@dataclass(frozen=True)
class Production:
    left: str                 # No terminal
    right: tuple[str, ...]    # Secuencia de símbolos (NT o t)


class Grammar:
    def __init__(self, start: str, productions: list[Production]):
        self.start = start
        self.productions = productions[:]
        self._rebuild_sets()

    def _rebuild_sets(self):
        self.N = set(p.left for p in self.productions)
        self.T = set(s for p in self.productions for s in p.right if not is_nonterminal(s))
        self.by_left: dict[str, list[tuple[str, ...]]] = defaultdict(list)
        for p in self.productions:
            self.by_left[p.left].append(p.right)

    def add_prod(self, A: str, rhs: tuple[str, ...]):
        self.productions.append(Production(A, rhs))

    def dedup(self):
        seen = set()
        uniq = []
        for p in self.productions:
            key = (p.left, p.right)
            if key not in seen:
                seen.add(key)
                uniq.append(p)
        self.productions = uniq
        self._rebuild_sets()

    # ---------------------- Simplificación → FNC ------------------------- #
    def to_cnf(self) -> 'Grammar':
        g = Grammar(self.start, self.productions)
        g = g._remove_useless()
        g = g._remove_epsilon()
        g = g._remove_unit()
        g = g._terminals_in_binaries()
        g = g._binarize()
        # Asegurar nuevo símbolo inicial si S aparece en RHS
        rhs_symbols = {sym for p in g.productions for sym in p.right}
        if g.start in rhs_symbols:
            S0 = g._fresh_nt('S0')
            g.add_prod(S0, (g.start,))
            g.start = S0
            g.dedup()
        return g

    def _fresh_nt(self, base: str) -> str:
        i = 1
        cand = base
        used = {p.left for p in self.productions} | {s for p in self.productions for s in p.right if is_nonterminal(s)}
        while cand in used:
            cand = f"{base}{i}"
            i += 1
        return cand

    def _remove_useless(self) -> 'Grammar':
        # 1) No generativos → eliminarlos
        generating = set()
        changed = True
        while changed:
            changed = False
            for p in self.productions:
                if p.left in generating:
                    continue
                if all((not is_nonterminal(s)) or (s in generating) for s in p.right):
                    generating.add(p.left)
                    changed = True
        prods1 = [p for p in self.productions if p.left in generating and all((not is_nonterminal(s)) or (s in generating) for s in p.right)]
        # 2) Inalcanzables desde S → eliminarlos
        reachable = set([self.start])
        changed = True
        while changed:
            changed = False
            for p in prods1:
                if p.left in reachable:
                    for s in p.right:
                        if is_nonterminal(s) and s not in reachable:
                            reachable.add(s)
                            changed = True
        prods2 = [p for p in prods1 if p.left in reachable]
        g = Grammar(self.start, prods2)
        g.dedup()
        return g

    def _remove_epsilon(self) -> 'Grammar':
        # Encontrar anulables (A ⇒* ε)
        nullable = set()
        changed = True
        while changed:
            changed = False
            for p in self.productions:
                if p.left in nullable:
                    continue
                if len(p.right) == 0 or all(is_nonterminal(s) and s in nullable for s in p.right):
                    nullable.add(p.left)
                    changed = True
        new_prods = set()
        for p in self.productions:
            if len(p.right) == 0:
                # omitimos ε, lo reconstruiremos salvo quizá S→ε si corresponde
                continue
            # Para cada subconjunto de símbolos anulables en RHS, crear variante sin ellos
            positions = [i for i, s in enumerate(p.right) if is_nonterminal(s) and s in nullable]
            m = len(positions)
            for mask in range(1 << m):
                rhs = list(p.right)
                for j in range(m):
                    if (mask >> j) & 1:
                        rhs[positions[j]] = None
                rhs2 = tuple(s for s in rhs if s is not None)
                if len(rhs2) == 0:
                    if p.left == self.start:
                        new_prods.add((p.left, tuple()))
                else:
                    new_prods.add((p.left, rhs2))
        g = Grammar(self.start, [Production(A, rhs) for (A, rhs) in new_prods])
        g.dedup()
        return g

    def _remove_unit(self) -> 'Grammar':
        # Clausura de unitarias A→B
        unit = defaultdict(set)  # A -> {B}
        for A in self.N:
            unit[A].add(A)
        changed = True
        while changed:
            changed = False
            for p in self.productions:
                if len(p.right) == 1 and is_nonterminal(p.right[0]):
                    A, B = p.left, p.right[0]
                    for C in unit[B]:
                        if C not in unit[A]:
                            unit[A].add(C)
                            changed = True
        prods = set()
        for A in self.N:
            for B in unit[A]:
                for rhs in self.by_left.get(B, []):
                    if not (len(rhs) == 1 and is_nonterminal(rhs[0])):
                        prods.add((A, rhs))
        g = Grammar(self.start, [Production(A, rhs) for (A, rhs) in prods])
        g.dedup()
        return g

    def _terminals_in_binaries(self) -> 'Grammar':
        # En reglas de longitud >=2, reemplazar terminales por preterminales únicos
        mapping: dict[str, str] = {}  # terminal -> NT
        new_prods: list[Production] = []
        for p in self.productions:
            rhs = list(p.right)
            if len(rhs) >= 2:
                for i, s in enumerate(rhs):
                    if not is_nonterminal(s):
                        if s not in mapping:
                            nt = self._fresh_nt(f"T_{s}")
                            mapping[s] = nt
                        rhs[i] = mapping[s]
                new_prods.append(Production(p.left, tuple(rhs)))
            else:
                new_prods.append(p)
        # añadir preterminales
        for t, nt in mapping.items():
            new_prods.append(Production(nt, (t,)))
        g = Grammar(self.start, new_prods)
        g.dedup()
        return g

    def _binarize(self) -> 'Grammar':
        # Convierte A → X1 X2 ... Xk (k>=3) en secuencia binaria.
        new_prods: list[Production] = []
        for p in self.productions:
            rhs = list(p.right)
            if len(rhs) <= 2:
                new_prods.append(p)
            else:
                A = p.left
                # Estrategia izquierda-ramificada:
                # A -> X1 Y1; Y1 -> X2 Y2; ...; Y_{k-3} -> X_{k-2} Y_{k-2}; Y_{k-2} -> X_{k-1} X_k
                X1 = rhs[0]
                X2 = rhs[1]
                Y_prev = self._fresh_nt(f"BIN_{A}")
                new_prods.append(Production(A, (X1, Y_prev)))
                k = 2
                while k < len(rhs) - 1:
                    Xk = rhs[k]
                    Y_next = self._fresh_nt(f"BIN_{A}")
                    new_prods.append(Production(Y_prev, (X2, Y_next)))
                    X2 = Xk
                    Y_prev = Y_next
                    k += 1
                # último par
                new_prods.append(Production(Y_prev, (X2, rhs[-1])))
        g = Grammar(self.start, new_prods)
        g.dedup()
        return g


@dataclass
class Node:
    sym: str
    i: int
    j: int
    left: 'Node | None' = None
    right: 'Node | None' = None
    token: str | None = None
