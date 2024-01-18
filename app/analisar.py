import numpy
import cv2
import time

from parametros import VERBOSO

def capturar_video_vivas(larvas_por_frame, frames):
    if VERBOSO:
        print("Analisando intervalo estável")

    cordenadas_larvas = larvas_por_frame[0]["cordenadas"]
    data_frame = []
        
    for numero_frame in frames:
        framedir = "app\\imagens\\" + str(numero_frame) + ".png"
        frame = cv2.imread(framedir)
        
        lista_roi = []

        for numero_larva, larva in enumerate(cordenadas_larvas, start=0):
            centro = larva["center"]
            raio = larva["radius"]
            largura = raio*2
            x = centro[0] - raio
            y = centro[1] - raio
            roi = frame[y:y+largura, x:x+largura]
            pretos = numpy.sum(roi == 0)
            larva = {   "numero_larva" : numero_larva,
                        "presença" : pretos}
            frame = cv2.rectangle(frame, (x, y), (x+largura, y+largura), (255, 0, 255), 1) 
            frame = cv2.putText(frame, ('Presença: ' + str(pretos)), (x, y + largura + 10), cv2.FONT_HERSHEY_SIMPLEX , 0.3, (255, 0, 255), 1, cv2.LINE_AA) 

            lista_roi.append(larva)

        data = {    "frame" : numero_frame,
                    "analise" : lista_roi}
        data_frame.append(data)
        numero_frame = numero_frame + 1
        print(numero_frame)

        h, w, _ = frame.shape

        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.imshow('frame', frame)
        cv2.resizeWindow('frame', int(h//1.5), int(w//1.5))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # time.sleep(1)

    with open('analise.txt', 'a',  encoding="UTF-8") as f:
        f.write(str(data_frame))
        f.write(' ')