# NetCode lexer
Este proyecto implementa un analizador léxico para el lenguaje de programación propuesto **NetCode**. El analizador léxico se encarga de leer un archivo de código fuente, identificar los tokens del lenguaje y mostrar estos tokens en una lista de objetos.
## Instalación de [Python](https://www.python.org/)
Para utilizar este analizador léxico, es necesario instalar Python en su ultima versión disponible para `windows`:
- Sitio web oficial: https://www.python.org/
- Video de ayuda: https://www.youtube.com/watch?v=i6j8jT_OdEU

En el caso de `Linux` ya viene preinstalada para la mayoria de las distros.
## Instalación de [pip](https://pypi.org/project/pip/)


En caso no posean el comando pip nativo de Python, seguir las siguientes indicaciones para `windows`:
- Sitio web oficial: https://pypi.org/project/pip/
- Video de ayuda: https://www.youtube.com/watch?v=2wGveK_AQE4


En caso no posean el comando pip nativo de Python, seguir las siguientes indicaciones para `Linux`:
```bash
   sudo apt update
   sudo apt install python3-pip
```
## Instalación de [ply](https://ericknavarro.io/2020/02/10/24-Mi-primer-proyecto-utilizando-PLY/)
El módulo PLY (Python Lex-Yacc). Se puede instalar utilizando cmd en windows:
```bash
pip install ply
```
El módulo PLY (Python Lex-Yacc). Se puede instalar utilizando la terminal en `Linux`:
```bash
sudo apt update
sudo apt install python3-pip
pip3 install ply
```

## Descripción del lexer 
El lexer de **NetCode** utiliza el módulo **PLY** para identificar diferentes componentes léxicos como:
- Funciones
- Tipos de datos
- Operadores
- Literales
- Comentarios
- Identificadores

  
El lexer toma como entrada un archivo de texto que contiene el código fuente y genera una lista de tokens que representan los elementos sintácticos del lenguaje. Estos tokens se almacenan en una lista de objetos `Token`, donde cada objeto contiene:
- Tipo del token
- Valor del token
- Línea donde se encuentra
- Posición en el código
## Código Fuente Lexer: [`AQUI`](./lexic.py)
## EJEMPLOS: [`EXPLICACIÓN DETALLADA`](https://github.com/dabeaz/ply)

## Instalación de [Graphviz](https://graphviz.org/)


Seguir las siguientes indicaciones para `windows`:
- Sitio web oficial: https://graphviz.org/
- Descarga el instalador de Windows.
- Ejecuta el archivo descargado y sigue las instrucciones del asistente de instalación.
- Asegúrate de que la opción "Add Graphviz to the system PATH" esté seleccionada durante la instalación, para que puedas usar Graphviz desde la línea de comandos.
- Una vez instalado, abre la terminal (CMD) y ejecuta dot -version para verificar que Graphviz esté instalado correctamente.


Seguir las siguientes indicaciones para `Linux`:
```bash
   sudo apt-get install graphviz
   dot -version
```

## Descripción del sintactic 
El sintactic de **NetCode** utiliza diferentes componentes léxicos como:
- Lista de tokens (sacada de lexic)
- Función analizador sintáctico
- Función generador tabla ll1.csv
- Estructura de datos: Node, Simbolo
- Gramática.txt
  
## Código Fuente Functions sintactic: [`AQUI`](./functions_sintactic.py)
## Código Fuente Sintactic: [`AQUI`](./sintactic.py)
