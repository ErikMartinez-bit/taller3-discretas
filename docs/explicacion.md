
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
### Ejercicio 2 — RSA de juguete

**Categoría:** cripto

**1. ¿Qué problema resuelve el programa?**

Genera llaves RSA (n, d) a partir de dos primos p, q y un exponente público
e, y usa esas llaves para cifrar y descifrar un mensaje numérico M. Es una
versión educativa: no debe usarse como seguridad real.

**2. ¿Qué idea matemática usa?**

Aritmética modular y el teorema de Euler. n = p*q, phi(n) = (p-1)(q-1). El
exponente privado d es el inverso modular de e módulo phi(n) (calculado con
el algoritmo de Euclides extendido), que existe solo si gcd(e, phi(n)) = 1.
Cifrado y descifrado son congruencias: C ≡ M^e (mod n), M ≡ C^d (mod n). El
teorema de Euler garantiza que M^(e*d) ≡ M (mod n) porque e*d ≡ 1 (mod phi(n)).
Los primos p, q son el secreto: sin ellos no se puede calcular phi(n) ni d.

**3. ¿Cómo se ejecuta?**

python src/cripto/ejercicio_02.py

Muestra el caso obligatorio del enunciado y un segundo ejemplo con otros
números. Luego entra en modo interactivo y pide p, q, e y M por teclado.

**4. ¿Qué pruebas se hicieron?**

| Entrada | Salida esperada | ¿Caso límite? |
|---|---|---|
| p=61,q=53,e=17,M=65 | n=3233, phi=3120, d=2753, C=2790, M=65 | No (caso obligatorio) |
| p=17,q=11,e=7,M=88 | C=11, descifrado=88 | No (otro ejemplo conocido) |
| (17*d) mod phi(n) | 1 | No (verifica inverso modular) |
| p=5,q=11,e=8 | lanza ValueError (gcd(e,phi)=8≠1) | Sí (e inválido) |
| p=5,q=11,e=3,M=55 (M=n) | descifrado=0 | Sí (M no menor que n) |

**5. ¿Qué limitaciones tiene la solución?**

Solo funciona correctamente si M < n; si M ≥ n, el resultado se reduce
módulo n y se pierde información (limitación matemática de RSA, no un bug).
No verifica que p y q sean primos ni que e sea válido en rango; solo valida
que gcd(e, phi(n)) = 1. Con primos pequeños no ofrece seguridad real.

---
### Ejercicio 3 — MPC básico: promedio sin mostrar los datos

**Categoría:** cripto

**1. ¿Qué problema resuelve el programa?**

Simula un cálculo multipartito seguro (MPC): tres servidores calculan la
suma y el promedio de una lista de notas sin que ninguno vea una nota
completa en ningún momento.

**2. ¿Qué idea matemática usa?**

Secret sharing aditivo módulo M. Cada nota x se reparte en 3 partes
aleatorias s1, s2, s3 tales que x ≡ s1 + s2 + s3 (mod M). Ejemplo pequeño
con M=97 y x=40: se eligen al azar s1=53 y s2=61, y se calcula
s3 = (40 - 53 - 61) mod 97 = 23. Comprobación: (53+61+23) mod 97 = 137 mod
97 = 40. Cada s_i por separado es un número "al azar" en [0, M) que no
revela nada de x; solo sumando las 3 partes se recupera x. Cada servidor
suma únicamente las partes que le tocaron de todas las notas (suma
parcial); al sumar las 3 sumas parciales (mod M) se reconstruye la suma
total real, sin que ningún servidor haya reconstruido una nota individual.

**3. ¿Cómo se ejecuta?**

python src/cripto/ejercicio_03.py

Corre el ejemplo del enunciado y un segundo ejemplo con más notas. Luego
pide en modo interactivo una lista de notas separadas por coma.

**4. ¿Qué pruebas se hicieron?**

| Entrada | Salida esperada | ¿Caso límite? |
|---|---|---|
| [40, 35, 50, 25] | suma=150, promedio=37.5 | No (ejemplo del enunciado) |
| [10] | suma=10, promedio=10.0 | Sí (una sola nota) |
| lista de 50 notas | suma y promedio coinciden con cálculo directo | Sí (lista grande) |
| vistas de cada servidor | ninguna coincide con la lista real de notas | No (verifica privacidad) |
| [] (lista vacía) | lanza ValueError | Sí (lista vacía) |
| [40, 60, 10] (60 fuera de rango) | lanza ValueError | Sí (nota inválida) |

**5. ¿Qué limitaciones tiene la solución?**

Es una simulación en un solo programa: los "servidores" son listas en
memoria, no procesos ni máquinas separadas realmente aisladas. Solo
funciona bien si la suma real de las notas es menor que M; con M=1000003
y notas de 0 a 50, esto es seguro para cursos de tamaño normal, pero no
se valida automáticamente si M fuera más pequeño o el curso enorme.

---
