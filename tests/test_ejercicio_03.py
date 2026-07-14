def test_ejemplo_del_enunciado():
    r = simular_mpc_promedio([40, 35, 50, 25])
    assert r["suma"] == 150
    assert r["promedio"] == 37.5

def test_una_sola_nota():
    r = simular_mpc_promedio([10])
    assert r["suma"] == 10
    assert r["promedio"] == 10.0

def test_lista_grande_de_cualquier_tamano():
    notas = [i % 51 for i in range(50)]  # 50 notas
    r = simular_mpc_promedio(notas)
    assert r["suma"] == sum(notas)
    assert r["promedio"] == sum(notas) / len(notas)

def test_ningun_servidor_tiene_la_nota_original():
    notas = [40, 35, 50, 25]
    r = simular_mpc_promedio(notas)
    # Ninguna "parte" individual debe coincidir con la nota real
    # (probabilísticamente casi imposible que coincidan al ser valores
    # aleatorios en un rango de 0 a M-1, con M=1000003 >> 50)
    for servidor in r["servidores"]:
        assert servidor != notas

def test_lista_vacia_lanza_error():
    try:
        simular_mpc_promedio([])
        assert False, "Debia lanzar ValueError con lista vacia"
    except ValueError:
        pass

def test_nota_fuera_de_rango_lanza_error():
    try:
        simular_mpc_promedio([40, 60, 10])  # 60 > 50
        assert False, "Debia lanzar ValueError por nota fuera de rango"
    except ValueError:
        pass

test_ejemplo_del_enunciado()
test_una_sola_nota()
test_lista_grande_de_cualquier_tamano()
test_ningun_servidor_tiene_la_nota_original()
test_lista_vacia_lanza_error()
test_nota_fuera_de_rango_lanza_error()
print("Todas las pruebas del Ejercicio 3 pasaron correctamente.")
