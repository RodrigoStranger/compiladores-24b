# Compiladores 2024-B

## Autor: Rodrigo Emerson Infanzón Acosta
  
## [`Practica 1`](./binarytrees)
- Crear una clase para en C++ o Python para representar un nodo de un
árbol binario. Este debe contener datos como: key, data, left, y right.
La clase debe tener un constructor para inicializar los atributos, usted
puede agregar mas atributos si lo ve conveniente.

- Implementar un método para buscar un dato en el árbol binario.
Entrada: valor a buscar (según el key)
Salida: el dato encontrado (data), en caso de que no se encuentre: -1

- Implementar un método para agregar un nuevo dato al árbol binario
Entrada: key, data
Salida: True si lo llego a insertar y False si el dato ya existe

- Implementar una función para eliminar elementos.
  
### Entregables
- [`binarytree.cpp`](./binarytrees/binarytree.cpp)

## [`Practica 2`](./exercises)
- Implemente una cola y una pila respectivamente con los metodos pop y push.

- Implemente una funcion que ordene una coleccion de datos. La solucion debe tener como maximo un costo de nlog(n).

- Dada una coleccion de numeros y un valor x, encuentre un par de numeros en la coleccion que sea igual a x. Considere que la coleccion de datos puede estar desordenada y puede tener elementos repetidos. Implemente una solucion a ese problema al menor costo computacional.

### Entregables
- [`exercise01.py`](./exercises/exercise01.py)
- [`exercise02.py`](./exercises/exercise02.py)
- [`exercise03.py`](./exercises/exercise03.py)

## [`Practica 3`](./sketch)
- Traer 3 ejemplos de código fuente en el lenguaje que ustedes proponen e implementen: hola mundo, factorial iterativo, fibonacci recursivo.
- Los ejemplos deben estar en formato .txt.

### Entregables
- [`hola_mundo.txt`](./sketch/hola_mundo.txt)
- [`factorial_iterativo.txt`](./sketch/factorial_iterativo.txt)
- [`fibonacci_recursivo.txt`](./sketch/fibonacci_recursivo.txt)

## Elaboración de un lenguaje de programación compilado: requisitos mínimos
- Estructuras de control: if-else, bucle.
- Funciones y recursividad de funciones.
- Creación de variables y asignación de variables.
- Uso de operadores: +, -, *, /,  or, and, <, <=, >, >=, ==, !=
- Comentarios en linea o bloque.
- Tipos de datos: entero, flotante, booleano y string

## [`Especificación Léxica`](./lexical_specification)
Como parte del desarrollo de un nuevo lenguaje de programación, se debe definir una especificación léxica que incluya los siguientes componentes:
- Definición de los comentarios: Establecer cómo se declararán los comentarios en el código fuente (ej. líneas simples o bloques de comentario).
- Definición de los identificadores: Especificar las reglas para los nombres de variables, funciones, clases, etc. (ej. permitir letras, números, y subrayados, pero que no empiecen con un número).
- Definición de las palabras clave: Definir las palabras reservadas del lenguaje que no se pueden usar como identificadores (ej. if, else, for).
- Definición de los literales: Establecer los diferentes tipos de literales que el lenguaje soportará, como enteros, flotantes, cadenas de texto, etc.
- Definición de los operadores: Definir los operadores aritméticos, lógicos, de comparación, etc., que el lenguaje soportará.
- Expresión regular de cada componente léxico: Crear una tabla donde se describan las expresiones regulares que definen cada uno de los componentes léxicos anteriores.
### Entregables
- [`lexical_specification.pdf`](./lexical_specification/lexical_specification.pdf)
- [`lexical_specification.zip`](./lexical_specification/lexical_specification.zip)
## [`Lexer`](./lexer)


  
