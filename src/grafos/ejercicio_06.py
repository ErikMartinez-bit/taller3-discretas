def construir_grafo_no_dirigido(aristas, vertices=None):
    """Construye un diccionario de adyacencia no dirigido a partir de una
    lista de aristas (tuplas (u,v)). Si se pasa 'vertices', asegura que
    todos aparezcan en el grafo aunque no tengan aristas.
    """
    grafo = {}
    if vertices:
        for v in vertices:
            grafo.setdefault(v, set())
    for u, v in aristas:
        grafo.setdefault(u, set()).add(v)
        grafo.setdefault(v, set()).add(u)
    return grafo


def orden_por_grado_descendente(grafo):
    """Heurística de Welsh-Powell: procesa primero los vértices con más
    conflictos (mayor grado), alfabético para desempatar. No garantiza
    el óptimo, pero suele acercarse más que un orden arbitrario.
    """
    return sorted(grafo.keys(), key=lambda v: (-len(grafo[v]), v))


def colorear_grafo_voraz(grafo, orden=None):
    """Asigna colores (enteros 0,1,2,...) a los vértices de 'grafo' con
    un algoritmo voraz: recorre 'orden' (o por grado descendente si no
    se especifica) y a cada vértice le da el color más pequeño que
    ninguno de sus vecinos ya coloreados esté usando.
    """
    if orden is None:
        orden = orden_por_grado_descendente(grafo)

    colores = {}
    for vertice in orden:
        colores_vecinos = {colores[v] for v in grafo[vertice] if v in colores}
        color = 0
        while color in colores_vecinos:
            color += 1
        colores[vertice] = color
    return colores


def verificar_coloreo(grafo, colores) -> bool:
    """Verifica que ningún par de vértices adyacentes comparta color."""
    for u in grafo:
        for v in grafo[u]:
            if colores[u] == colores[v]:
                return False
    return True


def agrupar_por_color(colores: dict) -> dict:
    """Agrupa los vértices por color: {color: [vertices]}."""
    grupos = {}
    for vertice, color in colores.items():
        grupos.setdefault(color, []).append(vertice)
    for color in grupos:
        grupos[color].sort()
    return grupos


# --- Grafo de prueba: 10 cursos, aristas = estudiantes en comun ---
CURSOS = ["Calculo", "Fisica", "Programacion", "BasesDatos", "Estadistica",
          "Redes", "IA", "Discretas", "Algebra", "Quimica"]

CONFLICTOS = [
    ("Calculo", "Fisica"), ("Calculo", "Algebra"), ("Fisica", "Quimica"),
    ("Programacion", "BasesDatos"), ("Programacion", "IA"),
    ("BasesDatos", "Redes"), ("Estadistica", "IA"), ("Estadistica", "Discretas"),
    ("Redes", "IA"), ("Discretas", "Algebra"), ("Algebra", "Quimica"),
    ("IA", "Discretas"),
]

GRAFO_CURSOS = construir_grafo_no_dirigido(CONFLICTOS, CURSOS)


if __name__ == "__main__":
    colores = colorear_grafo_voraz(GRAFO_CURSOS)
    grupos = agrupar_por_color(colores)

    print("Coloreo de examenes (voraz, orden por grado descendente):")
    print(f"  Colores usados: {len(grupos)}")
    for color, vertices in sorted(grupos.items()):
        print(f"  Franja horaria {color}: {vertices}")
    print(f"  ¿Coloreo valido? {verificar_coloreo(GRAFO_CURSOS, colores)}")

    assert verificar_coloreo(GRAFO_CURSOS, colores)
    assert len(grupos) == 3

    # --- Segundo ejemplo: mismo tipo de problema, grafo distinto, para
    #     mostrar que el ORDEN afecta cuantos colores se necesitan
    #     (aunque el resultado siempre sea valido) ---
    ARISTAS_CRUZADO = [
        ("a1", "b2"), ("a1", "b3"),
        ("a2", "b1"), ("a2", "b3"),
        ("a3", "b1"), ("a3", "b2"),
    ]
    GRAFO_CRUZADO = construir_grafo_no_dirigido(ARISTAS_CRUZADO)

    orden_malo = ["a1", "b1", "a2", "b2", "a3", "b3"]
    colores_malo = colorear_grafo_voraz(GRAFO_CRUZADO, orden=orden_malo)
    colores_bueno = colorear_grafo_voraz(GRAFO_CRUZADO)  # por grado

    print("\nMismo grafo (bipartito, optimo=2 colores), dos ordenes distintos:")
    print(f"  Orden arbitrario a1,b1,a2,b2,a3,b3 -> {len(agrupar_por_color(colores_malo))} colores")
    print(f"  Orden por grado descendente        -> {len(agrupar_por_color(colores_bueno))} colores")

    assert verificar_coloreo(GRAFO_CRUZADO, colores_malo)
    assert verificar_coloreo(GRAFO_CRUZADO, colores_bueno)

    # --- Modo interactivo ---
    print("\n--- Modo interactivo ---")
    print(f"Cursos actuales: {CURSOS}")
    entrada = input("Nuevas aristas 'CursoA-CursoB' separadas por ';' (ENTER = usar el grafo de ejemplo): ")
    if entrada.strip():
        nuevas_aristas = []
        for par in entrada.split(";"):
            u, v = par.split("-")
            nuevas_aristas.append((u.strip(), v.strip()))
        grafo_u = construir_grafo_no_dirigido(nuevas_aristas)
    else:
        grafo_u = GRAFO_CURSOS

    colores_u = colorear_grafo_voraz(grafo_u)
    grupos_u = agrupar_por_color(colores_u)
    print(f"Colores usados: {len(grupos_u)}")
    for color, vertices in sorted(grupos_u.items()):
        print(f"  Franja horaria {color}: {vertices}")
    print(f"¿Coloreo valido? {verificar_coloreo(grafo_u, colores_u)}")
