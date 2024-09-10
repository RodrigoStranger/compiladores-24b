# NetCode lexer
Este proyecto implementa un analizador léxico para el lenguaje de programación propuesto **NetCode**. El analizador léxico se encarga de leer un archivo de código fuente, identificar los tokens del lenguaje y mostrar estos tokens en una lista de objetos.
## Instalación de [Python](https://www.python.org/)
Para utilizar este analizador léxico, es necesario instalar Python en su ultima versión disponible:
- Sitio web oficial: https://www.python.org/
- Video de ayuda: https://www.youtube.com/watch?v=i6j8jT_OdEU
## Instalación de [pip](https://pypi.org/project/pip/)
- En caso no posean el comando pip nativo de Python, seguir las siguientes indicaciones para windows:
- Sitio web oficial: https://pypi.org/project/pip/
- Video de ayuda: https://www.youtube.com/watch?v=2wGveK_AQE4
- En caso no posean el comando pip nativo de Python, seguir las siguientes indicaciones para linux:
```bash
   sudo apt update
   sudo apt install python3-pip
```
## Instalación de [ply](https://ericknavarro.io/2020/02/10/24-Mi-primer-proyecto-utilizando-PLY/)
El módulo PLY (Python Lex-Yacc). Se puede instalar utilizando cmd en windows:
```bash
pip install ply
```
El módulo PLY (Python Lex-Yacc). Se puede instalar utilizando la terminal en linux:
```bash
sudo pip3 install ply
```
## Verificación de instalación de [ply](https://ericknavarro.io/2020/02/10/24-Mi-primer-proyecto-utilizando-PLY/)
```bash
pip show ply
```
## Descripción del lexer 
El lexer de **NetCode** utiliza el módulo **PLY** para identificar diferentes componentes léxicos como:
- Funciones
- Tipos de datos
- Operadores
- Literales
- Comentarios
- Identificadores <br>
El lexer toma como entrada un archivo de texto que contiene el código fuente y genera una lista de tokens que representan los elementos sintácticos del lenguaje. Estos tokens se almacenan en una lista de objetos `Token`, donde cada objeto contiene:
- Tipo del token
- Valor del token
- Línea donde se encuentra
- Posición en el código
