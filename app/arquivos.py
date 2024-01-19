import os
import cv2
import glob

from parametros import VERBOSO

def salvar_frame(caminho, imagem):
    if VERBOSO:
        print("Salvando imagem: " + caminho + ".")
    cv2.imwrite(caminho, imagem)

def excluir_frames(lista_manter):
    if VERBOSO:
        print("Excluindo frames que não pertencem ao intervalo estável.")
    lista_manter = ["app\\imagens\\" + str(item) + ".png" for item in lista_manter]
    dir = os.listdir("app\\imagens\\")
    for file in dir:
        file = "app\\imagens\\" + file
        if file not in lista_manter:
            os.remove(file)

def salvar_video_seguro(diretorio_imagens):
    print("Salvando video do intervalo estável.")
    nome_video_saida = 'app\\intervalo_seguro.mp4'
    fps = 10

    lista_arquivos = sorted(glob.glob(os.path.join(diretorio_imagens, '*.png')))
    primeira_imagem = cv2.imread(lista_arquivos[0])

    if len(primeira_imagem.shape) == 3:
        altura, largura, _ = primeira_imagem.shape
    elif len(primeira_imagem.shape) == 2:
        altura, largura = primeira_imagem.shape
        
    video_saida = cv2.VideoWriter(nome_video_saida, cv2.VideoWriter_fourcc(*'H264'), fps, (largura, altura))

    for caminho_imagem in lista_arquivos:
        imagem = cv2.imread(caminho_imagem)
        video_saida.write(imagem)

    video_saida.release()
    print(f"Vídeo gerado com sucesso: {nome_video_saida}")
