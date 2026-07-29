import math
import heapq
from collections import Counter


def calcular_frecuencias(texto: str) -> dict:
    """Cuenta cuántas veces aparece cada símbolo (carácter) en el texto."""
    if texto == "":
        raise ValueError("El texto no puede estar vacío.")
    return dict(Counter(texto))


def calcular_probabilidades(frecuencias: dict) -> dict:
    """Convierte frecuencias absolutas en probabilidades (frecuencia
    relativa de cada símbolo sobre el total de caracteres).
    """
    total = sum(frecuencias.values())
    return {simbolo: freq / total for simbolo, freq in frecuencias.items()}


def entropia_shannon(probabilidades: dict) -> float:
    """Calcula H = - sum_i p_i * log2(p_i), en bits por símbolo."""
    return -sum(p * math.log2(p) for p in probabilidades.values() if p > 0)


def analizar_texto(texto: str) -> dict:
    """Junta frecuencias, probabilidades y entropía de un texto."""
    frecuencias = calcular_frecuencias(texto)
    probabilidades = calcular_probabilidades(frecuencias)
    H = entropia_shannon(probabilidades)
    return {
        "texto": texto,
        "frecuencias": frecuencias,
        "probabilidades": probabilidades,
        "entropia": H,
        "simbolos_distintos": len(frecuencias),
        "longitud": len(texto),
    }


def comparar_textos(texto1: str, texto2: str) -> str:
    """Compara la entropía de dos textos y explica cuál es mayor y por qué."""
    a1 = analizar_texto(texto1)
    a2 = analizar_texto(texto2)

    if a1["entropia"] > a2["entropia"]:
        mayor, menor = a1, a2
    elif a2["entropia"] > a1["entropia"]:
        mayor, menor = a2, a1
    else:
        return (f"Ambos textos tienen la misma entropía "
                f"({a1['entropia']:.4f} bits/símbolo).")

    return (
        f"El texto '{mayor['texto']}' tiene MAYOR entropía "
        f"({mayor['entropia']:.4f} bits/símbolo) que '{menor['texto']}' "
        f"({menor['entropia']:.4f} bits/símbolo), porque sus símbolos están "
        f"repartidos de forma más pareja (menos predecible símbolo a "
        f"símbolo), mientras que el otro texto está dominado por pocos "
        f"símbolos muy frecuentes (más predecible, menor incertidumbre)."
    )


def imprimir_analisis(texto: str):
    """Imprime frecuencia, probabilidad y entropía de un texto de forma legible."""
    a = analizar_texto(texto)
    print(f"Texto: '{texto}' (longitud={a['longitud']}, símbolos distintos={a['simbolos_distintos']})")
    print(f"{'Símbolo':<12}{'Frecuencia':>12}{'Probabilidad':>15}")
    for simbolo in sorted(a["frecuencias"], key=lambda s: -a["frecuencias"][s]):
        rep = repr(simbolo)  # para que espacios y saltos de línea se vean
        print(f"{rep:<12}{a['frecuencias'][simbolo]:>12}{a['probabilidades'][simbolo]:>15.4f}")
    print(f"Entropía H = {a['entropia']:.4f} bits/símbolo\n")
    return a


# --- Extensión opcional: código de Huffman ---

class _NodoHuffman:
    def __init__(self, prob, simbolo=None, izq=None, der=None):
        self.prob = prob
        self.simbolo = simbolo
        self.izq = izq
        self.der = der

    def __lt__(self, otro):  # para poder usar heapq
        return self.prob < otro.prob


def construir_arbol_huffman(probabilidades: dict) -> _NodoHuffman:
    """Construye el árbol de Huffman combinando repetidamente los dos
    nodos de menor probabilidad.
    """
    monticulo = [_NodoHuffman(p, simbolo=s) for s, p in probabilidades.items()]
    heapq.heapify(monticulo)

    if len(monticulo) == 1:  # un solo símbolo: código trivial "0"
        return monticulo[0]

    while len(monticulo) > 1:
        a = heapq.heappop(monticulo)
        b = heapq.heappop(monticulo)
        combinado = _NodoHuffman(a.prob + b.prob, izq=a, der=b)
        heapq.heappush(monticulo, combinado)

    return monticulo[0]


def generar_codigos_huffman(nodo: _NodoHuffman, prefijo: str = "", codigos: dict = None) -> dict:
    """Recorre el árbol y asigna a cada símbolo su código binario."""
    if codigos is None:
        codigos = {}
    if nodo.simbolo is not None:
        codigos[nodo.simbolo] = prefijo if prefijo else "0"
        return codigos
    generar_codigos_huffman(nodo.izq, prefijo + "0", codigos)
    generar_codigos_huffman(nodo.der, prefijo + "1", codigos)
    return codigos


def longitud_promedio_huffman(probabilidades: dict, codigos: dict) -> float:
    """Longitud promedio (bits/símbolo) del código de Huffman resultante."""
    return sum(probabilidades[s] * len(c) for s, c in codigos.items())


if __name__ == "__main__":
    # --- Dos mensajes obligatorios: uno repetitivo, uno variado ---
    texto_repetitivo = "AAAAAAAAAABBBAAAAA"
    texto_variado = "el veloz murcielago hindu comia feliz cardillo y kiwi"

    print("=== Texto repetitivo ===")
    a1 = imprimir_analisis(texto_repetitivo)

    print("=== Texto variado ===")
    a2 = imprimir_analisis(texto_variado)

    print(comparar_textos(texto_repetitivo, texto_variado))
    assert a2["entropia"] > a1["entropia"]

    # --- Extensión opcional: Huffman sobre el texto variado ---
    print("\n=== Extensión: código de Huffman (texto variado) ===")
    arbol = construir_arbol_huffman(a2["probabilidades"])
    codigos = generar_codigos_huffman(arbol)
    long_prom = longitud_promedio_huffman(a2["probabilidades"], codigos)
    print(f"Códigos asignados (símbolo: código): {codigos}")
    print(f"Longitud promedio de Huffman: {long_prom:.4f} bits/símbolo")
    print(f"Entropía de Shannon:          {a2['entropia']:.4f} bits/símbolo")
    print(f"¿Huffman >= entropía? {long_prom >= a2['entropia']}")
    assert long_prom >= a2["entropia"] - 1e-9  # tolerancia numérica

    # --- Modo interactivo ---
    print("\n--- Modo interactivo ---")
    texto_u1 = input("Primer texto: ")
    texto_u2 = input("Segundo texto: ")
    try:
        imprimir_analisis(texto_u1)
        imprimir_analisis(texto_u2)
        print(comparar_textos(texto_u1, texto_u2))
    except ValueError as err:
        print("Error:", err)
