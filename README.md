# Taller3-discretas

# Taller de Matemáticas Discretas — Seguridad, Redes, Lógica y Computación Cuántica

## Descripción

Este repositorio contiene la implementación de 10 ejercicios prácticos que muestran
cómo se aplican las matemáticas discretas en criptografía/seguridad, teoría de grafos,
álgebra booleana / circuitos lógicos, y conceptos básicos de información y computación
cuántica.

Cada ejercicio incluye: el código fuente, una forma de ejecutarlo, al menos tres
pruebas con entradas y salidas, y una explicación breve de la idea matemática detrás
de la solución (ver carpeta `docs/`).

## Integrante

- Erik Santiago Martinez Perez

## Lenguaje usado

Python 3.x (probado en Google Colab)

## Estructura del repositorio
taller-discretas/

├── README.md

├── requirements.txt

├── .gitignore

├── src/                                              # Código fuente de los 10 ejercicios, por bloque

│   ├── Bloque_A-Criptografía/                        # Bloque A - Criptografía (ejercicios 1-3)

│   ├── Bloque_B-Grafos/                              # Bloque B - Grafos (ejercicios 4-6)

│   └── Bloque_C-Boole-Shannon-ComputaciónCuántica/   # Bloque C - Boole, Shannon y Computación Cuántica (ejercicios 7-10)

├── tests/                  Pruebas por ejercicio

└── docs/                     Explicación matemática (Markdown → PDF)

## Instrucciones para ejecutar

Cada ejercicio se puede correr de forma independiente:

```bash
python src/<bloque>/ejercicio_XX.py    # bloque = bloque_a, bloque_b o bloque_c
```

Las pruebas de cada ejercicio están en `tests/` y se corren igual:

```bash
python tests/test_ejercicio_XX.py
```

Los ejercicios se desarrollaron y probaron en Google Colab; el código no depende
de ningún archivo local fuera del repositorio.

## Lista de ejercicios desarrollados

| # | Tema | Archivo fuente | Pruebas | Estado |
|---|------|----------------|---------|--------|
| 1 | Criptografía (César) | src/bloque_a/ejercicio_01.py | tests/test_ejercicio_01.py | hecho |
| 2 | Criptografía (RSA de juguete) | src/bloque_a/ejercicio_02.py | tests/test_ejercicio_02.py | hecho |
| 3 | Criptografía (MPC - promedio secreto) | src/bloque_a/ejercicio_03.py | tests/test_ejercicio_03.py | hecho |
| 4 | Grafos (Dijkstra - ruta más corta) | src/bloque_b/ejercicio_04.py | tests/test_ejercicio_04.py, tests/grafo_ejemplo.json | hecho |
| 5 | Grafos (impacto del cierre de una estación) | src/bloque_b/ejercicio_05.py | tests/test_ejercicio_05.py | hecho |
| 6 | Grafos (coloreo voraz - horarios de examen) | src/bloque_b/ejercicio_06.py | tests/test_ejercicio_06.py | hecho |
| 7 | Boole (tablas de verdad y circuitos) | src/bloque_c/ejercicio_07.py | tests/test_ejercicio_07.py | hecho |
| 8 | Boole (simplificación - Quine-McCluskey) | src/bloque_c/ejercicio_08.py | tests/test_ejercicio_08.py | hecho |
| 9 | Shannon (entropía + Huffman opcional) | src/bloque_c/ejercicio_09.py | tests/test_ejercicio_09.py | hecho |
| 10 | Cuántica (simulador de 1 qubit) | src/bloque_c/ejercicio_10.py | tests/test_ejercicio_10.py | hecho |

## Librerías externas

Solo se usa NUMPY, exactamente para el ejercicio 10 CUANTICA
