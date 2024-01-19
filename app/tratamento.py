import cv2
import numpy

from parametros import VERBOSO
from contagem import numero_de_larvas_frame, mapear
from arquivos import salvar_frame

def crop_video(caminho_video, valor_erosao):
    if VERBOSO:
        print("Recortando área selecionada do video.")
    cap = cv2.VideoCapture(caminho_video)
    larvas_por_frame = []
    i = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cropped_frame = frame

        imagem_tratada = aplicar_threshold(cropped_frame)
        imagem_tratada = erosion(imagem_tratada, valor_erosao)

        _, contornos = numero_de_larvas_frame(imagem_tratada)
        
        if len(imagem_tratada.shape) == 3:
            h, w, _ = imagem_tratada.shape
        elif len(imagem_tratada.shape) == 2:
            h, w = imagem_tratada.shape

        imagem_branca = numpy.ones((h, w, 3), dtype=numpy.uint8) * 255
        imagem_mapeada, circulos_frame = mapear(imagem_tratada, contornos)
        data = { "frame" : i,
                 "contagem": len(circulos_frame),
                 "cordenadas" : circulos_frame}
        larvas_por_frame.append(data)

        caminho = 'app\\imagens\\' + str (i) + '.png'
        salvar_frame(caminho, imagem_mapeada)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        i = i + 1 
    
    cap.release()
    cv2.destroyAllWindows()

    return larvas_por_frame

def erosion(image, valor):
    if VERBOSO:
        print("Aplicanto erosão.")
    # valor = 8
    kernel = numpy.ones((valor, valor), numpy.uint8) 
    image = cv2.dilate(image, kernel, iterations=1) 
    return image

def aplicar_threshold(frame):
    if VERBOSO:
        print("Aplicanto threshold.")
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresholded_frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
    return thresholded_frame
