import cv2
import numpy

from parametros import VERBOSO
from contagem import numero_de_larvas_frame, mapear

def crop_video(caminho_video):
    if VERBOSO:
        print("Recortando área selecionada do video.")
    cap = cv2.VideoCapture(caminho_video)
    larvas_por_frame = []
    i = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        if frame_number % 10 == 0:
            imagem_tratada = aplicar_threshold(frame)
            imagem_tratada = erosion(imagem_tratada)

            _, contornos = numero_de_larvas_frame(imagem_tratada)
            
            if len(imagem_tratada.shape) == 3:
                h, w, _ = imagem_tratada.shape
            elif len(imagem_tratada.shape) == 2:
                h, w = imagem_tratada.shape

            imagem_branca = numpy.ones((h, w, 3), dtype=numpy.uint8) * 255
            circulos_frame = mapear(imagem_branca, contornos)
            data = { "frame" : i,
                    "contagem": len(circulos_frame),
                    "cordenadas" : circulos_frame}
            larvas_por_frame.append(data)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            i = i + 1 
    
    cap.release()
    cv2.destroyAllWindows()

    return larvas_por_frame

def erosion(image):
    if VERBOSO:
        print("Aplicanto erosão.")
    kernel = numpy.ones((8, 8), numpy.uint8) 
    image = cv2.dilate(image, kernel, iterations=1) 
    return image

def aplicar_threshold(frame):
    if VERBOSO:
        print("Aplicanto threshold.")
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresholded_frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
    return thresholded_frame