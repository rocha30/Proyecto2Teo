# Proyecto: Parser CYK para CFG (Cocke–Younger–Kasami)

Este repositorio contendrá la investigación e implementación del algoritmo CYK (Cocke–Younger–Kasami) para realizar el parsing de una gramática libre de contexto (CFG) y determinar si una frase simple en inglés pertenece al lenguaje generado por dicha gramática.

> Estado: inicial (README de arranque para poder hacer el primer commit/push). La implementación se agregará en siguientes commits.

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

## Estructura de proyecto (sugerida)

```
Proyecto2/
  ├── src/
  │   ├── cyk.py            # Núcleo del algoritmo CYK
  │   ├── grammar.py        # Lectura/validación de gramática (CNF)
  │   └── parser.py         # CLI o puntos de entrada de alto nivel
  ├── data/
  │   └── grammar.cnf|json  # Gramática en CNF (formato a definir)
  ├── tests/
  │   └── test_cyk.py       # Casos de prueba (unit/integration)
  ├── README.md
  ├── requirements.txt      # Dependencias (si aplica)
  └── .gitignore            # Archivos a ignorar por git
```

> La estructura es una guía. Se ajustará según el lenguaje y las herramientas que se elijan.

## Plan de trabajo (propuesto)

1. Investigar a fondo CYK y CNF; definir gramática objetivo para oraciones simples.
2. Elegir lenguaje de implementación (p. ej., Python) y formatos de entrada (p. ej., JSON/YAML/propio).
3. Implementar lector/validador de gramática y verificador de CNF.
4. Implementar CYK (tabla, combinaciones, base y paso inductivo).
5. (Opcional) Reconstrucción de árbol de parseo desde la tabla CYK.
6. Agregar pruebas: casos positivos/negativos y bordes (tokens desconocidos, vacío si aplica).
7. Documentar uso y ejemplos; optimizaciones si hicieran falta.

## Criterios de aceptación

- Dada una gramática en CNF y una oración tokenizada, la herramienta debe:
  - Indicar si la oración pertenece al lenguaje (True/False).
  - Manejar tokens desconocidos de forma clara (error o rechazo).
  - Pasar al menos 5 casos de prueba positivos y 5 negativos.
  - (Opcional) Generar al menos un árbol de derivación válido cuando la oración es aceptada.

## Cómo usar (TBD)

- Pendiente de la implementación. Ejemplo tentativo (si se usa Python):

```
python -m src.parser --grammar data/grammar.json --sentence "the dog sees a cat"
```

- Una vez implementado, este README se actualizará con instrucciones exactas y requisitos.

## Pruebas (TBD)

- Se usarán pruebas unitarias y de integración.
- Casos considerados:
  - Oraciones válidas según la gramática.
  - Oraciones con orden incorrecto.
  - Tokens no cubiertos por la gramática.
  - (Opcional) Cadena vacía si la gramática permite ε.

## Referencias

- Cocke, J., & Younger, D. H. (1967). Parsing context free languages.
- Kasami, T. (1965). An efficient recognition and syntax analysis algorithm for context-free languages.
- Hopcroft, Motwani, Ullman. Introduction to Automata Theory, Languages, and Computation.
- Jurafsky, D., & Martin, J. H. Speech and Language Processing (secciones de parsing y CNF).
- Wikipedia: Cocke–Younger–Kasami algorithm.

## Licencia

Por definir.

## Estado y próximos pasos

- [x] Crear README inicial para permitir el primer push.
- [ ] Elegir lenguaje y formato de gramática.
- [ ] Implementar lector/validador de gramática (CNF).
- [ ] Implementar algoritmo CYK.
- [ ] Agregar pruebas y ejemplos.

---

¿Quieres que también deje una gramática base en `data/` y un esqueleto de `src/` para continuar más rápido? Puedo agregarlo en este repo cuando lo indiques.