import time
import pandas as pd
from parametros import ANALISE

from tratamento import crop_video
from selecao import encontrar_mais_recorrentes, encontrar_maior_intervalo_sequencial
from arquivos import excluir_frames, salvar_video_seguro
from analisar import capturar_video_vivas, resultado_larva
from planilha import criar_planilha, inserir_dado

video_path = "app\\videoalta.mov"
valor_erosao = 8

larvas_por_frame = crop_video(video_path, valor_erosao)

lista_contagens = [item['contagem'] for item in larvas_por_frame]
quantidade_real_larvas = encontrar_mais_recorrentes(lista_contagens)
frames_quantidade_certa = [item['frame'] for item in larvas_por_frame if item['contagem'] == quantidade_real_larvas]

intervalo = encontrar_maior_intervalo_sequencial(frames_quantidade_certa)
excluir_frames(intervalo)

frames_quantidade_certa = [item for item in larvas_por_frame if item["frame"] in intervalo]
analise = capturar_video_vivas(frames_quantidade_certa, intervalo)

frames = len(frames_quantidade_certa)
larvas = quantidade_real_larvas

planilha = pd.DataFrame(index=range(larvas), columns=range(frames))

for indice, frame in enumerate(analise, start=0):
    numero_frame = frame['frame']
    analise = frame["analise"]
    for larva in analise:
        presenca = larva['presença']
        numero_larva = larva['numero_larva']
        planilha.at[larva['numero_larva'], indice] = presenca

mortas = 0
vivas = 0

for indice in range(36):
    dados_larva = planilha.iloc[indice]
    status = sum(1 for item in dados_larva if item == 0) >= 0.3 * len(dados_larva)
    if status:
        vivas = vivas + 1
        print("Larva " + str(indice) + " está viva!")
    else:
        mortas = mortas + 1
        print("Larva " + str(indice) + " está morta!")

print("Mortas: " + str(mortas) + " Vivas: " + str(vivas))
time.sleep(5)

planilha.to_csv('app\\analise.csv', index=False)