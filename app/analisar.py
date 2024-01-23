import numpy
import cv2

from parametros import VERBOSO, DEBUG

def acompanhar_larvas(caminho_video, cordenadas_larvas, quantidade_frames):
    if VERBOSO:
        print("Recortando área selecionada do video.")
    cap = cv2.VideoCapture(caminho_video)

    data_frame = [[None] * (quantidade_frames) for _ in range(len(cordenadas_larvas))]

    numero_frame = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = aplicar_threshold(frame)

        for numero_larva, larva in enumerate(cordenadas_larvas, start=0):
            print(larva)
            centro = larva["center"]
            raio = larva["radius"]
            largura = raio*2
            x = centro[0] - raio
            y = centro[1] - raio        
            roi = frame[y:y+largura, x:x+largura]
            presenca = numpy.sum(roi == 0)
            data_frame[numero_larva][numero_frame] = presenca
            frame = cv2.rectangle(frame, (x, y), (x+largura, y+largura), (255, 0, 255), 1) 
            frame = cv2.putText(frame, ('Presença: ' + str(presenca)), (x, y + largura + 10), cv2.FONT_HERSHEY_SIMPLEX , 0.3, (255, 0, 255), 1, cv2.LINE_AA) 


        if len(frame.shape) == 3:
            h, w, _ = frame.shape
        elif len(frame.shape) == 2:
            h, w = frame.shape

        if DEBUG:
            cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
            cv2.imshow('frame', frame)
            cv2.resizeWindow('frame', int(h//1.5), int(w//1.5))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        numero_frame += 1
    cap.release()
    cv2.destroyAllWindows()
    return data_frame


def acompanhar_larvas_mortas(caminho_video, cordenadas_larvas, quantidade_frames):
    if VERBOSO:
        print("Recortando área selecionada do video.")
    cap = cv2.VideoCapture(caminho_video)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        for numero_larva, larva in enumerate(cordenadas_larvas, start=0):
            centro = larva["center"]
            raio = larva["radius"]
            largura = raio*2
            x = centro[0] - raio
            y = centro[1] - raio        
            frame = cv2.rectangle(frame, (x, y), (x+largura, y+largura), (255, 0, 255), 1) 
            frame = cv2.putText(frame, ('Larva ' + str(numero_larva)), (x, y + largura + 10), cv2.FONT_HERSHEY_SIMPLEX , 0.3, (255, 0, 255), 1, cv2.LINE_AA) 


        if len(frame.shape) == 3:
            h, w, _ = frame.shape
        elif len(frame.shape) == 2:
            h, w = frame.shape

        if DEBUG:
            cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
            cv2.imshow('frame', frame)
            cv2.resizeWindow('frame', int(h//1.5), int(w//1.5))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
    cap.release()
    cv2.destroyAllWindows()

def aplicar_threshold(frame):
    if VERBOSO:
        print("Aplicanto threshold.")
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresholded_frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
    return thresholded_frame