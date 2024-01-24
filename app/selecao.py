from collections import Counter
from parametros import VERBOSO

def circulos_internos(circulos):
    if VERBOSO:
        print("Excluindo círculos sobressalentes.")
    circulos = sorted(circulos, key=lambda x: x['radius'], reverse=True) 

    indices_para_remover = set()

    for i in range(len(circulos)):
        for j in range(i + 1, len(circulos)):
            distancia_entre_centros = ((circulos[i]['center'][0] - circulos[j]['center'][0]) ** 2 +
                                       (circulos[i]['center'][1] - circulos[j]['center'][1]) ** 2) ** 0.5

            if distancia_entre_centros + circulos[j]['radius'] <= circulos[i]['radius']:
                indices_para_remover.add(j)
            elif distancia_entre_centros < circulos[i]['radius'] + circulos[j]['radius']:
                indices_para_remover.add(j)

    circulos_filtrados = [circulos[i] for i in range(len(circulos)) if i not in indices_para_remover]

    radii = [circulos_filtrados['radius'] for circulos_filtrados in circulos_filtrados]
    media_radius = sum(radii) / len(radii)

    circulos_filtrados = [circle for circle in circulos_filtrados if abs(circle['radius'] - media_radius) <= 0.95 * media_radius]
                  
    return circulos_filtrados

def encontrar_mais_recorrentes(larvas_frame):
    if VERBOSO:
        print("Encontrando contagem mais recorrende e definindo número total.")
    contagem = Counter(larvas_frame)
    tres_maiores = contagem.most_common(3)
    
    if VERBOSO:
        for valor, frequencia in tres_maiores:
            print(f"Valor: {valor}, Recorrência: {frequencia}")

    mais_recorrente = max(tres_maiores, key=lambda x: x[1])
    print(f"A quantidade de larvas é {mais_recorrente[0]}.")

    return mais_recorrente[0]

def encontrar_maior_intervalo_sequencial(array):
    if VERBOSO:
        print("Encontrando intervalo mais estável.")
    array.sort()
    maior_intervalo = []
    atual_intervalo = [array[0]]

    for i in range(1, len(array)):
        if array[i] == array[i - 1] + 1:
            atual_intervalo.append(array[i])
        else:
            if len(atual_intervalo) > len(maior_intervalo):
                maior_intervalo = atual_intervalo
            atual_intervalo = [array[i]]

    if len(atual_intervalo) > len(maior_intervalo):
        maior_intervalo = atual_intervalo

    return maior_intervalo