import random

NUM_SERVIDORES = 3


def generar_partes(x: int, M: int, num_partes: int = NUM_SERVIDORES) -> list:
    """Divide el entero x en 'num_partes' partes aleatorias módulo M,
    tales que la suma de las partes (mod M) es igual a x.
    """
    partes = [random.randrange(M) for _ in range(num_partes - 1)]
    ultima = (x - sum(partes)) % M
    partes.append(ultima)
    return partes


def distribuir_notas(notas: list, M: int, num_partes: int = NUM_SERVIDORES) -> list:
    """Reparte cada nota en partes y arma la vista de cada servidor.
    Devuelve una lista de listas: servidores[i] = lista de las partes
    que le tocaron al servidor i (una por cada nota, en el mismo orden).
    Ningún servidor recibe la lista de notas original.
    """
    for nota in notas:
        if not (0 <= nota <= 50):
            raise ValueError(f"Nota inválida: {nota} (debe estar entre 0 y 50).")

    servidores = [[] for _ in range(num_partes)]
    for nota in notas:
        partes = generar_partes(nota, M, num_partes)
        for i in range(num_partes):
            servidores[i].append(partes[i])
    return servidores


def suma_parcial_servidor(partes_servidor: list, M: int) -> int:
    """Cada servidor, de forma local, suma solo las partes que le tocaron."""
    return sum(partes_servidor) % M


def reconstruir_suma(sumas_parciales: list, M: int) -> int:
    """Combina las sumas parciales de los 3 servidores para obtener
    la suma total real de las notas, sin que nadie haya visto una
    nota completa.
    """
    return sum(sumas_parciales) % M


def simular_mpc_promedio(notas: list, M: int = 1000003) -> dict:
    """Corre la simulación completa y devuelve suma, promedio y las
    vistas de cada servidor (solo para fines demostrativos: en un
    escenario real esas vistas no se mostrarían juntas).
    """
    if len(notas) == 0:
        raise ValueError("La lista de notas no puede estar vacía.")

    servidores = distribuir_notas(notas, M)
    sumas_parciales = [suma_parcial_servidor(s, M) for s in servidores]
    suma_total = reconstruir_suma(sumas_parciales, M)
    promedio = suma_total / len(notas)

    return {
        "suma": suma_total,
        "promedio": promedio,
        "servidores": servidores,       # partes que ve cada servidor
        "sumas_parciales": sumas_parciales,
    }


if __name__ == "__main__":
    # --- Ejemplo del enunciado ---
    notas = [40, 35, 50, 25]
    resultado = simular_mpc_promedio(notas)
    print("Ejemplo del enunciado:")
    print(f"  Suma reconstruida: {resultado['suma']}")
    print(f"  Promedio: {resultado['promedio']}")
    print(f"  Vista del servidor 1 (partes, no notas): {resultado['servidores'][0]}")
    assert resultado["suma"] == 150
    assert resultado["promedio"] == 37.5

    # --- Ejemplo distinto, con más notas (no es caso fijo) ---
    notas2 = [10, 20, 30, 40, 50, 0, 15]
    resultado2 = simular_mpc_promedio(notas2)
    print("\nSegundo ejemplo:")
    print(f"  Notas reales: {notas2} (esto solo se imprime para verificar, "
          f"ningún servidor lo conoce)")
    print(f"  Suma reconstruida: {resultado2['suma']}")
    print(f"  Promedio: {resultado2['promedio']:.4f}")

    # --- Modo interactivo ---
    print("\n--- Modo interactivo ---")
    entrada = input("Notas separadas por coma (ej: 40,35,50,25): ")
    notas_usuario = [int(n.strip()) for n in entrada.split(",")]
    try:
        r = simular_mpc_promedio(notas_usuario)
        print(f"Suma: {r['suma']}  Promedio: {r['promedio']}")
    except ValueError as err:
        print("Error:", err)
