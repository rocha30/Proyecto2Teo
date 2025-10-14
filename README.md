# Proyecto: Parser CYK para CFG (Cocke–Younger–Kasami)

Implementación del algoritmo CYK para realizar el parsing de una gramática libre de contexto (CFG) y determinar si una frase simple en inglés pertenece al lenguaje generado por dicha gramática. Incluye conversión de gramáticas a Forma Normal de Chomsky (CNF), parser CYK con reconstrucción de árbol, y una CLI de ejemplo.


---

## Objetivos

- Investigar el algoritmo CYK para reconocimiento de cadenas en lenguajes generados por CFG en Forma Normal de Chomsky (CNF).
- Diseñar o adaptar una gramática para un subconjunto de oraciones simples del inglés (p. ej., S → NP VP, etc.).
- Convertir la gramática a CNF (si no lo está) respetando las restricciones del algoritmo.
- Implementar el algoritmo CYK para decidir pertenencia (aceptar/rechazar una oración).
- (Opcional) Reconstruir y mostrar un árbol(s) de derivación a partir de la tabla CYK.
- (Opcional) Proveer trazas/visualizaciones de la tabla CYK para depuración.

## Fundamentos (resumen)

- CYK es un algoritmo de programación dinámica que decide si una cadena w de longitud n pertenece al lenguaje L(G) de una gramática G en CNF.
- Requiere que la gramática esté en CNF: cada producción debe ser de la forma A → BC o A → a; opcionalmente S → ε si el lenguaje incluye la cadena vacía.
- Complejidad: O(n^3 · |P|), donde |P| es el número de producciones de la gramática.
- Idea: construir una tabla triangular T[i][ℓ] (o T[i][j]) con los no terminales que generan el substring w[i..i+ℓ−1], combinando subsoluciones más pequeñas.

## Contrato de la herramienta (tentativo)

- Entrada:
  - Gramática en CNF (archivo o estructura en memoria).
  - Oración (string) o lista de tokens en inglés simple.
- Salida:
  - Booleano: pertenece/no pertenece.
  - (Opcional) Tabla CYK y/o árbol de derivación.
- Errores comunes:
  - Gramática no está en CNF.
  - Tokens no cubiertos por las reglas léxicas (A → a).

## Gramática ejemplo (CNF mínima, ilustrativa)

- S → NP VP
- NP → Det N
- VP → V NP | V
- Det → "a" | "the"
- N → "dog" | "cat"
- V → "sees" | "barks"

Ejemplos de oraciones:
- Acepta: "the dog sees a cat"
- Acepta: "the dog barks"
- Rechaza: "dog the sees"

Nota: la gramática definitiva puede variar; asegúrate de mantener CNF o incluir un paso de conversión a CNF.

## Estructura de proyecto

```
Proyecto2/
  ├── cyk_parser.py            # CLI: corre demo o evalúa una oración
  ├── cyk/                     # Paquete con la implementación
  │   ├── __init__.py          # Re-exporta tipos y funciones comunes
  │   ├── models.py            # Production, Grammar (→ CNF), Node
  │   ├── cyk.py               # CYKParser (núcleo del algoritmo)
  │   ├── utils.py             # normalize_sentence, pretty_tree
  │   └── grammar_en.py        # build_project_grammar() en CNF
  └── README.md
```

Requisitos:
- Python 3.10 o superior.

## Plan de trabajo

1. Investigar a fondo CYK y CNF; definir gramática objetivo para oraciones simples.
2. Implementación en Python y definición de formato(s) de gramática (hecho: gramática embebida y conversión a CNF).
3. Implementar lector/validador externo (pendiente, opcional: JSON/YAML).
4. Implementado CYK con reconstrucción de árbol (hecho).
5. Agregar pruebas automatizadas (pendiente) y ampliar cobertura de casos borde.
6. Documentación de uso y ejemplos (hecho para CLI básica).

## Criterios de aceptación

- Dada una gramática en CNF y una oración tokenizada, la herramienta debe:
  - Indicar si la oración pertenece al lenguaje (True/False).
  - Manejar tokens desconocidos de forma clara (error o rechazo).
  - Pasar al menos 5 casos de prueba positivos y 5 negativos.
  - (Opcional) Generar al menos un árbol de derivación válido cuando la oración es aceptada.

## Cómo usar

- Ejecutar el demo con varios ejemplos:

```
python3 cyk_parser.py --demo
```

- Evaluar una oración individual (normaliza a minúsculas y elimina puntuación simple):

```
python3 cyk_parser.py --sentence "She eats a cake with a fork"
```

Salida típica:

```
Entrada: She eats a cake with a fork.
Tokens:  ['she', 'eats', 'a', 'cake', 'with', 'a', 'fork']
Resultado: SÍ  |  Tiempo: 0.03 ms
Parse tree:
(S (NP she) (VP (VP (V eats) (NP (Det a) (N cake))) (PP (P with) (NP (Det a) (N fork)))))
```

## Casos límite probados

- Múltiples PP consecutivos (VP → VP PP):
  - "She eats the cake with a fork in the oven" → Acepta.
  - "She eats the cake with a fork in the oven with a knife" → Acepta.
- PP antes del NP objeto:
  - "She eats with a fork the cake" → Rechaza (según la gramática actual).
- Alternando objeto + varios PPs:
  - "The cat drinks the juice in the oven with a fork" → Acepta.

Nota: para permitir PPs antes del objeto (p. ej., "She eats with a fork the cake"), habría que extender la gramática y volver a convertir a CNF.

## Referencias

- Cocke, J., & Younger, D. H. (1967). Parsing context free languages.
- Kasami, T. (1965). An efficient recognition and syntax analysis algorithm for context-free languages.
- Hopcroft, Motwani, Ullman. Introduction to Automata Theory, Languages, and Computation.
- Jurafsky, D., & Martin, J. H. Speech and Language Processing (secciones de parsing y CNF).
- Wikipedia: Cocke–Younger–Kasami algorithm.
