from collections import defaultdict

class NodoFP:
    def __init__(self, item, padre):
        self.item = item
        self.cuenta = 1
        self.padre = padre
        self.hijos = {}
        self.enlace = None

class ArbolFP:
    def __init__(self):
        self.raiz = NodoFP(None, None)
        self.tabla_encabezado = defaultdict(list)

    def insertar(self, transaccion):
        nodo_actual = self.raiz
        for item in transaccion:
            if item in nodo_actual.hijos:
                nodo_actual.hijos[item].cuenta += 1
            else:
                nuevo_nodo = NodoFP(item, nodo_actual)
                nodo_actual.hijos[item] = nuevo_nodo
                self.tabla_encabezado[item].append(nuevo_nodo)
            nodo_actual = nodo_actual.hijos[item]

def imprimir_arbol(nodo, indentacion=0):

    if nodo.item is not None:
        print(' ' * indentacion + f"Ítem: {nodo.item}, Cuenta: {nodo.cuenta}")

    for hijo in nodo.hijos.values():
        imprimir_arbol(hijo, indentacion + 4)

def minar_arbol(arbol, soporte_minimo, prefijo, conjuntos_frecuentes):
    for item, nodos in arbol.tabla_encabezado.items():
        soporte = sum(nodo.cuenta for nodo in nodos)
        if soporte >= soporte_minimo:
            nuevo_conjunto_frecuente = prefijo + [item]
            conjuntos_frecuentes.append((nuevo_conjunto_frecuente, soporte))

            arbol_condicional = construir_arbol_condicional(nodos)
            minar_arbol(arbol_condicional, soporte_minimo, nuevo_conjunto_frecuente, conjuntos_frecuentes)

def construir_arbol_condicional(nodos):
    arbol_condicional = ArbolFP()
    for nodo in nodos:
        camino = []
        nodo_actual = nodo
        while nodo_actual.padre.item is not None:
            camino.append(nodo_actual.padre.item)
            nodo_actual = nodo_actual.padre
        camino = list(reversed(camino))
        if camino:
            arbol_condicional.insertar(camino)
    return arbol_condicional

def fpgrowth_con_impresion(transacciones, soporte_minimo):
    arbol = ArbolFP()
    for transaccion in transacciones:
        transaccion_ordenada = sorted(transaccion)  
        arbol.insertar(transaccion_ordenada)


    print("Estructura del Árbol FP:")
    imprimir_arbol(arbol.raiz)
    

    conjuntos_frecuentes = []
    minar_arbol(arbol, soporte_minimo, [], conjuntos_frecuentes)
    
    return conjuntos_frecuentes


with open('datos1.txt') as archivo:
    transacciones = [linea.split() for linea in archivo]


soporte_minimo = 3


conjuntos_frecuentes = fpgrowth_con_impresion(transacciones, soporte_minimo)
print("\nConjuntos frecuentes:")
print(conjuntos_frecuentes)
