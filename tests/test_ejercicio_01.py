def test_cifrado_basico():
    assert cifrar("HOLA UNAL", 3) == "KROD XQDO"

def test_descifrado_es_inverso_del_cifrado():
    texto = "Ataque Al Amanecer, Plan B (fase 2)."
    for k in [1, 5, 13, 25]:
        assert descifrar(cifrar(texto, k), k) == texto

def test_conserva_mayusculas_puntuacion_y_numeros():
    texto = "Sala #5, 22:00!"
    cifrado = cifrar(texto, 7)
    for original, c in zip(texto, cifrado):
        if not original.isalpha():
            assert original == c

def test_caso_limite_desplazamiento_cero_y_26():
    texto = "Prueba Limite"
    assert cifrar(texto, 0) == texto
    assert cifrar(texto, 26) == texto

def test_fuerza_bruta_incluye_la_llave_correcta():
    texto = "Mensaje Secreto"
    k_real = 19
    resultados = fuerza_bruta(cifrar(texto, k_real))
    assert resultados[k_real] == texto
    assert len(resultados) == 26

test_cifrado_basico()
test_descifrado_es_inverso_del_cifrado()
test_conserva_mayusculas_puntuacion_y_numeros()
test_caso_limite_desplazamiento_cero_y_26()
test_fuerza_bruta_incluye_la_llave_correcta()
print("Todas las pruebas del Ejercicio 1 pasaron correctamente.")
