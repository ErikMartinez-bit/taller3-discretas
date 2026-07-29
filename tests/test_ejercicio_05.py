import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Bloque_B-Grafos"))

from ejercicio_05 import

def test_impacto_ruta_mas_larga():
    gd = eliminar_vertice(GRAFO_CIUDAD, "Centro")
    f = comparar_impacto(GRAFO_CIUDAD, gd, [("Portal", "Estadio")])[0]
    assert f["distancia_antes"] == 17
    assert f["distancia_despues"] == 19
    assert f["diferencia"] == 2
    assert f["estado"] == "ruta más larga"

def test_impacto_sin_cambio():
    gd = eliminar_vertice(GRAFO_CIUDAD, "Centro")
    f = comparar_impacto(GRAFO_CIUDAD, gd, [("Museo", "Terminal")])[0]
    assert f["diferencia"] == 0
    assert f["estado"] == "sin cambio"

def test_impacto_desconectado_nodo_aislado():
    gd = eliminar_vertice(GRAFO_CIUDAD, "Centro")
    f = comparar_impacto(GRAFO_CIUDAD, gd, [("Portal", "Biblioteca")])[0]
    assert f["distancia_despues"] is None
    assert f["estado"] == "quedó desconectado"

def test_impacto_nodo_cerrado_es_el_destino():
    gd = eliminar_vertice(GRAFO_CIUDAD, "Centro")
    f = comparar_impacto(GRAFO_CIUDAD, gd, [("Portal", "Centro")])[0]
    assert f["estado"] == "estación cerrada (nodo eliminado de la red)"

def test_cierre_de_arista_no_afecta_el_resto_del_grafo():
    gd = eliminar_arista(GRAFO_CIUDAD, "Universidad", "Parque")
    assert "Parque" not in gd["Universidad"]
    assert "Universidad" not in gd["Parque"]
    assert gd["Portal"]["Calle26"] == 4  # el resto del grafo sigue intacto

def test_eliminar_vertice_inexistente_lanza_error():
    try:
        eliminar_vertice(GRAFO_CIUDAD, "Aeropuerto")
        assert False, "Debia lanzar ValueError"
    except ValueError:
        pass

test_impacto_ruta_mas_larga()
test_impacto_sin_cambio()
test_impacto_desconectado_nodo_aislado()
test_impacto_nodo_cerrado_es_el_destino()
test_cierre_de_arista_no_afecta_el_resto_del_grafo()
test_eliminar_vertice_inexistente_lanza_error()
print("Todas las pruebas del Ejercicio 5 pasaron correctamente.")
