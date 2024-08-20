# Dada una coleccion de numeros y un valor x, encuentre un par de numeros en la coleccion que sea
# igual a x. Considere que la coleccion de datos puede estar desordenada y puede tener elementos
# repetidos. Implemente una solucion a ese problema al menor costo computacional.

# Ejemplos:
# input: [1, 2, 3, 9]; x = 8
# output: No solution

# input: [1, 2, 4, 4]; x = 8
# output: (4, 4); indexes: (2, 3)

# El algoritmo de búsqueda con conjunto tiene una complejidad de o(n),ya que 
# recorre la lista una vez y realiza operaciones de inserción y búsqueda en un conjunto, que son 
# O(1) en promedio, osea constante, aqui su desarrollo:

def busquedaconconjunto(vector, x):
    vistos = {}
    encontrados = False
    for i, numero in enumerate(vector):
        complemento = x - numero
        if complemento in vistos:
            print(f"({complemento}, {numero}); indexes: ({vistos[complemento]}, {i})")
            encontrados = True
        vistos[numero] = i
    
    if not encontrados:
        print("No solution")

vector = [1, 4]
x = 8
busquedaconconjunto(vector,x)