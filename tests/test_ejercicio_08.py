import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Bloque_C-Boole-Shannon-ComputaciónCuántica"))

from ejercicio_08 import *

def test_caso_obligatorio_minterminos_1_3_5_7():
    expr, patrones, _ = simplificar([1, 3, 5, 7], 3)
    assert expr == "C"
    assert verificar_equivalencia([1, 3, 5, 7], patrones, 3)

def test_cuatro_variables_A_igual_cero():
    expr, patrones, _ = simplificar(list(range(8)), 4)
    assert expr == "NOT A"
    assert verificar_equivalencia(list(range(8)), patrones, 4)

def test_funcion_siempre_falsa():
    expr, patrones, _ = simplificar([], 3)
    assert expr == "0"
    assert verificar_equivalencia([], patrones, 3)

def test_funcion_siempre_verdadera():
    expr, patrones, _ = simplificar(list(range(8)), 3)
    assert expr == "1"
    assert verificar_equivalencia(list(range(8)), patrones, 3)

def test_expresion_simplificada_tiene_menos_o_igual_literales():
    # La suma directa de mintérminos usaría 3 literales por término;
    # la simplificada para {1,3,5,7} usa solo 1 literal (C).
    expr, _, _ = simplificar([1, 3, 5, 7], 3)
    assert " AND " not in expr  # un solo literal, sin necesidad de AND

def test_mintermino_fuera_de_rango_lanza_error():
    try:
        simplificar([8], 3)  # máximo válido para n=3 es 7
        assert False, "Debía lanzar ValueError"
    except ValueError:
        pass

def test_numero_de_variables_invalido_lanza_error():
    try:
        simplificar([1, 2], 5)
        assert False, "Debía lanzar ValueError"
    except ValueError:
        pass

test_caso_obligatorio_minterminos_1_3_5_7()
test_cuatro_variables_A_igual_cero()
test_funcion_siempre_falsa()
test_funcion_siempre_verdadera()
test_expresion_simplificada_tiene_menos_o_igual_literales()
test_mintermino_fuera_de_rango_lanza_error()
test_numero_de_variables_invalido_lanza_error()
print("Todas las pruebas del Ejercicio 8 pasaron correctamente.")
