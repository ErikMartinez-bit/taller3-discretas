def test_caso_obligatorio_del_enunciado():
    n, phi_n, d = generar_llaves(61, 53, 17)
    C = cifrar(65, 17, n)
    assert (n, phi_n, d, C) == (3233, 3120, 2753, 2790)
    assert descifrar(C, d, n) == 65

def test_ejemplo_conocido_wikipedia():
    # p=17, q=11, e=7, M=88 -> C=11, descifrado=88
    n, phi_n, d = generar_llaves(17, 11, 7)
    C = cifrar(88, 7, n)
    assert C == 11
    assert descifrar(C, d, n) == 88

def test_inverso_modular_es_correcto():
    n, phi_n, d = generar_llaves(61, 53, 17)
    assert (17 * d) % phi_n == 1

def test_e_invalido_lanza_error():
    # p=5, q=11 -> phi(n)=40; e=8 no es coprimo con 40 (gcd=8)
    try:
        generar_llaves(5, 11, 8)
        assert False, "Debia lanzar ValueError por e invalido"
    except ValueError:
        pass

def test_mensaje_mayor_o_igual_que_n_caso_limite():
    n, phi_n, d = generar_llaves(5, 11, 3)  # n=55
    C = cifrar(55, 3, n)          # M == n, caso limite
    assert descifrar(C, d, n) == 0  # 55 mod 55 = 0: limitacion esperada

test_caso_obligatorio_del_enunciado()
test_ejemplo_conocido_wikipedia()
test_inverso_modular_es_correcto()
test_e_invalido_lanza_error()
test_mensaje_mayor_o_igual_que_n_caso_limite()
print("Todas las pruebas del Ejercicio 2 pasaron correctamente.")
