import os
import cv2

from parametros import VERBOSO, DEBUG

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