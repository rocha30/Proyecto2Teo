from __future__ import annotations

from .models import Production, Grammar


def build_project_grammar() -> Grammar:
    # Versión cercana a FNC; se convertirá formalmente con to_cnf().
    P: list[Production] = []
    def add(A: str, rhs: list[str]):
        P.append(Production(A, tuple(rhs)))

    # Regla principal
    add('S', ['NP', 'VP'])
    # VP
    add('VP', ['VP', 'PP'])
    add('VP', ['V', 'NP'])
    add('VP', ['cooks'])
    add('VP', ['drinks'])
    add('VP', ['eats'])
    add('VP', ['cuts'])
    # PP
    add('PP', ['P', 'NP'])
    # NP
    add('NP', ['Det', 'N'])
    add('NP', ['he'])
    add('NP', ['she'])
    # V
    add('V', ['cooks'])
    add('V', ['drinks'])
    add('V', ['eats'])
    add('V', ['cuts'])
    # P
    add('P', ['in'])
    add('P', ['with'])
    # N
    for w in ['cat', 'dog', 'beer', 'cake', 'juice', 'meat', 'soup', 'fork', 'knife', 'oven', 'spoon']:
        add('N', [w])
    # Det
    add('Det', ['a'])
    add('Det', ['the'])

    g = Grammar('S', P)
    return g.to_cnf()
