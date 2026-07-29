def euclides_extendido(a: int, b: int):
    """Algoritmo de Euclides extendido.
    Devuelve (g, x, y) tales que a*x + b*y = g = gcd(a, b).
    """
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = euclides_extendido(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return (g, x, y)


def inverso_modular(e: int, modulo: int) -> int:
    """Calcula d tal que (e * d) % modulo == 1, usando Euclides extendido.
    Lanza un error claro si e y modulo no son coprimos (no existe inverso).
    """
    g, x, _ = euclides_extendido(e, modulo)
    if g != 1:
        raise ValueError(
            f"e={e} no es válido: gcd(e, phi(n)) = {g} (debe ser 1, "
            f"es decir, e y phi(n) deben ser coprimos)."
        )
    return x % modulo


def generar_llaves(p: int, q: int, e: int):
    """Genera n, phi(n) y d a partir de p, q, e.
    Devuelve (n, phi_n, d).
    """
    n = p * q
    phi_n = (p - 1) * (q - 1)
    d = inverso_modular(e, phi_n)  # lanza ValueError si e no sirve
    return n, phi_n, d


def cifrar(m: int, e: int, n: int) -> int:
    """Cifra el mensaje m (entero) como C = m^e mod n."""
    if m >= n:
        print(f"Aviso: M={m} >= n={n}; RSA solo garantiza resultados "
              f"correctos si M < n (aquí se reduce M mod n automáticamente).")
    return pow(m, e, n)


def descifrar(c: int, d: int, n: int) -> int:
    """Descifra el criptograma c como M = c^d mod n."""
    return pow(c, d, n)


if __name__ == "__main__":
    # --- Caso de prueba obligatorio del enunciado ---
    p, q, e, M = 61, 53, 17, 65
    n, phi_n, d = generar_llaves(p, q, e)
    C = cifrar(M, e, n)
    M_recuperado = descifrar(C, d, n)
    print("Caso obligatorio:")
    print(f"  n={n}  phi(n)={phi_n}  d={d}  C={C}  M_recuperado={M_recuperado}")
    assert (n, phi_n, d, C, M_recuperado) == (3233, 3120, 2753, 2790, 65)

    # --- Segundo ejemplo, con primos y mensaje distintos (no es caso fijo) ---
    p2, q2, e2, M2 = 17, 11, 7, 88
    n2, phi_n2, d2 = generar_llaves(p2, q2, e2)
    C2 = cifrar(M2, e2, n2)
    M2_recuperado = descifrar(C2, d2, n2)
    print("\nSegundo ejemplo:")
    print(f"  n={n2}  phi(n)={phi_n2}  d={d2}  C={C2}  M_recuperado={M2_recuperado}")

    # --- Modo interactivo ---
    print("\n--- Modo interactivo ---")
    p_u = int(input("Primo p: "))
    q_u = int(input("Primo q: "))
    e_u = int(input("Exponente publico e: "))
    try:
        n_u, phi_u, d_u = generar_llaves(p_u, q_u, e_u)
        print(f"n={n_u}  phi(n)={phi_u}  d={d_u}")
        M_u = int(input("Mensaje M (entero) a cifrar: "))
        C_u = cifrar(M_u, e_u, n_u)
        print(f"Cifrado C={C_u}")
        print(f"Descifrado de vuelta: {descifrar(C_u, d_u, n_u)}")
    except ValueError as err:
        print("Error:", err)
