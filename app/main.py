import time
import csv
import os

from tratamento import crop_video
from selecao import encontrar_mais_recorrentes, encontrar_maior_intervalo_sequencial
from analisar import acompanhar_larvas, acompanhar_larvas_mortas

caminho = 'videos\\' 

matrizcsv = []
matrizcsv.append([0] * 4)

matrizcsv[0][0], matrizcsv[0][1], matrizcsv[0][2], matrizcsv[0][3] = 'Video', 'Vivas', 'Mortas', 'Tempo de Análise'

for numero_video, video in enumerate(os.listdir(caminho), start=1):
    time_inicio = time.time()
    video_path = caminho + video
    
    ponto = video.find(".")
    if ponto != -1:
        nomevideo = video[:ponto + 1]

    print("Analisando: " + video)

    larvas_por_frame = crop_video(video_path)

    lista_contagens = [item['contagem'] for item in larvas_por_frame]
    quantidade_real_larvas = encontrar_mais_recorrentes(lista_contagens)
    frames_quantidade_certa = [item['frame'] for item in larvas_por_frame if item['contagem'] == quantidade_real_larvas]
    intervalo = encontrar_maior_intervalo_sequencial(frames_quantidade_certa)

    frameinicial = intervalo[0]

    for dicionario in larvas_por_frame:
        if dicionario.get('frame') == frameinicial:
            cordenadas_larvas = dicionario['cordenadas']
            break

    time_segundo_processamento = time.time()
    matriz = acompanhar_larvas(video_path, cordenadas_larvas, len(larvas_por_frame))

    mortas, vivas = 0, 0
    cordenadas_mortas =  []

    index = 0
    for larva in matriz:
        if 0 in larva:
            vivas += 1
        else:
            mortas += 1
            cordenadas_mortas.append(cordenadas_larvas[index])
        index += 1

    print("Mortas: " + str(mortas))
    print("Vivas: " + str(vivas))
    acompanhar_larvas_mortas(video_path, cordenadas_mortas, nomevideo)

    print("Tempo de processamento: " + str(time.time() - time_inicio) + " segundos.")

    matrizcsv.append([0] * 4)
    matrizcsv[numero_video][0], matrizcsv[numero_video][1], matrizcsv[numero_video][2], matrizcsv[numero_video][3] = video, vivas, mortas, str(time.time() - time_inicio)


with open('AnaliseVideos.csv', 'w', newline='') as arquivo_csv:
    escritor_csv = csv.writer(arquivo_csv)
    for linha in matrizcsv:
        escritor_csv.writerow(linha)