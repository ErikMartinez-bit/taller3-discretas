"""
Ejercicio 1 — Cifrado César
Bloque: Criptografía

Idea matemática:
El cifrado César es una transformación afín sobre el alfabeto, visto como
el anillo Z_26 (enteros módulo 26). Cada letra se identifica con un número
de 0 a 25 (A=0, B=1, ..., Z=25) y se aplica:

    cifrado(letra)    = (letra + k) mod 26
    descifrado(letra) = (letra - k) mod 26 = (letra + (26 - k)) mod 26

Como la suma módulo 26 es invertible, el cifrado siempre se puede deshacer
conociendo k: basta desplazar en sentido contrario. Eso es lo que lo hace
"reversible" y, a la vez, inseguro: al haber solo 26 desplazamientos
posibles, un atacante puede probarlos todos (fuerza bruta) casi al instante.
"""

ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
N = len(ALFABETO)  # 26


def _desplazar_letra(letra: str, k: int) -> str:
    """Desplaza una sola letra k posiciones (mod 26).
    Conserva mayúsculas/minúsculas. Si no es A-Z (espacio, número,
    puntuación), la devuelve sin cambios.
    """
    if letra.isalpha() and letra.upper() in ALFABETO:
        es_mayuscula = letra.isupper()
        indice = ALFABETO.index(letra.upper())
        nueva_letra = ALFABETO[(indice + k) % N]
        return nueva_letra if es_mayuscula else nueva_letra.lower()
    return letra


def cifrar(texto: str, k: int) -> str:
    """Cifra 'texto' desplazando cada letra k posiciones hacia adelante."""
    k = k % N
    return "".join(_desplazar_letra(c, k) for c in texto)


def descifrar(texto: str, k: int) -> str:
    """Descifra 'texto' que fue cifrado con desplazamiento k."""
    k = k % N
    return "".join(_desplazar_letra(c, -k) for c in texto)


def fuerza_bruta(texto_cifrado: str) -> dict:
    """Prueba los 26 desplazamientos posibles y devuelve
    {k: texto_descifrado_con_ese_k}. Viable porque el espacio de
    llaves es diminuto (26 intentos).
    """
    return {k: descifrar(texto_cifrado, k) for k in range(N)}


if __name__ == "__main__":
    # --- Ejemplo del enunciado ---
    texto = "HOLA UNAL"
    k = 3
    cifrado = cifrar(texto, k)
    print(f"Texto original:  {texto}")
    print(f"Cifrado (k={k}):  {cifrado}")
    print(f"Descifrado:      {descifrar(cifrado, k)}")

    # --- Entrada distinta, para mostrar que no es un caso fijo ---
    texto2 = "Reunion Secreta a las 22:00, Sala #5!"
    k2 = 11
    cifrado2 = cifrar(texto2, k2)
    print(f"\nTexto original:  {texto2}")
    print(f"Cifrado (k={k2}): {cifrado2}")
    print(f"Descifrado:      {descifrar(cifrado2, k2)}")

    # --- Ataque de fuerza bruta (k desconocido) ---
    print(f"\nFuerza bruta sobre '{cifrado2}':")
    for intento_k, resultado in fuerza_bruta(cifrado2).items():
        print(f"  k={intento_k:2d} -> {resultado}")

    # --- Modo interactivo: entradas nuevas dadas por el usuario ---
    print("\n--- Modo interactivo ---")
    opcion = input("¿Qué quieres hacer? (1) Cifrar  (2) Descifrar  (3) Fuerza bruta: ")

    if opcion == "1":
        texto_usuario = input("Texto a cifrar: ")
        k_usuario = int(input("Desplazamiento k: "))
        print("Resultado:", cifrar(texto_usuario, k_usuario))
    elif opcion == "2":
        texto_usuario = input("Texto a descifrar: ")
        k_usuario = int(input("Desplazamiento k: "))
        print("Resultado:", descifrar(texto_usuario, k_usuario))
    elif opcion == "3":
        texto_usuario = input("Texto cifrado (k desconocido): ")
        for intento_k, resultado in fuerza_bruta(texto_usuario).items():
            print(f"  k={intento_k:2d} -> {resultado}")
    else:
        print("Opción no válida, se omite el modo interactivo.")
