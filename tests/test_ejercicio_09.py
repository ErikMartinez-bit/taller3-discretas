import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Bloque_C-Boole-Shannon-ComputaciónCuántica"))

from ejercicio_09 import *

def test_texto_completamente_uniforme_tiene_entropia_cero():
    a = analizar_texto("AAAAAA")
    assert abs(a["entropia"] - 0.0) < 1e-9

def test_dos_simbolos_equiprobables_entropia_uno():
    # "AB" repetido: P(A)=P(B)=0.5 -> H = 1 bit exacto
    a = analizar_texto("ABABABAB")
    assert abs(a["entropia"] - 1.0) < 1e-9

def test_texto_variado_tiene_mayor_entropia_que_repetitivo():
    rep = "AAAAAAAAAABBBAAAAA"
    var = "el veloz murcielago hindu comia feliz cardillo y kiwi"
    assert analizar_texto(var)["entropia"] > analizar_texto(rep)["entropia"]

def test_probabilidades_suman_uno():
    a = analizar_texto("mississippi")
    assert abs(sum(a["probabilidades"].values()) - 1.0) < 1e-9

def test_texto_vacio_lanza_error():
    try:
        analizar_texto("")
        assert False, "Debía lanzar ValueError"
    except ValueError:
        pass

def test_huffman_longitud_promedio_mayor_o_igual_a_entropia():
    texto = "el veloz murcielago hindu comia feliz cardillo y kiwi"
    a = analizar_texto(texto)
    arbol = construir_arbol_huffman(a["probabilidades"])
    codigos = generar_codigos_huffman(arbol)
    long_prom = longitud_promedio_huffman(a["probabilidades"], codigos)
    assert long_prom >= a["entropia"] - 1e-9

def test_huffman_un_solo_simbolo_codigo_trivial():
    a = analizar_texto("ZZZZZ")
    arbol = construir_arbol_huffman(a["probabilidades"])
    codigos = generar_codigos_huffman(arbol)
    assert codigos == {"Z": "0"}

test_texto_completamente_uniforme_tiene_entropia_cero()
test_dos_simbolos_equiprobables_entropia_uno()
test_texto_variado_tiene_mayor_entropia_que_repetitivo()
test_probabilidades_suman_uno()
test_texto_vacio_lanza_error()
test_huffman_longitud_promedio_mayor_o_igual_a_entropia()
test_huffman_un_solo_simbolo_codigo_trivial()
print("Todas las pruebas del Ejercicio 9 pasaron correctamente.")
