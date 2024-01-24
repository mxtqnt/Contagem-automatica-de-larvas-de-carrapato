import cv2

from parametros import VERBOSO, DEBUG
from selecao import circulos_internos

def numero_de_larvas_frame(imagem):
    if VERBOSO:
        print("Contando larvas por frame.")
    arestas = cv2.Canny(imagem, 50,200)
    contornos, _ = cv2.findContours(arestas.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    numero_de_larvas = len(contornos)

    if DEBUG:
        cv2.putText(imagem, str(numero_de_larvas), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (154, 60, 85), 2)
    
    if len(imagem.shape) == 3:
        h, w, _ = imagem.shape
    elif len(imagem.shape) == 2:
        h, w = imagem.shape

    if DEBUG:
        cv2.namedWindow('Contagem', cv2.WINDOW_NORMAL)
        cv2.imshow('Contagem', imagem)
        cv2.resizeWindow('Contagem', h//4, w//4)
    return numero_de_larvas, contornos


def mapear(imagem, contornos):
    if VERBOSO:
        print("Mapeando larvas por frame.")
    dados_Circulo = []
    for contorno in contornos:
        (x, y), radius = cv2.minEnclosingCircle(contorno)
        center = (int(x), int(y))
        radius = int(radius)

        data = { "center" : center,
                  "radius" :  radius}
        dados_Circulo.append(data)

    circulos_filtrados =  circulos_internos(dados_Circulo)

    for circulo in circulos_filtrados:
        centro = circulo['center']
        raio = circulo['radius']

        cv2.circle(imagem, centro, raio, (0, 0, 0), -1)

    if len(imagem.shape) == 3:
        h, w, _ = imagem.shape
    elif len(imagem.shape) == 2:
        h, w = imagem.shape

    if DEBUG:
        cv2.putText(imagem, str(len(circulos_filtrados)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (154, 60, 85), 2)
        cv2.namedWindow('Circuladas', cv2.WINDOW_NORMAL)
        cv2.imshow('Circuladas', imagem)
        cv2.resizeWindow('Circuladas', h//4, w//4)

    return circulos_filtrados