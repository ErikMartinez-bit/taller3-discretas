import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Bloque_C-Boole-Shannon-ComputaciónCuántica"))

from ejercicio_07 import *

def test_expresion_1_A_and_B_or_not_C():
    variables, filas = generar_tabla_verdad("(A AND B) OR (NOT C)")
    assert variables == ["A", "B", "C"]
    assert len(filas) == 8
    fila = next(f for f in filas if f["A"] and f["B"] and not f["C"])
    assert fila["Resultado"] is True
    fila2 = next(f for f in filas if not f["A"] and not f["B"] and f["C"])
    assert fila2["Resultado"] is False

def test_expresion_2_A_xor_B_and_C():
    variables, filas = generar_tabla_verdad("(A XOR B) AND C")
    fila = next(f for f in filas if f["A"] and not f["B"] and f["C"])
    assert fila["Resultado"] is True
    fila2 = next(f for f in filas if f["A"] and f["B"] and f["C"])
    assert fila2["Resultado"] is False

def test_expresion_3_A_or_B_and_not_A_or_C():
    variables, filas = generar_tabla_verdad("(A OR B) AND (NOT A OR C)")
    fila = next(f for f in filas if f["A"] and not f["B"] and not f["C"])
    assert fila["Resultado"] is False

def test_evaluar_expresion_entrada_concreta():
    assert evaluar_expresion("(A AND B) OR (NOT C)", {"A": True, "B": False, "C": True}) is False
    assert evaluar_expresion("(A AND B) OR (NOT C)", {"A": True, "B": True, "C": False}) is True

def test_simbolos_equivalen_a_palabras():
    v1, f1 = generar_tabla_verdad("(A ∧ B) ∨ (¬C)")
    v2, f2 = generar_tabla_verdad("(A AND B) OR (NOT C)")
    assert v1 == v2 and f1 == f2

def test_parentesis_desbalanceados_lanza_error():
    try:
        parsear("(A AND B")
        assert False, "Debía lanzar ValueError"
    except ValueError:
        pass

test_expresion_1_A_and_B_or_not_C()
test_expresion_2_A_xor_B_and_C()
test_expresion_3_A_or_B_and_not_A_or_C()
test_evaluar_expresion_entrada_concreta()
test_simbolos_equivalen_a_palabras()
test_parentesis_desbalanceados_lanza_error()
print("Todas las pruebas del Ejercicio 7 pasaron correctamente.")
