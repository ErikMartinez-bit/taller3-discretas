import heapq
import copy


def dijkstra(grafo, origen, destino):
    """Distancia y ruta más corta entre origen y destino (pesos no negativos).
    Devuelve (distancia, ruta); (None, []) si destino es inalcanzable.
    """
    if origen not in grafo:
        raise ValueError(f"El nodo origen '{origen}' no está en el grafo.")
    if destino not in grafo:
        raise ValueError(f"El nodo destino '{destino}' no está en el grafo.")

    distancias = {nodo: float("inf") for nodo in grafo}
    distancias[origen] = 0
    predecesor = {nodo: None for nodo in grafo}
    visitados = set()
    cola = [(0, origen)]

    while cola:
        dist_actual, actual = heapq.heappop(cola)
        if actual in visitados:
            continue
        visitados.add(actual)
        if actual == destino:
            break
        for vecino, peso in grafo.get(actual, {}).items():
            nueva_dist = dist_actual + peso
            if nueva_dist < distancias[vecino]:
                distancias[vecino] = nueva_dist
                predecesor[vecino] = actual
                heapq.heappush(cola, (nueva_dist, vecino))

    if distancias[destino] == float("inf"):
        return None, []

    ruta, nodo = [], destino
    while nodo is not None:
        ruta.append(nodo)
        nodo = predecesor[nodo]
    ruta.reverse()
    return distancias[destino], ruta


def eliminar_vertice(grafo: dict, vertice: str) -> dict:
    """Devuelve una copia del grafo sin 'vertice' y sin ninguna arista que
    apunte hacia él (simula el cierre de una estación).
    """
    if vertice not in grafo:
        raise ValueError(f"El vértice '{vertice}' no existe en el grafo.")
    nuevo = copy.deepcopy(grafo)
    del nuevo[vertice]
    for nodo in nuevo:
        nuevo[nodo].pop(vertice, None)
    return nuevo


def eliminar_arista(grafo: dict, u: str, v: str, bidireccional: bool = True) -> dict:
    """Devuelve una copia del grafo sin la arista u-v (simula el cierre de
    una conexión puntual, sin cerrar toda la estación).
    """
    if u not in grafo or v not in grafo.get(u, {}):
        raise ValueError(f"La arista {u}-{v} no existe en el grafo.")
    nuevo = copy.deepcopy(grafo)
    nuevo[u].pop(v, None)
    if bidireccional:
        nuevo[v].pop(u, None)
    return nuevo


def comparar_impacto(grafo_antes: dict, grafo_despues: dict, pares: list) -> list:
    """Calcula, para cada par (origen,destino), la distancia antes y
    después del cierre, la diferencia y un estado descriptivo.
    """
    filas = []
    for origen, destino in pares:
        d_antes, _ = dijkstra(grafo_antes, origen, destino)

        nodo_eliminado = origen not in grafo_despues or destino not in grafo_despues
        d_despues = None if nodo_eliminado else dijkstra(grafo_despues, origen, destino)[0]

        if nodo_eliminado:
            estado = "estación cerrada (nodo eliminado de la red)"
        elif d_antes is None:
            estado = "ya estaba desconectado antes del cierre"
        elif d_despues is None:
            estado = "quedó desconectado"
        elif d_despues > d_antes:
            estado = "ruta más larga"
        else:
            estado = "sin cambio"

        diferencia = (d_despues - d_antes) if (d_antes is not None and d_despues is not None) else None

        filas.append({
            "origen": origen, "destino": destino,
            "distancia_antes": d_antes, "distancia_despues": d_despues,
            "diferencia": diferencia, "estado": estado,
        })
    return filas


def imprimir_tabla(filas: list) -> None:
    """Imprime la tabla origen/destino/antes/después/diferencia/estado."""
    encabezado = f"{'Origen':<12}{'Destino':<12}{'Antes':>8}{'Después':>10}{'Diferencia':>12}  Estado"
    print(encabezado)
    print("-" * len(encabezado))
    for f in filas:
        antes = f["distancia_antes"] if f["distancia_antes"] is not None else "-"
        despues = f["distancia_despues"] if f["distancia_despues"] is not None else "-"
        diferencia = f["diferencia"] if f["diferencia"] is not None else "-"
        print(f"{f['origen']:<12}{f['destino']:<12}{str(antes):>8}{str(despues):>10}{str(diferencia):>12}  {f['estado']}")


# --- Grafo: el mismo del ejercicio 4, más "Biblioteca", un nodo que solo
#     se conecta por Centro (para poder mostrar una desconexión real) ---
GRAFO_CIUDAD = {
    "Portal":       {"Calle26": 4, "Terminal": 8},
    "Calle26":      {"Portal": 4, "Museo": 3, "Centro": 7},
    "Museo":        {"Calle26": 3, "Centro": 2, "Universidad": 5},
    "Centro":       {"Calle26": 7, "Museo": 2, "Universidad": 1, "Parque": 6, "Biblioteca": 2},
    "Universidad":  {"Museo": 5, "Centro": 1, "Parque": 3, "Estadio": 9},
    "Parque":       {"Centro": 6, "Universidad": 3, "Estadio": 4, "Terminal": 10},
    "Terminal":     {"Portal": 8, "Parque": 10, "Estadio": 12},
    "Estadio":      {"Universidad": 9, "Parque": 4, "Terminal": 12},
    "Biblioteca":   {"Centro": 2},
}

PARES_PRUEBA = [
    ("Portal", "Estadio"),
    ("Portal", "Museo"),
    ("Calle26", "Parque"),
    ("Museo", "Terminal"),
    ("Portal", "Biblioteca"),
]


if __name__ == "__main__":
    vertice_cerrado = "Centro"
    grafo_despues = eliminar_vertice(GRAFO_CIUDAD, vertice_cerrado)

    print(f"Cierre simulado: se elimina el vértice '{vertice_cerrado}'.\n")
    filas = comparar_impacto(GRAFO_CIUDAD, grafo_despues, PARES_PRUEBA)
    imprimir_tabla(filas)

    assert filas[0]["diferencia"] == 2 and filas[0]["estado"] == "ruta más larga"       # Portal-Estadio
    assert filas[1]["diferencia"] == 0 and filas[1]["estado"] == "sin cambio"           # Portal-Museo
    assert filas[2]["diferencia"] == 2 and filas[2]["estado"] == "ruta más larga"       # Calle26-Parque
    assert filas[3]["diferencia"] == 0 and filas[3]["estado"] == "sin cambio"           # Museo-Terminal
    assert filas[4]["estado"] == "quedó desconectado"                                   # Portal-Biblioteca

    # --- Segundo ejemplo: cerrar una arista puntual en vez de la estación completa ---
    print("\nCierre simulado: se elimina solo la arista Universidad-Parque.\n")
    grafo_despues_arista = eliminar_arista(GRAFO_CIUDAD, "Universidad", "Parque")
    imprimir_tabla(comparar_impacto(GRAFO_CIUDAD, grafo_despues_arista, PARES_PRUEBA))

    # --- Modo interactivo ---
    print("\n--- Modo interactivo ---")
    print(f"Vértices actuales: {list(GRAFO_CIUDAD.keys())}")
    tipo = input("¿Qué quieres cerrar? (1) Un vértice  (2) Una arista: ")
    try:
        if tipo == "1":
            v = input("Vértice a cerrar: ")
            grafo_cerrado = eliminar_vertice(GRAFO_CIUDAD, v)
        elif tipo == "2":
            u = input("Nodo u de la arista: ")
            v = input("Nodo v de la arista: ")
            grafo_cerrado = eliminar_arista(GRAFO_CIUDAD, u, v)
        else:
            grafo_cerrado = None
            print("Opción no válida.")

        if grafo_cerrado is not None:
            entrada = input("Pares 'origen,destino' separados por ';' (ENTER = usar los 5 de ejemplo): ")
            if entrada.strip():
                pares_u = [tuple(p.split(",")) for p in entrada.split(";")]
                pares_u = [(o.strip(), d.strip()) for o, d in pares_u]
            else:
                pares_u = PARES_PRUEBA
            imprimir_tabla(comparar_impacto(GRAFO_CIUDAD, grafo_cerrado, pares_u))
    except ValueError as err:
        print("Error:", err)
