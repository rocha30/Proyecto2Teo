#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Proyecto 2 – Teoría de la Computación
Implementación: Simplificación de gramáticas (→ FNC) + Algoritmo CYK + Parse Tree + Medición de tiempo.

Uso rápido (desde terminal):
  python cyk_parser.py --demo                 # corre pruebas de ejemplo
  python cyk_parser.py --sentence "She eats a cake with a fork"  # evalúa una oración
"""
from __future__ import annotations
import argparse
import sys

from cyk import (
    CYKParser,
    build_project_grammar,
    normalize_sentence,
    pretty_tree,
)


def run_sentence(parser: CYKParser, sentence: str):
    toks = normalize_sentence(sentence)
    ok, table, root, ms = parser.parse(toks)
    print(f"Entrada: {sentence}")
    print(f"Tokens:  {toks}")
    print(f"Resultado: {'SÍ' if ok else 'NO'}  |  Tiempo: {ms:.3f} ms")
    if ok and root:
        print("Parse tree:")
        print(pretty_tree(root, toks))


def main():
    g = build_project_grammar()
    parser = CYKParser(g)

    ap = argparse.ArgumentParser()
    ap.add_argument('--sentence', type=str, help='Frase a evaluar (en inglés).')
    ap.add_argument('--demo', action='store_true', help='Corre ejemplos de prueba del enunciado.')
    args = ap.parse_args()

    if args.sentence:
        run_sentence(parser, args.sentence)
        return
    if args.demo:
        tests = [
            "She eats a cake with a fork.",
            "The cat drinks the beer.",
            "She eat a cake with a fork.",
            "She eats cake with a fork.",
            "He cuts the meat in the oven.",
            "The cat the beer drinks.",
            "She drinks the juice.",
        ]
        for s in tests:
            print('-' * 72)
            run_sentence(parser, s)
        return

    # Si no hay args, leer de stdin una línea
    print("Escribe una oración en inglés y presiona Enter (Ctrl+C para salir):")
    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            run_sentence(parser, line)
            print()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
