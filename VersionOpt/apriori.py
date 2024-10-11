import itertools

def Apriori_gen(itemset, tamano):
    candidatos = []
    for i in range(tamano):
        elemento_i = itemset[i]
        for j in range(i + 1, tamano):
            elemento_j = itemset[j]
            
            if elemento_i[:-1] == elemento_j[:-1]:
                nuevo_itemset = elemento_i + elemento_j[-1]
                candidatos.append(nuevo_itemset)
    
    return candidatos

def Apriori_prune(candidato_count, min_support):
    return sorted([item for item, count in candidato_count.items() if count >= min_support])

def Apriori_conteo_subset(candidatos, tamano_candidatos):

    conteo = dict()

    with open('datos2.txt') as archivo:
        transacciones = [linea.split() for linea in archivo]
    
    for candidato in candidatos:
        conteo[candidato] = 0
        conjunto_candidato = set(candidato)
        
        for transaccion in transacciones:
            if conjunto_candidato.issubset(transaccion):
                conteo[candidato] += 1
                
    return conteo

def generar_reglas_asociacion(itemsets_frecuentes, soporte, min_confianza):

    reglas = []    
    for itemset in itemsets_frecuentes:
        if len(itemset) > 1:

            for i in range(1, len(itemset)):

                for antecedente in itertools.combinations(itemset, i):
                    antecedente = set(antecedente)
                    consecuente = set(itemset) - antecedente
                    antecedente_str = ''.join(sorted(antecedente))
                    consecuente_str = ''.join(sorted(consecuente))
                    itemset_str = ''.join(sorted(itemset)) 
                    
                    if itemset_str in soporte and antecedente_str in soporte:
                        soporte_itemset = soporte[itemset_str]
                        soporte_antecedente = soporte[antecedente_str]
                        confianza = soporte_itemset / soporte_antecedente
                        if confianza >= min_confianza:
                            regla = (antecedente, consecuente, confianza)
                            reglas.append(regla)
    
    return reglas


min_support = 3
min_confianza = 0.6


C1 = {}
with open('datos1.txt') as archivo:
    for linea in archivo:
        for item in linea.split():
            if item in C1:
                C1[item] += 1
            else:
                C1[item] = 1

print("C1 (conteo de 1-itemsets):", C1)

L1 = Apriori_prune(C1, min_support)
print('***************************************')
print('Frecuencia 1-itemset:', L1)
print('***************************************')

k = 2
L = Apriori_gen(L1, len(L1))
itemsets_frecuentes = L1.copy()
soporte_itemsets = C1.copy()
while L:
    C = Apriori_conteo_subset(L, len(L))
    print(f'------------------------------------')
    print(f'Conjuntos de {k}-itemsets generados:', L)
    L_filtrados = Apriori_prune(C, min_support)
    print(f'Frecuencia {k}-itemset:', L_filtrados)
    print('------------------------------------')
    itemsets_frecuentes.extend(L_filtrados)
    soporte_itemsets.update(C)
    L = Apriori_gen(L_filtrados, len(L_filtrados))
    k += 1
reglas = generar_reglas_asociacion(itemsets_frecuentes, soporte_itemsets, min_confianza)
print('***************************************')
print('Reglas de Asociación:')
for antecedente, consecuente, confianza in reglas:
    print(f'{antecedente} -> {consecuente} (Confianza: {confianza:.2f})')
