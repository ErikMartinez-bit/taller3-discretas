import numpy as np
import random

# --- Compuertas como matrices 2x2 ---
X = np.array([[0, 1],
              [1, 0]], dtype=float)

Z = np.array([[1, 0],
              [0, -1]], dtype=float)

H = (1 / np.sqrt(2)) * np.array([[1, 1],
                                  [1, -1]], dtype=float)

# --- Estados base ---
KET_0 = np.array([1, 0], dtype=float)  # |0>
KET_1 = np.array([0, 1], dtype=float)  # |1>


def aplicar_compuerta(estado: np.ndarray, compuerta: np.ndarray) -> np.ndarray:
    """Aplica una compuerta (matriz 2x2) a un estado (vector de 2 entradas).
    Devuelve el nuevo estado como vector.
    """
    if estado.shape != (2,):
        raise ValueError("El estado debe ser un vector de 2 entradas.")
    return compuerta @ estado


def probabilidades(estado: np.ndarray) -> tuple:
    """Calcula (P(0), P(1)) según la regla de Born: |alpha|^2 y |beta|^2."""
    alpha, beta = estado
    p0 = abs(alpha) ** 2
    p1 = abs(beta) ** 2
    return p0, p1


def medir_una_vez(estado: np.ndarray) -> int:
    """Simula una sola medición: devuelve 0 o 1 según las probabilidades
    del estado (una medición real colapsa el estado; aquí solo se
    devuelve el resultado, ya que cada llamada es independiente).
    """
    p0, p1 = probabilidades(estado)
    return 0 if random.random() < p0 else 1


def simular_mediciones(estado: np.ndarray, num_mediciones: int = 1000) -> dict:
    """Repite la medición num_mediciones veces y cuenta las frecuencias
    observadas de 0 y 1.
    """
    if num_mediciones <= 0:
        raise ValueError("num_mediciones debe ser un entero positivo.")
    resultados = [medir_una_vez(estado) for _ in range(num_mediciones)]
    conteo_0 = resultados.count(0)
    conteo_1 = resultados.count(1)
    return {
        "conteo_0": conteo_0, "conteo_1": conteo_1,
        "frecuencia_0": conteo_0 / num_mediciones,
        "frecuencia_1": conteo_1 / num_mediciones,
    }


def imprimir_estado(nombre: str, estado: np.ndarray):
    """Imprime un estado, sus probabilidades teóricas y 1000 mediciones simuladas."""
    p0, p1 = probabilidades(estado)
    sim = simular_mediciones(estado, 1000)
    print(f"{nombre}: estado={np.round(estado, 4)}")
    print(f"  Probabilidades teóricas -> P(0)={p0:.4f}  P(1)={p1:.4f}")
    print(f"  1000 mediciones simuladas -> frecuencia 0={sim['frecuencia_0']:.4f} "
          f"({sim['conteo_0']} veces)  frecuencia 1={sim['frecuencia_1']:.4f} ({sim['conteo_1']} veces)")
    return p0, p1, sim


if __name__ == "__main__":
    # --- Caso obligatorio 1: X|0> = |1> ---
    estado_X0 = aplicar_compuerta(KET_0, X)
    print("Caso obligatorio 1: X|0>")
    imprimir_estado("X|0>", estado_X0)
    assert np.allclose(estado_X0, KET_1)

    # --- Caso obligatorio 2: H|0> da ~50%/50% ---
    print("\nCaso obligatorio 2: H|0>")
    estado_H0 = aplicar_compuerta(KET_0, H)
    p0, p1, sim = imprimir_estado("H|0>", estado_H0)
    assert abs(p0 - 0.5) < 1e-9 and abs(p1 - 0.5) < 1e-9
    assert abs(sim["frecuencia_0"] - 0.5) < 0.1  # tolerancia estadística razonable

    # --- Caso obligatorio 3: HH|0> = |0> ---
    print("\nCaso obligatorio 3: H(H|0>)")
    estado_HH0 = aplicar_compuerta(estado_H0, H)
    imprimir_estado("HH|0>", estado_HH0)
    assert np.allclose(estado_HH0, KET_0, atol=1e-9)

    # --- Ejemplo adicional: Z sobre |1>, y combinación de compuertas ---
    print("\nEjemplo adicional: Z|1> y H(Z(X|0>))")
    estado_Z1 = aplicar_compuerta(KET_1, Z)
    imprimir_estado("Z|1>", estado_Z1)  # cambia el signo, pero no la probabilidad de medir 1

    estado_combinado = aplicar_compuerta(aplicar_compuerta(aplicar_compuerta(KET_0, X), Z), H)
    imprimir_estado("H(Z(X|0>))", estado_combinado)

    # --- Modo interactivo ---
    print("\n--- Modo interactivo ---")
    print("Compuertas disponibles: X, Z, H (puedes encadenar varias separadas por espacio, ej: 'X H')")
    estado_inicial = input("Estado inicial (0 o 1): ").strip()
    estado_u = KET_0.copy() if estado_inicial == "0" else KET_1.copy()

    secuencia = input("Secuencia de compuertas a aplicar (ej: 'H' o 'X Z H'): ").strip().split()
    compuertas = {"X": X, "Z": Z, "H": H}
    try:
        for nombre_compuerta in secuencia:
            estado_u = aplicar_compuerta(estado_u, compuertas[nombre_compuerta.upper()])
        imprimir_estado(f"Estado final tras {secuencia}", estado_u)
    except KeyError as err:
        print(f"Error: compuerta no reconocida {err}. Usa X, Z o H.")
