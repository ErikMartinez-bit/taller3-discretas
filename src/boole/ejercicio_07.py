import re

# --- Tokenizador: acepta palabras (AND/OR/NOT/XOR) y simbolos (∧ ∨ ¬ ⊕) ---
PATRON_TOKEN = re.compile(r'AND|OR|NOT|XOR|[A-Da-d]|[∧∨¬⊕&|!^()]', re.IGNORECASE)
SIMBOLOS = {"∧": "AND", "∨": "OR", "¬": "NOT", "⊕": "XOR",
            "&": "AND", "|": "OR", "!": "NOT", "^": "XOR"}


def tokenizar(expr_str: str) -> list:
    """Convierte el string de la expresión en una lista de tokens
    normalizados: 'AND','OR','NOT','XOR','(',')','A','B','C','D'.
    Caracteres no reconocidos (comas, letras E-Z, etc.) se ignoran.
    """
    crudos = PATRON_TOKEN.findall(expr_str)
    tokens = []
    for t in crudos:
        tu = t.upper()
        if tu in ("AND", "OR", "NOT", "XOR"):
            tokens.append(tu)
        elif t in SIMBOLOS:
            tokens.append(SIMBOLOS[t])
        elif t in "()":
            tokens.append(t)
        elif tu in "ABCD":
            tokens.append(tu)
    return tokens


# --- Parser de descenso recursivo: OR < XOR < AND < NOT (precedencia) ---
def _parse_expr(tokens, pos):
    return _parse_or(tokens, pos)

def _parse_or(tokens, pos):
    nodo, pos = _parse_and(tokens, pos)
    while pos < len(tokens) and tokens[pos] == "OR":
        derecho, pos = _parse_and(tokens, pos + 1)
        nodo = ("OR", nodo, derecho)
    return nodo, pos

def _parse_and(tokens, pos):
    nodo, pos = _parse_xor(tokens, pos)
    while pos < len(tokens) and tokens[pos] == "AND":
        derecho, pos = _parse_xor(tokens, pos + 1)
        nodo = ("AND", nodo, derecho)
    return nodo, pos

def _parse_xor(tokens, pos):
    nodo, pos = _parse_not(tokens, pos)
    while pos < len(tokens) and tokens[pos] == "XOR":
        derecho, pos = _parse_not(tokens, pos + 1)
        nodo = ("XOR", nodo, derecho)
    return nodo, pos

def _parse_not(tokens, pos):
    if pos < len(tokens) and tokens[pos] == "NOT":
        operando, pos = _parse_not(tokens, pos + 1)
        return ("NOT", operando), pos
    return _parse_atom(tokens, pos)

def _parse_atom(tokens, pos):
    if pos >= len(tokens):
        raise ValueError("Expresión booleana incompleta.")
    tok = tokens[pos]
    if tok == "(":
        nodo, pos = _parse_expr(tokens, pos + 1)
        if pos >= len(tokens) or tokens[pos] != ")":
            raise ValueError("Falta un paréntesis de cierre ')'.")
        return nodo, pos + 1
    if tok in "ABCD":
        return ("VAR", tok), pos + 1
    raise ValueError(f"Token inesperado: '{tok}'.")


def parsear(expr_str: str):
    """Tokeniza y construye el árbol de sintaxis de una expresión."""
    tokens = tokenizar(expr_str)
    if not tokens:
        raise ValueError("La expresión está vacía o no tiene tokens válidos.")
    nodo, pos = _parse_expr(tokens, 0)
    if pos != len(tokens):
        raise ValueError(f"Sobran símbolos después de la posición {pos}: {tokens[pos:]}")
    return nodo


def _evaluar_nodo(nodo, valores: dict) -> bool:
    tipo = nodo[0]
    if tipo == "VAR":
        return valores[nodo[1]]
    if tipo == "NOT":
        return not _evaluar_nodo(nodo[1], valores)
    izq = _evaluar_nodo(nodo[1], valores)
    der = _evaluar_nodo(nodo[2], valores)
    if tipo == "AND":
        return izq and der
    if tipo == "OR":
        return izq or der
    if tipo == "XOR":
        return izq != der
    raise ValueError(f"Nodo desconocido: {tipo}")


def _variables_usadas(nodo) -> set:
    if nodo[0] == "VAR":
        return {nodo[1]}
    if nodo[0] == "NOT":
        return _variables_usadas(nodo[1])
    return _variables_usadas(nodo[1]) | _variables_usadas(nodo[2])


def evaluar_expresion(expr_str: str, valores: dict) -> bool:
    """Evalúa la expresión en una entrada concreta, ej:
    evaluar_expresion("(A AND B) OR (NOT C)", {"A": True, "B": False, "C": True})
    """
    nodo = parsear(expr_str)
    return _evaluar_nodo(nodo, valores)


def generar_tabla_verdad(expr_str: str):
    """Genera todas las 2^n combinaciones de las variables usadas en la
    expresión y evalúa el resultado en cada una. Devuelve (variables, filas).
    """
    nodo = parsear(expr_str)
    variables = sorted(_variables_usadas(nodo))
    n = len(variables)
    filas = []
    for i in range(2 ** n):
        valores = {var: bool((i >> (n - 1 - j)) & 1) for j, var in enumerate(variables)}
        filas.append({**valores, "Resultado": _evaluar_nodo(nodo, valores)})
    return variables, filas


def imprimir_tabla(expr_str: str):
    """Imprime la tabla de verdad completa de una expresión."""
    variables, filas = generar_tabla_verdad(expr_str)
    print(f"Expresión: {expr_str}")
    encabezado = " ".join(variables) + " | Resultado"
    print(encabezado)
    print("-" * len(encabezado))
    for fila in filas:
        valores_str = " ".join("V" if fila[v] else "F" for v in variables)
        print(f"{valores_str} | {'V' if fila['Resultado'] else 'F'}")
    return variables, filas


if __name__ == "__main__":
    # --- Las 3 expresiones obligatorias del enunciado ---
    expresiones = [
        "(A AND B) OR (NOT C)",
        "(A XOR B) AND C",
        "(A OR B) AND (NOT A OR C)",
    ]
    for expr in expresiones:
        imprimir_tabla(expr)
        print()

    # --- Prueba de que los símbolos (∧ ∨ ¬ ⊕) dan el mismo resultado ---
    print("Misma expresión con símbolos en vez de palabras:")
    imprimir_tabla("(A ∧ B) ∨ (¬C)")
    print()

    # --- Evaluación en una entrada concreta ---
    entrada1 = {"A": True, "B": False, "C": True}
    r1 = evaluar_expresion(expresiones[0], entrada1)
    print(f"Evaluar '{expresiones[0]}' con A=V,B=F,C=V -> {'V' if r1 else 'F'}")

    entrada2 = {"A": True, "B": True, "C": False}
    r2 = evaluar_expresion(expresiones[0], entrada2)
    print(f"Evaluar '{expresiones[0]}' con A=V,B=V,C=F -> {'V' if r2 else 'F'}")

    # --- Modo interactivo ---
    print("\n--- Modo interactivo ---")
    expr_usuario = input("Expresión (usa A,B,C,D y AND,OR,NOT,XOR): ")
    try:
        variables, _ = imprimir_tabla(expr_usuario)
        if input("\n¿Evaluar en una entrada concreta? (s/n): ").strip().lower().startswith("s"):
            valores_u = {}
            for var in variables:
                valores_u[var] = input(f"Valor de {var} (V/F): ").strip().upper() == "V"
            resultado = evaluar_expresion(expr_usuario, valores_u)
            print(f"Resultado: {'V' if resultado else 'F'}")
    except ValueError as err:
        print("Error:", err)
