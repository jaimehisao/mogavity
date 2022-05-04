class Stack:
    def __init__(self):
        self.stack = []

    # push es la función de agregar elementos a la pila
    # usamos la función append de List para agregar elemento
    def push(self, value):
        print('added ' + value)
        self.stack.append(value)

    # pop es la función para eliminar el último elemento que se agregó a la pila
    # la función pop() de List tiene la misma función que buscamos
    # tenemos que checar primero si la pila tiene elementos para poder hacer el pop
    def pop(self):
        if len(self.stack) < 1:
            return None
        return self.stack.pop()

    # is_Empty es la función para checar si la pila está vacía
    # checamos si la pila tiene 0 elementos, si es así regresamos True
    def is_Empty(self):
        if len(self.stack) == 0:
            return True
        return False

    # top es la función para que nos regrese el último elemento de la pila
    # primero checamos que no esté vacío y después regresamos el último elemento de la lista
    def top(self):
        if len(self.stack) < 1:
            return None
        return self.stack[-1]

    # size es la función que nos dice cuantos elementos tiene la pila
    # con la función len de Python podemos obtener la cantidad de elementos de la pila
    def size(self):
        return len(self.stack)

    def show_all(self):
        print(*self.stack)
