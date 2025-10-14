import heapq
import time
import sys

# Se implementa un limite de recursion para problemas mas grandes como 12 discos
sys.setrecursionlimit(5000)

# constantes
TORRE_ORIGEN = 0
TORRE_AUXILIAR = 1
TORRE_DESTINO = 2
NOMBRES_TORRES = {0: 'Origen (A)', 1: 'Auxiliar (B)', 2: 'Destino (C)'}


#Esta funcion se comparte para IDDFS y A*

def generar_sucesores(estado):
    """
    Genera todos los posibles estados sucesores y el movimiento asociado.
    Devuelve (nuevo_estado, (origen, destino)).
    """
    sucesores = []

    for origen in range(3):
        # Evita generar copias si la torre origen esta vacia
        if not estado[origen]:
            continue

        disco_a_mover = estado[origen][-1]

        for destino in range(3):
            if origen == destino: continue

            # Verifica si la torre destino esta vacia o si el disco a mover es mas pequeño
            if not estado[destino] or disco_a_mover < estado[destino][-1]:
                # Crear el nuevo estado
                nueva_torres_listas = [list(pila) for pila in estado]
                nueva_torres_listas[origen].pop()
                nueva_torres_listas[destino].append(disco_a_mover)

                # Estado inmutable (tupla de tuplas)
                nuevo_estado = tuple(tuple(p) for p in nueva_torres_listas)
                movimiento = (origen, destino)
                sucesores.append((nuevo_estado, movimiento))

    return sucesores


#Algoritmo IDDFS

def dfs_limitado(estado_actual, estado_objetivo, limite, visitados, nodos):
    """
    Realiza la busqueda de profundidad limitada y evita ciclos usando "Visitados" como referencia
    """
    nodos[0] += 1
    if estado_actual == estado_objetivo:
        return []  # Se encontro la solucion devuelve la lista de movimientos vacia
    if limite == 0:
        return None

    for sucesor_estado, movimiento in generar_sucesores(estado_actual):

        if sucesor_estado not in visitados:
            # Añade los nodos visitados
            visitados.add(sucesor_estado)

            # Llamada recursiva con limite reducido
            resultado = dfs_limitado(
                sucesor_estado,
                estado_objetivo,
                limite - 1,
                visitados,
                nodos
            )

            if resultado is not None:
                # Si se encuentra, añade el movimiento actual y propaga
                return [movimiento] + resultado
            visitados.remove(sucesor_estado)
    return None


def resolver_iddfs(estado_inicial, estado_objetivo, n_discos):
    """
    Funcion para resolver el problema por busqueda de profundidad iterativa
    """
    nodos_generados = [0]
    tiempo_inicio = time.time()
    movimientos_minimos = (2 ** n_discos) - 1
    limite_max = movimientos_minimos + 1

    for profundidad in range(limite_max + 1):
        # Crea el historial en cada iteracion
        visitados = {estado_inicial}

        # Se manda a llamar la busqueda limitada
        solucion_movimientos = dfs_limitado(
            estado_inicial,
            estado_objetivo,
            profundidad,
            visitados,
            nodos_generados
        )

        if solucion_movimientos is not None:
            tiempo_fin = time.time()
            # La longitud del camino es el numero de movimientos
            return solucion_movimientos, len(solucion_movimientos), nodos_generados[0], tiempo_fin - tiempo_inicio

    tiempo_fin = time.time()
    return None, None, nodos_generados[0], tiempo_fin - tiempo_inicio


#Algoritmo A*

def heuristica(estado):
    """
    Heuristica admisible para Hanoi: 2^k - 1, donde k es el disco mas grande
    que no esta en la torre destino (2).
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
        # Costo minimo para mover 'k' a su posición final
        return (2 ** k) - 1


def resolver_a_estrella(n_discos, estado_inicial, estado_objetivo):
    """Implementacion de A* para Torres de Hanoi."""

    # Frontera: (resultado_f, resultado_g, estado, camino)
    frontera = []
    g_inicial = 0
    h_inicial = heuristica(estado_inicial)
    f_inicial = g_inicial + h_inicial
    heapq.heappush(frontera, (f_inicial, g_inicial, estado_inicial, []))

    # estado:resultado_g para evitar expandir caminos peores
    costo_g_minimo = {estado_inicial: g_inicial}
    nodos_generados = 1  # El estado inicial ya es el primer nodo

    tiempo_inicio = time.time()

    while frontera:
        f_actual, g_actual, estado_actual, camino_actual = heapq.heappop(frontera)

        # Condicion objetivo
        if estado_actual == estado_objetivo:
            tiempo_fin = time.time()
            return camino_actual, g_actual, nodos_generados, tiempo_fin - tiempo_inicio

        # Expansion de Nodos
        for sucesor_estado, movimiento in generar_sucesores(estado_actual):
            nodos_generados += 1
            g_sucesor = g_actual + 1

            # Si se encuentra un camino mejor (menor costo g) al sucesor
            if g_sucesor < costo_g_minimo.get(sucesor_estado, float('inf')):
                costo_g_minimo[sucesor_estado] = g_sucesor

                h_sucesor = heuristica(sucesor_estado)
                f_sucesor = g_sucesor + h_sucesor

                nuevo_camino = camino_actual + [movimiento]

                heapq.heappush(frontera, (f_sucesor, g_sucesor, sucesor_estado, nuevo_camino))

    tiempo_fin = time.time()
    return None, None, nodos_generados, tiempo_fin - tiempo_inicio


#Funcion para comparar y mostrar los resultados

def imprimir_resultados(alg, res):
    """Formatea e imprime los resultados para un algoritmo."""

    # Se extraen las metricas para cada algoritmo
    camino = res.get('camino')
    movimientos = res.get('movimientos')
    nodos = res.get('nodos')
    tiempo = res.get('tiempo')

    print(f"\n Algoritmo: {alg}")
    if camino:
        print(f"Solucion Encontrada: Si")
        print(f"Movimientos realizados:{movimientos}")
        print(f"Nodos Generados: {nodos}")
        print(f"Tiempo transcurrido: {tiempo:.4f} segundos")

        # Mapear movimientos a nombres de torre (A, B, C)
        movimientos_formateados = [
            f"{NOMBRES_TORRES[o]} -> {NOMBRES_TORRES[d]}" for o, d in camino
        ]
        print("Secuencia de movimientos:")
        for i, mov in enumerate(movimientos_formateados):
            print(f"  {i + 1:02d}. {mov}")

    else:
        print(f"No se encontro solucion.")
        print(f"Nodos Generados: {nodos}")
        print(f"Tiempo transcurrido: {tiempo:.4f} segundos")


def comparador():
    """El usuario escoge la cantidad de discos y el algoritmo a utilizar"""

    while True:
        try:
            n_discos = int(input("Ingrese el numero de discos: "))
            if n_discos < 1:
                raise ValueError
            break
        except ValueError:
            print("Ingrese un numero valido de discos\n")

    pila_inicial = tuple(range(n_discos, 0, -1))
    # Se definen los estados inmutables
    estado_inicial = (pila_inicial, tuple(), tuple())
    estado_objetivo = (tuple(), tuple(), pila_inicial)
    mov_minimos = (2 ** n_discos) - 1

    print(f"\nDiscos: {n_discos} | Movimientos optimos: {mov_minimos}")
    print("\nSeleccione los algoritmos a ejecutar:")
    print("1. Busqueda en Profundidad Iterativa (IDDFS)")
    print("2. A* (Busqueda Informada)")
    print("3. Comparacion (Ambos)")

    while True:
        opcion = input("Ingrese su opcion (1, 2, o 3): ")
        if opcion in ['1', '2', '3']:
            break
        print("No valida")

    resultados = {}

    #Ejecutar IDDFS
    if opcion in ['1', '3']:
        print("\nComenzando IDDFS...")
        # Llama a la nueva función
        camino, movimientos, nodos, tiempo = resolver_iddfs(estado_inicial, estado_objetivo, n_discos)
        resultados['IDDFS'] = {'camino': camino, 'movimientos': movimientos, 'nodos': nodos, 'tiempo': tiempo}

    #Ejecutar A*
    if opcion in ['2', '3']:
        print("\nComenzando A*...")
        # Llama a la nueva función
        camino, movimientos, nodos, tiempo = resolver_a_estrella(n_discos, estado_inicial, estado_objetivo)
        resultados['A*'] = {'camino': camino, 'movimientos': movimientos, 'nodos': nodos, 'tiempo': tiempo}

    #Comparacion
    print("\nRESULTADOS DE LA COMPARACION")

    for alg, res in resultados.items():
        imprimir_resultados(alg, res)


# Ejecutar la función principal
if __name__ == "__main__":
    comparador()