def se_pueden_combinar(t1: str, t2: str):
    """Indica si dos patrones (strings de '0','1','-') difieren en
    exactamente una posición no-dash, con los '-' en las mismas posiciones
    en ambos. Devuelve el índice donde difieren, o None si no se pueden
    combinar.
    """
    if len(t1) != len(t2):
        return None
    indice_diferente = None
    for i, (c1, c2) in enumerate(zip(t1, t2)):
        if c1 == "-" or c2 == "-":
            if c1 != c2:
                return None  # los '-' deben estar en la misma posición
            continue
        if c1 != c2:
            if indice_diferente is not None:
                return None  # más de una diferencia: no se pueden combinar
            indice_diferente = i
    return indice_diferente


def generar_implicantes_primos(minterminos: list, n: int) -> set:
    """Aplica Quine-McCluskey: combina términos repetidamente hasta que
    no se pueda más. Devuelve el conjunto de implicantes primos, cada uno
    como (patron_str, frozenset_de_minterminos_que_cubre).
    """
    terminos = {(format(m, f"0{n}b"), frozenset({m})) for m in minterminos}
    primos = set()

    while True:
        combinados = set()
        nuevos = set()
        lista = list(terminos)
        for i in range(len(lista)):
            for j in range(i + 1, len(lista)):
                t1, m1 = lista[i]
                t2, m2 = lista[j]
                idx = se_pueden_combinar(t1, t2)
                if idx is not None:
                    nuevo_patron = t1[:idx] + "-" + t1[idx + 1:]
                    nuevos.add((nuevo_patron, frozenset(m1 | m2)))
                    combinados.add((t1, m1))
                    combinados.add((t2, m2))
        primos |= (terminos - combinados)  # los no combinados son primos
        if not nuevos:
            break
        terminos = nuevos

    return primos


def seleccionar_cobertura(minterminos: list, primos: set) -> set:
    """Elige implicantes primos esenciales (los que cubren algún mintérmino
    en solitario) y cubre el resto con una heurística voraz (el implicante
    que cubra más mintérminos pendientes en cada paso).
    """
    cobertura = {m: [] for m in minterminos}
    for patron, cubiertos in primos:
        for m in cubiertos:
            if m in cobertura:
                cobertura[m].append((patron, cubiertos))

    esenciales = {imps[0] for imps in cobertura.values() if len(imps) == 1}
    ya_cubiertos = set()
    for _, cubiertos in esenciales:
        ya_cubiertos |= cubiertos

    seleccionados = set(esenciales)
    restantes = set(minterminos) - ya_cubiertos
    while restantes:
        mejor = max(primos, key=lambda pm: len(pm[1] & restantes))
        if not (mejor[1] & restantes):
            break
        seleccionados.add(mejor)
        restantes -= mejor[1]

    return seleccionados


def patron_a_termino(patron: str, variables: list) -> str:
    """Convierte un patrón ('1','0','-') en un término legible, ej.
    '--1' con variables [A,B,C] -> 'C'; '101' -> '(A AND NOT B AND C)'.
    """
    literales = []
    for var, bit in zip(variables, patron):
        if bit == "1":
            literales.append(var)
        elif bit == "0":
            literales.append(f"NOT {var}")
    if not literales:
        return "1"  # todas las variables son "-": función siempre verdadera
    if len(literales) == 1:
        return literales[0]
    return "(" + " AND ".join(literales) + ")"


def simplificar(minterminos: list, num_variables: int):
    """Punto de entrada principal. Recibe los mintérminos y el número de
    variables (3 o 4) y devuelve (expresion_simplificada, patrones, variables).
    """
    if num_variables not in (3, 4):
        raise ValueError("num_variables debe ser 3 o 4.")

    variables = ["A", "B", "C", "D"][:num_variables]
    valor_maximo = 2 ** num_variables - 1
    minterminos = sorted(set(minterminos))

    for m in minterminos:
        if not (0 <= m <= valor_maximo):
            raise ValueError(
                f"Mintérmino inválido: {m} (debe estar entre 0 y {valor_maximo} "
                f"para {num_variables} variables)."
            )

    if not minterminos:
        return "0", [], variables  # función siempre falsa
    if len(minterminos) == valor_maximo + 1:
        return "1", ["-" * num_variables], variables  # función siempre verdadera

    primos = generar_implicantes_primos(minterminos, num_variables)
    seleccionados = seleccionar_cobertura(minterminos, primos)
    patrones = sorted(p for p, _ in seleccionados)
    expresion = " OR ".join(patron_a_termino(p, variables) for p in patrones)
    return expresion, patrones, variables


# --- Funciones de verificación (comparan tabla de verdad original vs simplificada) ---

def mintermino_a_termino(m: int, n: int, variables: list) -> str:
    """Término producto completo (todas las variables) de un mintérmino."""
    return patron_a_termino(format(m, f"0{n}b"), variables)


def expresion_original_desde_minterminos(minterminos: list, n: int, variables: list) -> str:
    """La expresión SIN simplificar: suma de todos los mintérminos."""
    if not minterminos:
        return "0"
    return " OR ".join(mintermino_a_termino(m, n, variables) for m in sorted(minterminos))


def _cubre(bits: str, patron: str) -> bool:
    return all(c2 == "-" or c1 == c2 for c1, c2 in zip(bits, patron))


def verificar_equivalencia(minterminos: list, patrones: list, n: int) -> bool:
    """Compara, para las 2^n combinaciones posibles, si pertenecer a
    'minterminos' coincide con estar cubierto por algún patrón simplificado.
    Es la comprobación de que ambas expresiones tienen la misma tabla de verdad.
    """
    minterminos_set = set(minterminos)
    for m in range(2 ** n):
        bits = format(m, f"0{n}b")
        esperado = m in minterminos_set
        obtenido = any(_cubre(bits, p) for p in patrones) if patrones else False
        if esperado != obtenido:
            return False
    return True


if __name__ == "__main__":
    # --- Caso obligatorio del enunciado ---
    minterminos1, n1 = [1, 3, 5, 7], 3
    expr1, patrones1, vars1 = simplificar(minterminos1, n1)
    orig1 = expresion_original_desde_minterminos(minterminos1, n1, vars1)
    print("Caso obligatorio: mintérminos {1,3,5,7}, 3 variables")
    print(f"  Expresión original:      {orig1}")
    print(f"  Expresión simplificada:  {expr1}")
    print(f"  ¿Misma tabla de verdad?  {verificar_equivalencia(minterminos1, patrones1, n1)}")
    assert expr1 == "C"
    assert verificar_equivalencia(minterminos1, patrones1, n1)

    # --- Segundo ejemplo: 4 variables, mintérminos distintos (no caso fijo) ---
    minterminos2, n2 = list(range(8)), 4  # A=0 en las 4 variables
    expr2, patrones2, vars2 = simplificar(minterminos2, n2)
    print("\nSegundo ejemplo: mintérminos 0-7, 4 variables")
    print(f"  Expresión simplificada:  {expr2}")
    print(f"  ¿Misma tabla de verdad?  {verificar_equivalencia(minterminos2, patrones2, n2)}")
    assert expr2 == "NOT A"
    assert verificar_equivalencia(minterminos2, patrones2, n2)

    # --- Modo interactivo ---
    print("\n--- Modo interactivo ---")
    n_u = int(input("Número de variables (3 o 4): "))
    entrada = input("Mintérminos separados por coma (ej: 1,3,5,7): ")
    minterminos_u = [int(x.strip()) for x in entrada.split(",") if x.strip() != ""]
    try:
        expr_u, patrones_u, vars_u = simplificar(minterminos_u, n_u)
        orig_u = expresion_original_desde_minterminos(minterminos_u, n_u, vars_u)
        print(f"Expresión original:      {orig_u}")
        print(f"Expresión simplificada:  {expr_u}")
        print(f"¿Misma tabla de verdad?  {verificar_equivalencia(minterminos_u, patrones_u, n_u)}")
    except ValueError as err:
        print("Error:", err)
