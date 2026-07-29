import heapq
import json


def cargar_grafo_desde_diccionario(dic: dict) -> dict:
    """Valida y devuelve un grafo ya representado como diccionario de
    adyacencia: {nodo: {vecino: peso, ...}, ...}. Verifica que todos los
    pesos sean no negativos (requisito de Dijkstra).
    """
    for nodo, vecinos in dic.items():
        for vecino, peso in vecinos.items():
            if peso < 0:
                raise ValueError(
                    f"Peso negativo detectado ({nodo}->{vecino}={peso}); "
                    f"Dijkstra requiere pesos no negativos."
                )
    return dic


def cargar_grafo_desde_archivo(ruta_archivo: str) -> dict:
    """Carga un grafo desde un archivo JSON con formato:
    {"NodoA": {"NodoB": peso, ...}, ...}
    """
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        dic = json.load(f)
    return cargar_grafo_desde_diccionario(dic)


def dijkstra(grafo: dict, origen: str, destino: str):
    """Calcula la distancia más corta y la ruta entre origen y destino.
    Devuelve (distancia, ruta) donde ruta es una lista de nodos.
    Si destino es inalcanzable, devuelve (None, []).
    """
    if origen not in grafo:
        raise ValueError(f"El nodo origen '{origen}' no está en el grafo.")
    if destino not in grafo:
        raise ValueError(f"El nodo destino '{destino}' no está en el grafo.")

    distancias = {nodo: float("inf") for nodo in grafo}
    distancias[origen] = 0
    predecesor = {nodo: None for nodo in grafo}
    visitados = set()

    cola = [(0, origen)]  # (distancia_tentativa, nodo)

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
        return None, []  # inalcanzable

    # Reconstruir la ruta siguiendo los predecesores hacia atrás
    ruta = []
    nodo = destino
    while nodo is not None:
        ruta.append(nodo)
        nodo = predecesor[nodo]
    ruta.reverse()

    return distancias[destino], ruta


# --- Grafo de prueba: 8 vértices, 13 aristas (red de transporte ficticia) ---
GRAFO_CIUDAD = {
    "Portal":       {"Calle26": 4, "Terminal": 8},
    "Calle26":      {"Portal": 4, "Museo": 3, "Centro": 7},
    "Museo":        {"Calle26": 3, "Centro": 2, "Universidad": 5},
    "Centro":       {"Calle26": 7, "Museo": 2, "Universidad": 1, "Parque": 6},
    "Universidad":  {"Museo": 5, "Centro": 1, "Parque": 3, "Estadio": 9},
    "Parque":       {"Centro": 6, "Universidad": 3, "Estadio": 4, "Terminal": 10},
    "Terminal":     {"Portal": 8, "Parque": 10, "Estadio": 12},
    "Estadio":      {"Universidad": 9, "Parque": 4, "Terminal": 12},
}


if __name__ == "__main__":
    grafo = cargar_grafo_desde_diccionario(GRAFO_CIUDAD)

    # --- Ejemplo principal ---
    distancia, ruta = dijkstra(grafo, "Portal", "Estadio")
    print("Ruta más corta Portal -> Estadio:")
    print(f"  Distancia total: {distancia}")
    print(f"  Ruta: {' -> '.join(ruta)}")

    # --- Segundo ejemplo, distinto par de nodos ---
    distancia2, ruta2 = dijkstra(grafo, "Terminal", "Museo")
    print("\nRuta más corta Terminal -> Museo:")
    print(f"  Distancia total: {distancia2}")
    print(f"  Ruta: {' -> '.join(ruta2)}")

    # --- Modo interactivo ---
    print("\n--- Modo interactivo ---")
    print(f"Vértices disponibles: {list(grafo.keys())}")
    origen_u = input("Nodo origen: ")
    destino_u = input("Nodo destino: ")
    try:
        d, r = dijkstra(grafo, origen_u, destino_u)
        if d is None:
            print(f"No existe ruta entre {origen_u} y {destino_u}.")
        else:
            print(f"Distancia: {d}  Ruta: {' -> '.join(r)}")
    except ValueError as err:
        print("Error:", err)
