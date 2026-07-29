import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Bloque_B-Grafos"))

from ejercicio_04 import *

def test_ruta_principal_portal_estadio():
    d, r = dijkstra(GRAFO_CIUDAD, "Portal", "Estadio")
    assert d == 17
    assert r == ["Portal", "Calle26", "Museo", "Centro", "Universidad", "Parque", "Estadio"]

def test_ruta_directa_mas_corta_que_alternativas():
    # Portal -> Terminal: la arista directa (8) es mejor que cualquier rodeo
    d, r = dijkstra(GRAFO_CIUDAD, "Portal", "Terminal")
    assert d == 8
    assert r == ["Portal", "Terminal"]

def test_origen_igual_a_destino():
    d, r = dijkstra(GRAFO_CIUDAD, "Centro", "Centro")
    assert d == 0
    assert r == ["Centro"]

def test_nodo_inexistente_lanza_error():
    try:
        dijkstra(GRAFO_CIUDAD, "Portal", "Aeropuerto")
        assert False, "Debia lanzar ValueError por nodo inexistente"
    except ValueError:
        pass

def test_nodo_inalcanzable_devuelve_none():
    grafo_desconectado = {"X": {"Y": 1}, "Y": {"X": 1}, "Z": {}}
    d, r = dijkstra(grafo_desconectado, "X", "Z")
    assert d is None
    assert r == []

def test_peso_negativo_lanza_error_al_cargar():
    try:
        cargar_grafo_desde_diccionario({"A": {"B": -3}, "B": {"A": -3}})
        assert False, "Debia lanzar ValueError por peso negativo"
    except ValueError:
        pass

test_ruta_principal_portal_estadio()
test_ruta_directa_mas_corta_que_alternativas()
test_origen_igual_a_destino()
test_nodo_inexistente_lanza_error()
test_nodo_inalcanzable_devuelve_none()
test_peso_negativo_lanza_error_al_cargar()
print("Todas las pruebas del Ejercicio 4 pasaron correctamente.")
