import math
from simpleai.search import SearchProblem, astar, breadth_first, depth_first
from simpleai.search.viewers import BaseViewer
import time

# Representamos la varilla como una tupla de tres celdas
# Cada celda es una tupla de coordenadas (x, y)
# La varilla siempre está ordenada de izquierda a derecha o de arriba a abajo

# Definición de los laberintos
laberinto1 = [
    ["t","t","t",".",".",".",".",".","."],
    ["#",".",".",".","#",".",".",".","."],
    [".",".",".",".","#",".",".",".","."],
    [".","#",".",".",".",".",".","#","."],
    [".","#",".",".",".",".",".","#","."]
]

laberinto2 = [
    ["t","t","t",".",".",".",".",".","."],
    ["#",".",".",".","#",".",".","#","."],
    [".",".",".",".","#",".",".",".","."],
    [".","#",".",".",".",".",".","#","."],
    [".","#",".",".",".",".",".","#","."]
]

laberinto3 = [
    ["t","t","t"],
    [".",".","."],
    [".",".","."]
]

laberinto4 = [
    ["t","t","t",".",".",".",".",".",".","."],
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

    def puede_moverse(self, x, y, dx, dy, orientacion):
        # Calculamos las nuevas coordenadas de la celda izquierda/superior de la varilla
        nx, ny = x + dx, y + dy
        # Comprobamos si la varilla se saldría del tablero
        if nx < 0 or ny < 0 or nx >= len(self.tablero[0]) or ny >= len(self.tablero):
            return False
        # Comprobamos si la varilla chocaría con una pared
        if self.tablero[ny][nx] == '#':
            return False
        # Si la varilla está en orientación horizontal, comprobamos la celda a la derecha
        if orientacion == 'H' and nx + 2 < len(self.tablero[0]) and self.tablero[ny][nx + 2] == '#':
            return False
        # Si la varilla está en orientación vertical, comprobamos la celda inferior
        if orientacion == 'V' and ny + 2 < len(self.tablero) and self.tablero[ny + 2][nx] == '#':
            return False
        # Si no se dan ninguna de las condiciones anteriores, la varilla puede moverse
        return True

    def puede_cambiar_orientacion(self, x, y, orientacion):
        # Comprobamos si la varilla puede cambiar su orientación sin chocar con una pared o salirse del tablero
        if orientacion == 'H':  # Si la varilla está en orientación horizontal
            # Comprobamos si hay espacio suficiente para cambiar a orientación vertical
            return y + 2 < len(self.tablero) and self.tablero[y + 2][x] != '#'
        else:  # Si la varilla está en orientación vertical
            # Comprobamos si hay espacio suficiente para cambiar a orientación horizontal
            return x + 2 < len(self.tablero[0]) and self.tablero[y][x + 2] != '#'

    def result(self, estado, accion):
        # Aquí necesitamos definir cómo cambia el estado de la varilla en función de la acción tomada
        x, y = estado[0]  # La celda izquierda/superior de la varilla
        orientacion = 'H' if estado[0][1] == estado[1][1] else 'V'

        if accion == 'I':  # Si la acción es mover a la izquierda
            return crear_varilla(x - 1, y, orientacion)
        elif accion == 'D':  # Si la acción es mover a la derecha
            return crear_varilla(x + 1, y, orientacion)
        elif accion == 'A':  # Si la acción es mover hacia arriba
            return crear_varilla(x, y - 1, orientacion)
        elif accion == 'B':  # Si la acción es mover hacia abajo
            return crear_varilla(x, y + 1, orientacion)
        else:  # Si la acción es cambiar la orientación
            return crear_varilla(x, y, 'V' if orientacion == 'H' else 'H')

    def is_goal(self, estado):
        # Aquí necesitamos definir cuándo hemos alcanzado el objetivo
        # En este caso, el objetivo es que la varilla esté en la esquina inferior derecha del tablero, en posición horizontal
        return estado == self.objetivo

    def heuristic(self, estado):
        # Aquí necesitamos definir una función heurística para ayudar a la búsqueda a encontrar la solución más rápidamente
        # En este caso, usamos la distancia de Manhattan entre la celda derecha de la varilla y la celda objetivo
        x, y = estado[2]  # La celda derecha/inferior de la varilla
        gx, gy = self.objetivo[2]  # La celda objetivo
        return abs(gx - x) + abs(gy - y)


def generar_tabla(resultados):
    solucion = resultados.path()
    longitud_total = len(solucion) - 1
    costo_total = resultados.path_cost
    tamaño_maximo = resultados.max_fringe_size
    nodos_visitados = resultados.num_visited_nodes
    iteraciones = resultados.iterations

    tabla = [
        ["Longitud total de la solución", longitud_total],
        ["Costo total de la solución", costo_total],
        ["Tamaño máximo de la frontera", tamaño_maximo],
        ["Nodos visitados", nodos_visitados],
        ["Iteraciones", iteraciones]
    ]

    # Imprimir la tabla en español
    print("Tabla de resultados:")
    print("--------------------")
    for fila in tabla:
        print(f"{fila[0]}: {fila[1]}")
    print("--------------------")


# Función principal que ejecuta el algoritmo de búsqueda
def main():
    print("RESOLVIENDO MEDIANTE A*...")
    for i, laberinto in enumerate(laberintos):
        print(f"Resolviendo laberinto {i + 1}...")
        problema = ProblemaLaberinto(laberinto)
        visor = BaseViewer()
        resultado = astar(problema, graph_search=True, viewer=visor)
        print(f"Solución encontrada: {resultado.path()}")
        generar_tabla(resultado)



# Ejecutamos la función principal
if __name__ == "__main__":
    main()




