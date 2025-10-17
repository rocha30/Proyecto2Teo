from __future__ import annotations

from .models import Production, Grammar


def build_project_grammar() -> Grammar:
    # Versión cercana a FNC; se convertirá formalmente con to_cnf().
    P: list[Production] = []
    def add(A: str, rhs: list[str]):
        P.append(Production(A, tuple(rhs)))

    # Regla principal
    add('S', ['NP', 'VP'])
    # VP - Soporte para verbos transitivos e intransitivos
    add('VP', ['VP', 'PP'])      # VP con frase preposicional
    add('VP', ['V', 'NP'])       # Verbo transitivo (con objeto directo)
    add('VP', ['V'])             # Verbo intransitivo (sin objeto directo)
    add('VP', ['cooks'])         # Verbo directo como VP
    add('VP', ['drinks'])
    add('VP', ['eats'])
    add('VP', ['cuts'])
    add('VP', ['sees'])          # Nuevo verbo del enunciado
    add('VP', ['barks'])         # Nuevo verbo del enunciado
    add('VP', ['sleeps'])        # Verbo intransitivo adicional
    add('VP', ['runs'])          # Verbo intransitivo adicional
    # PP
    add('PP', ['P', 'NP'])
    # NP
    add('NP', ['Det', 'N'])
    add('NP', ['he'])
    add('NP', ['she'])
    # V - Verbos que pueden tomar objetos directos o ser intransitivos
    add('V', ['cooks'])
    add('V', ['drinks'])
    add('V', ['eats'])
    add('V', ['cuts'])
    add('V', ['sees'])           # Verbo transitivo del enunciado
    add('V', ['barks'])          # Puede ser intransitivo o transitivo
    add('V', ['sleeps'])         # Generalmente intransitivo
    add('V', ['runs'])           # Puede ser intransitivo o transitivo
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
