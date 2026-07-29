import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Bloque_C-Boole-Shannon-ComputaciónCuántica"))

from ejercicio_10 import *

def test_X_sobre_ket0_da_ket1():
    estado = aplicar_compuerta(KET_0, X)
    assert np.allclose(estado, KET_1)

def test_H_sobre_ket0_da_probabilidades_50_50():
    estado = aplicar_compuerta(KET_0, H)
    p0, p1 = probabilidades(estado)
    assert abs(p0 - 0.5) < 1e-9
    assert abs(p1 - 0.5) < 1e-9

def test_HH_sobre_ket0_regresa_a_ket0():
    estado = aplicar_compuerta(KET_0, H)
    estado = aplicar_compuerta(estado, H)
    assert np.allclose(estado, KET_0, atol=1e-9)

def test_Z_sobre_ket1_invierte_signo_pero_no_probabilidad():
    estado = aplicar_compuerta(KET_1, Z)
    assert np.allclose(estado, np.array([0, -1]))
    p0, p1 = probabilidades(estado)
    assert abs(p1 - 1.0) < 1e-9  # la probabilidad de medir 1 sigue siendo 1

def test_simulacion_1000_mediciones_converge_a_probabilidad_teorica():
    estado = aplicar_compuerta(KET_0, H)  # 50/50
    sim = simular_mediciones(estado, 1000)
    assert sim["conteo_0"] + sim["conteo_1"] == 1000
    assert abs(sim["frecuencia_0"] - 0.5) < 0.1  # tolerancia estadística

def test_estado_no_normalizado_no_es_valido_para_born_correcta():
    # Verifica que |0> y |1> puros dan probabilidad exacta 1 y 0
    p0, p1 = probabilidades(KET_0)
    assert p0 == 1.0 and p1 == 0.0

def test_num_mediciones_invalido_lanza_error():
    try:
        simular_mediciones(KET_0, 0)
        assert False, "Debía lanzar ValueError"
    except ValueError:
        pass

test_X_sobre_ket0_da_ket1()
test_H_sobre_ket0_da_probabilidades_50_50()
test_HH_sobre_ket0_regresa_a_ket0()
test_Z_sobre_ket1_invierte_signo_pero_no_probabilidad()
test_simulacion_1000_mediciones_converge_a_probabilidad_teorica()
test_estado_no_normalizado_no_es_valido_para_born_correcta()
test_num_mediciones_invalido_lanza_error()
print("Todas las pruebas del Ejercicio 10 pasaron correctamente.")
