import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Bloque_B-Grafos"))

from ejercicio_06 import

def test_coloreo_valido_grafo_cursos():
    colores = colorear_grafo_voraz(GRAFO_CURSOS)
    assert verificar_coloreo(GRAFO_CURSOS, colores)

def test_cantidad_de_colores_grafo_cursos():
    colores = colorear_grafo_voraz(GRAFO_CURSOS)
    assert len(agrupar_por_color(colores)) == 3

def test_grafo_completo_necesita_n_colores():
    # En K4 cada vertice es vecino de todos los demas: se necesitan 4 colores.
    aristas_k4 = [("w", "x"), ("w", "y"), ("w", "z"),
                  ("x", "y"), ("x", "z"), ("y", "z")]
    grafo_k4 = construir_grafo_no_dirigido(aristas_k4)
    colores = colorear_grafo_voraz(grafo_k4)
    assert verificar_coloreo(grafo_k4, colores)
    assert len(agrupar_por_color(colores)) == 4

def test_orden_afecta_cantidad_de_colores():
    aristas = [("a1", "b2"), ("a1", "b3"), ("a2", "b1"),
               ("a2", "b3"), ("a3", "b1"), ("a3", "b2")]
    grafo = construir_grafo_no_dirigido(aristas)

    orden_malo = ["a1", "b1", "a2", "b2", "a3", "b3"]
    colores_malo = colorear_grafo_voraz(grafo, orden=orden_malo)
    colores_bueno = colorear_grafo_voraz(grafo)

    assert verificar_coloreo(grafo, colores_malo)
    assert verificar_coloreo(grafo, colores_bueno)
    assert len(agrupar_por_color(colores_malo)) == 3   # subóptimo
    assert len(agrupar_por_color(colores_bueno)) == 2  # óptimo (bipartito)

def test_grafo_sin_aristas_usa_un_solo_color():
    grafo = construir_grafo_no_dirigido([], vertices=["A", "B", "C"])
    colores = colorear_grafo_voraz(grafo)
    assert len(agrupar_por_color(colores)) == 1

def test_verificar_coloreo_detecta_conflicto():
    grafo = construir_grafo_no_dirigido([("A", "B")])
    colores_invalidos = {"A": 0, "B": 0}  # a propósito, mismo color
    assert verificar_coloreo(grafo, colores_invalidos) is False

test_coloreo_valido_grafo_cursos()
test_cantidad_de_colores_grafo_cursos()
test_grafo_completo_necesita_n_colores()
test_orden_afecta_cantidad_de_colores()
test_grafo_sin_aristas_usa_un_solo_color()
test_verificar_coloreo_detecta_conflicto()
print("Todas las pruebas del Ejercicio 6 pasaron correctamente.")
