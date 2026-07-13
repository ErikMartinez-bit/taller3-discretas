
# Documento de explicación — Taller de Matemáticas Discretas

## Plantilla por ejercicio (copiar y llenar para cada uno de los 10)

### Ejercicio N — [Nombre del ejercicio]

**Categoría:** cripto / grafos / boole / cuantica

**1. ¿Qué problema resuelve el programa?**


**2. ¿Qué idea matemática usa?**


**3. ¿Cómo se ejecuta?**

```bash
python src/<carpeta>/ejercicio_XX.py
```

**4. ¿Qué pruebas se hicieron?**

| Entrada | Salida esperada | Salida obtenida | ¿Caso límite? |
|---------|------------------|------------------|----------------|
|         |                  |                  |                |

**5. ¿Qué limitaciones tiene la solución?**


---
### Ejercicio 1 — Cifrado César

**Categoría:** cripto

**1. ¿Qué problema resuelve el programa?**

Cifra y descifra mensajes con el cifrado César, y además rompe un mensaje
cifrado cuando no se conoce el desplazamiento, probando las 26 posibilidades.

**2. ¿Qué idea matemática usa?**

Aritmética modular sobre Z_26. El cifrado es la función afín f(x) = (x+k) mod 26.
Como esa suma es invertible (restar k, o sumar 26-k), el cifrado se deshace
aplicando el desplazamiento contrario. La fuerza bruta es posible porque el
espacio de llaves es de solo 26 valores.

**3. ¿Cómo se ejecuta?**

python src/cripto/ejercicio_01.py

Al correrlo, primero muestra el ejemplo del enunciado y la fuerza bruta de
un segundo texto. Luego entra en modo interactivo y pregunta:
(1) Cifrar, (2) Descifrar o (3) Fuerza bruta — pidiendo el texto (y k,
si aplica) por teclado.

**4. ¿Qué pruebas se hicieron?**

| Entrada | Salida esperada | ¿Caso límite? |
|---|---|---|
| cifrar("HOLA UNAL", 3) | "KROD XQDO" | No (ejemplo del enunciado) |
| descifrar(cifrar(texto,k),k) para k=1,5,13,25 | texto original | Sí (k grande) |
| cifrar("Sala #5, 22:00!", 7) | signos/números sin cambio | Sí (no alfabéticos) |
| cifrar(texto,0) y cifrar(texto,26) | igual al original | Sí (desplazamiento nulo/vuelta completa) |
| fuerza_bruta(cifrado) | incluye el texto original entre 26 opciones | Sí (llave desconocida) |

**5. ¿Qué limitaciones tiene la solución?**

Solo funciona con A-Z sin ñ. Tildes, ñ y símbolos de otros idiomas quedan sin
cifrar. No detecta automáticamente cuál de los 26 resultados es el correcto;
eso lo decide quien lee la salida.

---
