import math
from simpleai.search import SearchProblem, astar
from simpleai.search.viewers import BaseViewer, ConsoleViewer

# Representamos la varilla como una tupla de tres celdas
# Cada celda es una tupla de coordenadas (x, y)
# La varilla siempre está ordenada de izquierda a derecha o de arriba a abajo (por ello necesitamos saber su posicion tanto horizontal como vertical)

# Definición de los laberintos
laberinto1 = [
    [".",".",".",".",".",".",".",".","."],
    ["#",".",".",".","#",".",".",".","."],
    [".",".",".",".","#",".",".",".","."],
    [".","#",".",".",".",".",".","#","."],
    [".","#",".",".",".",".",".","#","."]
]

laberinto2 = [
    [".",".",".",".",".",".",".",".","."],
    ["#",".",".",".","#",".",".","#","."],
    [".",".",".",".","#",".",".",".","."],
    [".","#",".",".",".",".",".","#","."],
    [".","#",".",".",".",".",".","#","."]
]

laberinto3 = [
    [".",".","."],
    [".",".","."],
    [".",".","."]
]

laberinto4 = [
    [".",".",".",".",".",".",".",".",".","."],
    [".","#",".",".",".",".","#",".",".","."],
    [".","#",".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".",".",".","."],
    [".","#",".",".",".",".",".",".",".","."],
    [".","#",".",".",".","#",".",".",".","."],
    [".",".",".",".",".",".","#",".",".","."],
    [".",".",".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".",".",".","."]
]

# Agrupamos todos los laberintos en una lista
laberintos = [laberinto1, laberinto2, laberinto3, laberinto4]

def crear_varilla(x, y, orientacion):
    if orientacion == 'H':
        return ((x, y), (x+1, y), (x+2, y))
    else:  # orientacion == 'V'
        return ((x, y), (x, y+1), (x, y+2))

class ProblemaLaberinto(SearchProblem):  # Definimos una clase que hereda de SearchProblem
    def __init__(self, tablero):  # Método de inicialización de la clase
        self.tablero = tablero  # Guardamos el tablero del laberinto
        # Definimos el estado objetivo como la varilla en la esquina inferior derecha del tablero, en posición horizontal
        self.objetivo = crear_varilla(len(tablero[0])-3, len(tablero)-1, 'H')

        # Buscamos la posición inicial de la varilla en el tablero
        for y in range(len(self.tablero)):  # Recorremos las filas del tablero
            for x in range(len(self.tablero[y])):  # Recorremos las celdas de cada fila
                if self.tablero[y][x].lower() == 't':  # Si encontramos una celda con la letra 't'
                    self.inicial = crear_varilla(x, y, 'H')  # Asumimos que esta es la posición inicial de la varilla y la creamos en posición horizontal

        # Llamamos al método de inicialización de la clase padre, pasando el estado inicial que hemos encontrado
        super(ProblemaLaberinto, self).__init__(initial_state=self.inicial)

    def actions(self, estado):
        # Aquí necesitamos definir las acciones posibles para la varilla
        # Esto incluirá mover la varilla una celda en cualquier dirección y cambiar su orientación
        acciones = []
        x, y = estado[0]  # La celda izquierda/superior de la varilla
        orientacion = 'H' if estado[0][1] == estado[1][1] else 'V'

        # Comprobamos si la varilla puede moverse en cada dirección
        if self.puede_moverse(x, y, -1, 0, orientacion):  # Izquierda
            acciones.append('I')
        if self.puede_moverse(x, y, 1, 0, orientacion):  # Derecha
            acciones.append('D')
        if self.puede_moverse(x, y, 0, -1, orientacion):  # Arriba
            acciones.append('A')
        if self.puede_moverse(x, y, 0, 1, orientacion):  # Abajo
            acciones.append('B')

        # Comprobamos si la varilla puede cambiar su orientación
        if self.puede_cambiar_orientacion(x, y, orientacion):
            acciones.append('C')

        return acciones
        pass

    def result(self, estado, accion):
        # Aquí necesitamos definir el resultado de aplicar una acción a un estado
        # Esto implicará mover la varilla o cambiar su orientación
        pass

    def is_goal(self, estado):
        # Aquí necesitamos comprobar si el estado es un estado objetivo
        # Un estado es un estado objetivo si la varilla está en la esquina inferior derecha del laberinto
        return estado == self.objetivo

    def cost(self, estado, accion, estado2):
        # El coste de cada acción es 1, independientemente de la acción
        return 1

    def heuristic(self, estado):
        # Aquí necesitamos definir la heurística para el algoritmo A*
        # Podemos usar la distancia de Manhattan desde la celda derecha/inferior de la varilla hasta la esquina inferior derecha del laberinto
        x, y = estado[2]  # La celda derecha/inferior de la varilla
        gx, gy = self.objetivo[2]  # La celda derecha/inferior del objetivo
        return abs(x - gx) + abs(y - gy)

# Aquí iría el resto del código, incluyendo la función principal y las funciones para visualizar el resultado


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def main():

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
