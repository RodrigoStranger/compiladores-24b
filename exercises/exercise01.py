#Implemente una cola y una pila respectivamente con los metodos pop y push.

vector = [1, 2, 3, 4, 5]

#cola: el primero que se agrega es el primero en salir
def enque(vector, valor):
    vector.append(valor)

def deque():
    del vector[0]


#pila: el último elemento que se agrega es el primero en salir
def push(vector, valor):
    vector.append(valor)

def pop(vector):
    return vector.pop()

push(vector,90)
print(vector)
pop(vector)
print(vector)