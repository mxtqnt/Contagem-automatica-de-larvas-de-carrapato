import time
import csv
from parametros import ANALISE, LARVAS_POR_FRAME

from tratamento import crop_video
from selecao import encontrar_mais_recorrentes, encontrar_maior_intervalo_sequencial
from analisar import acompanhar_larvas, acompanhar_larvas_mortas

time_inicio = time.time()

video_path = "app\\videoalta.mov"
valor_erosao = 8

larvas_por_frame = crop_video(video_path, valor_erosao)

lista_contagens = [item['contagem'] for item in larvas_por_frame]
quantidade_real_larvas = encontrar_mais_recorrentes(lista_contagens)
frames_quantidade_certa = [item['frame'] for item in larvas_por_frame if item['contagem'] == quantidade_real_larvas]
intervalo = encontrar_maior_intervalo_sequencial(frames_quantidade_certa)

frameinicial = intervalo[0]

for dicionario in larvas_por_frame:
    if dicionario.get('frame') == frameinicial:
        cordenadas_larvas = dicionario['cordenadas']
        break

matriz = acompanhar_larvas(video_path, cordenadas_larvas, len(larvas_por_frame))

with open('dados_frame.csv', 'w', newline='') as arquivo_csv:
    escritor_csv = csv.writer(arquivo_csv)
    for linha in matriz:
        escritor_csv.writerow(linha)

mortas, vivas = 0, 0

cordenadas_mortas =  []
for index, larva in enumerate(matriz, start=0):
    if 0 in larva:
        vivas += 1
        print(str(index) + " está viva" + str(cordenadas_larvas[index]['center']))
    else:
        mortas += 1
        cordenadas_mortas.append(cordenadas_larvas[index])
        print(str(index) + " está morta" + str(cordenadas_larvas[index]['center']))

print("Mortas: " + str(mortas))
print("Vivas: " + str(vivas))

acompanhar_larvas_mortas(video_path, cordenadas_mortas, len(larvas_por_frame))

print(str(time.time() - time_inicio))