import itertools

def Apriori_gen(itemset, tamano):
    """Genera candidatos (k-itemsets) a partir de un (k-1)-itemset"""
    candidatos = []
    
    # Generación de k-itemsets sin usar sets
    for i in range(tamano):
        elemento_i = itemset[i]
        for j in range(i + 1, tamano):
            elemento_j = itemset[j]
            
            # Verificar si los primeros k-2 elementos son iguales
            if elemento_i[:-1] == elemento_j[:-1]:
                # Combinar los últimos elementos de ambos itemsets
                nuevo_itemset = elemento_i + elemento_j[-1]
                
                # Agregar a la lista si no está ya
                candidatos.append(nuevo_itemset)
    
    return candidatos

def Apriori_prune(candidato_count, min_support):
    """Filtra candidatos que cumplen con el soporte mínimo"""
    return sorted([item for item, count in candidato_count.items() if count >= min_support])

def Apriori_conteo_subset(candidatos, tamano_candidatos):
    """Cuenta las veces que cada k-itemset está presente en las transacciones"""
    conteo = dict()
    
    # Cargar datos del archivo
    with open('datos2.txt') as archivo:
        transacciones = [linea.split() for linea in archivo]
    
    # Contar subconjuntos
    for candidato in candidatos:
        conteo[candidato] = 0
        conjunto_candidato = set(candidato)
        
        for transaccion in transacciones:
            # Verificar si el k-itemset está en la transacción
            if conjunto_candidato.issubset(transaccion):
                conteo[candidato] += 1
                
    return conteo

def generar_reglas_asociacion(itemsets_frecuentes, soporte, min_confianza):
    """Genera reglas de asociación a partir de los ítems frecuentes"""
    reglas = []
    
    # Para cada ítem frecuente de tamaño >= 2
    for itemset in itemsets_frecuentes:
        if len(itemset) > 1:
            # Generar todas las combinaciones posibles
            for i in range(1, len(itemset)):
                # Subconjuntos posibles del ítemset
                for antecedente in itertools.combinations(itemset, i):
                    antecedente = set(antecedente)
                    consecuente = set(itemset) - antecedente
                    
                    # Calcular soporte y confianza
                    antecedente_str = ''.join(sorted(antecedente))
                    consecuente_str = ''.join(sorted(consecuente))
                    itemset_str = ''.join(sorted(itemset))  # Nueva clave para el ítemset
                    
                    # Verificar que las claves existen en el soporte
                    if itemset_str in soporte and antecedente_str in soporte:
                        soporte_itemset = soporte[itemset_str]
                        soporte_antecedente = soporte[antecedente_str]
                        
                        confianza = soporte_itemset / soporte_antecedente
                        
                        # Agregar la regla si cumple con el umbral de confianza
                        if confianza >= min_confianza:
                            regla = (antecedente, consecuente, confianza)
                            reglas.append(regla)
    
    return reglas

# Parámetros de soporte mínimo y confianza mínima
min_support = 2
min_confianza = 0.4

# Paso 1: Generar C1 (conteo de 1-itemsets)
C1 = {}
with open('datos1.txt') as archivo:
    for linea in archivo:
        for item in linea.split():
            if item in C1:
                C1[item] += 1
            else:
                C1[item] = 1

print("C1 (conteo de 1-itemsets):", C1)

# Paso 2: Filtrar C1 con soporte mínimo
L1 = Apriori_prune(C1, min_support)
print('***************************************')
print('Frecuencia 1-itemset:', L1)
print('***************************************')


# Paso 3: Generar conjuntos de mayor tamaño
k = 2
L = Apriori_gen(L1, len(L1))

# Almacenar todos los ítems frecuentes y sus soportes
itemsets_frecuentes = L1.copy()
soporte_itemsets = C1.copy()  # Soporte de los ítems frecuentes

while L:
    # Paso 4: Contar candidatos en las transacciones
    C = Apriori_conteo_subset(L, len(L))
    
    # Imprimir todos los k-itemsets generados
    print(f'------------------------------------')
    print(f'Conjuntos de {k}-itemsets generados:', L)

    # Paso 5: Filtrar con soporte mínimo
    L_filtrados = Apriori_prune(C, min_support)
    
    # Imprimir los k-itemsets que cumplen con el soporte
    print(f'Frecuencia {k}-itemset:', L_filtrados)
    print('------------------------------------')
    
    # Almacenar ítems frecuentes y sus soportes
    itemsets_frecuentes.extend(L_filtrados)
    soporte_itemsets.update(C)
    
    # Generar (k+1)-itemsets
    L = Apriori_gen(L_filtrados, len(L_filtrados))  # Cambiado para usar L_filtrados
    k += 1

# Generar reglas de asociación
reglas = generar_reglas_asociacion(itemsets_frecuentes, soporte_itemsets, min_confianza)

# Mostrar las reglas generadas
print('***************************************')
print('Reglas de Asociación:')
for antecedente, consecuente, confianza in reglas:
    print(f'{antecedente} -> {consecuente} (Confianza: {confianza:.2f})')
