#Implemente una funcion que ordene una coleccion de datos.
#La solucion debe tener como maximo un costo de nlog(n).

vector = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

#la implementacion de una funcion de ordenamiento (ascendentemente) que posee un costo maximo costo de 
#nlog(n) es el algoritmo de ordemaniento quicksort, aqui su implementacion:

def particion(arreglo, bajo, alto):
    pivote = arreglo[alto]
    i = bajo - 1

    for j in range(bajo, alto):
        if arreglo[j] <= pivote:
            i = i + 1
            arreglo[i], arreglo[j] = arreglo[j], arreglo[i]

    arreglo[i + 1], arreglo[alto] = arreglo[alto], arreglo[i + 1]
    return i + 1

def QuickSort(arreglo, bajo, alto):
    if bajo < alto:
        pi = particion(arreglo, bajo, alto)
        QuickSort(arreglo, bajo, pi - 1)
        QuickSort(arreglo, pi + 1, alto)

print(vector)
QuickSort(vector,0,len(vector)-1)
print(vector)