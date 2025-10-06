import heapq
import time

# constantes
TORRE_ORIGEN = 0
TORRE_AUXILIAR = 1
TORRE_DESTINO = 2



def generar_sucesores(estado):
    """
    Genera todos los posibles estados sucesores a partir del estado actual. Un movimiento es valido si:
    1 Se mueve el disco superior
    2 Nunca se coloca un disco mas grande sobre uno más pequeño.
    """
    sucesores = []

    for origen in range(3):
        for destino in range(3):
            if origen == destino: continue

            # Se guarda una copia para validar
            torres_listas = [list(pila) for pila in estado]

            # Revisa si el disco superior no es mas grande
            if torres_listas[origen] and \
                    (not torres_listas[destino] or torres_listas[origen][-1] < torres_listas[destino][-1]):
                # Guarda el movimiento en otra lista
                nueva_torres_listas = [list(pila) for pila in estado]
                disco = nueva_torres_listas[origen].pop()
                nueva_torres_listas[destino].append(disco)

                # Estado inmutable (tupla de tuplas)
                nuevo_estado = tuple(tuple(p) for p in nueva_torres_listas)
                movimiento = (origen + 1, destino + 1)
                sucesores.append((nuevo_estado, movimiento))

    return sucesores


# ALGORITMO IDDFS (Busqueda en Profundidad Iterativa)



# Algoritmo A*

def heuristica(estado):
    """
    Heurística: h(n) = 2^k - 1, donde k es el disco mas grande que no este colocado en la tercer torre
    """
    disco_mas_grande_fuera = 0

    # Busca el disco mas grande en la Torre Origen (0) y Auxiliar (1)
    if estado[TORRE_ORIGEN]:
        disco_mas_grande_fuera = max(disco_mas_grande_fuera, max(estado[TORRE_ORIGEN]))

    if estado[TORRE_AUXILIAR]:
        disco_mas_grande_fuera = max(disco_mas_grande_fuera, max(estado[TORRE_AUXILIAR]))

    k = disco_mas_grande_fuera

    if k == 0:
        return 0
    else:
        return (2 ** k) - 1


def resolver_a_estrella(n_discos, estado_inicial, estado_objetivo):
    """Implementacion de A*"""

    # Frontera: (resultado_f, resultado_g, estado, camino)
    frontera = []

    g_inicial = 0
    h_inicial = heuristica(estado_inicial)
    f_inicial = g_inicial + h_inicial
    heapq.heappush(frontera, (f_inicial, g_inicial, estado_inicial, []))

    # estado:resultado_g para evitar expandir caminos peores
    costo_g_minimo = {estado_inicial: g_inicial}

    tiempo_inicio = time.time()

    while frontera:
        f_actual, g_actual, estado_actual, camino_actual = heapq.heappop(frontera)

        # Condicion objetivo
        if estado_actual == estado_objetivo:
            tiempo_fin = time.time()
            return camino_actual, g_actual, tiempo_fin - tiempo_inicio

        # Expansion de Nodos
        for sucesor_estado, movimiento in generar_sucesores(estado_actual):

            g_sucesor = g_actual + 1

            # Si se encuentra un camino mejor (menor costo g) al sucesor
            if g_sucesor < costo_g_minimo.get(sucesor_estado, float('inf')):
                costo_g_minimo[sucesor_estado] = g_sucesor

                h_sucesor = heuristica(sucesor_estado)
                f_sucesor = g_sucesor + h_sucesor

                nuevo_camino = camino_actual + [movimiento]

                heapq.heappush(frontera, (f_sucesor, g_sucesor, sucesor_estado, nuevo_camino))

    tiempo_fin = time.time()
    return None, None, tiempo_fin - tiempo_inicio  # No se encontro solucion


# Funcion para controlar y escoger algoritmo

def comparador():
    """Permite al usuario seleccionar la cantidad de discos y algoritmos a comparar."""

    while True:
        try:
            n_discos = int(input("Ingrese el numero de discos: "))
            if n_discos < 1:
                raise ValueError
            break
        except ValueError:
            print("Por favor, ingrese un numero entero positivo de discos.\n")

    pila_inicial = tuple(range(n_discos, 0, -1))
    # Definición de estados inmutables
    estado_inicial = (pila_inicial, tuple(), tuple())
    estado_objetivo = (tuple(), tuple(), pila_inicial)

    print(f"\nDiscos: {n_discos} ")
    print("\nSeleccione los algoritmos a ejecutar:")
    print("1 Busqueda en Profundidad Iterativa (IDDFS)")
    print("2 A*")
    print("3. Ambos (Para comparar)")

    while True:
        opcion = input("Ingrese su opcion (1, 2, o 3): ")
        if opcion in ['1', '2', '3']:
            break
        print("Opcion no valida")

    resultados = {}

    # --- Ejecutar IDDFS ---
    """
    Aun falta agregar esta parte
    """

    # --- Ejecutar A* ---
    if opcion in ['2', '3']:
        print("\n--- Ejecutando A* ---")
        camino, movimientos, tiempo = resolver_a_estrella(n_discos, estado_inicial, estado_objetivo)
        resultados['A*'] = {'camino': camino, 'movimientos': movimientos, 'tiempo': tiempo}

    # Comparacion
    print("RESULTADOS DE LA COMPARACION")

    for alg, res in resultados.items():
        print(f"\nAlgoritmo: {alg}")
        if res['camino']:
            print(f"Solución Encontrada:")
            print(f"Movimientos realizados: {res['movimientos']}")
            print(f"Tiempo transcurrido: {res['tiempo']:.4f} segundos")
        else:
            print(f"No se encontró solución. Tiempo transcurrido: **{res['tiempo']:.4f} segundos**")


# Ejecutar la función principal
if __name__ == "__main__":
    comparador()