import time
import pandas as pd
from parametros import ANALISE

from tratamento import crop_video, return_acompanhamento
from selecao import encontrar_mais_recorrentes, encontrar_maior_intervalo_sequencial
from arquivos import excluir_frames
from analisar import capturar_video_vivas

time_inicio = time.time()

video_path = "app\\videoalta.mov"
valor_erosao = 8

larvas_por_frame = crop_video(video_path, valor_erosao)

lista_contagens = [item['contagem'] for item in larvas_por_frame]
quantidade_real_larvas = encontrar_mais_recorrentes(lista_contagens)
frames_quantidade_certa = [item['frame'] for item in larvas_por_frame if item['contagem'] == quantidade_real_larvas]

intervalo = encontrar_maior_intervalo_sequencial(frames_quantidade_certa)
excluir_frames(intervalo)

frames_quantidade_certa = [item for item in larvas_por_frame if item["frame"] in intervalo]
analise, rois= capturar_video_vivas(frames_quantidade_certa, intervalo)

frames = len(intervalo)
larvas = quantidade_real_larvas

planilha = pd.DataFrame(index=range(larvas), columns=range(frames))

for indice, frame in enumerate(analise, start=0):
    numero_frame = frame['frame']
    analise = frame["analise"]
    for larva in analise:
        presenca = larva['presença']
        numero_larva = larva['numero_larva']
        planilha.at[larva['numero_larva'], indice] = presenca

mortas, vivas = 0, 0
rois = rois['analise']

roi_mortas = []
for indice, larva in enumerate(rois, start=0):
    dados_larva = planilha.iloc[indice]
    status = any(x == 0 for x in dados_larva)
    if status:
        vivas = vivas + 1
        print("Larva " + str(indice) + " está viva!")
    else:
        mortas = mortas + 1
        roi_mortas.append(larva)
        print("Larva " + str(indice) + " está morta!")

print("Mortas: " + str(mortas) + " Vivas: " + str(vivas)) 
planilha.to_csv('analise.csv', index=False)
time_final = time.time()

return_acompanhamento("app\\videoalta.mov", roi_mortas)

print("Tempo de análise: " + str(time_final - time_inicio))