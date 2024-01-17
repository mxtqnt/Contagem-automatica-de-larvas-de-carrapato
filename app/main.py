from tratamento import crop_video
from selecao import encontrar_mais_recorrentes, encontrar_maior_intervalo_sequencial
from arquivos import excluir_frames

video_path = "app\\videoalta.mov"
valor_erosao = 8

larvas_por_frame = crop_video(video_path, valor_erosao)

lista_contagens = [item['contagem'] for item in larvas_por_frame]
quantidade_real_larvas = encontrar_mais_recorrentes(lista_contagens)

frames_quantidade_certa = [item['frame'] for item in larvas_por_frame if item['contagem'] == quantidade_real_larvas]
intervalo = encontrar_maior_intervalo_sequencial(frames_quantidade_certa)
excluir_frames(intervalo)