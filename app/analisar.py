import numpy
import cv2

from parametros import VERBOSO, DEBUG, SINALIZAR

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

        frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        if frame_number % 10 == 0:
            frame = aplicar_threshold(frame)

            for numero_larva, larva in enumerate(cordenadas_larvas, start=0):
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
            numero_frame = numero_frame + 1

            if len(frame.shape) == 3:
                h, w, _ = frame.shape
            elif len(frame.shape) == 2:
                h, w = frame.shape

            if DEBUG:
                cv2.namedWindow('Movimento', cv2.WINDOW_NORMAL)
                cv2.imshow('Movimento', frame)
                cv2.resizeWindow('Movimento', int(h//3), int(w//3))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
    cap.release()

    cv2.destroyAllWindows()
    return data_frame


def acompanhar_larvas_mortas(caminho_video, cordenadas_larvas, nomevideo):
    if VERBOSO:
        print("Recortando área selecionada do video.")
    cap = cv2.VideoCapture(caminho_video)

    if SINALIZAR:
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        largura = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        altura = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        fourcc = cv2.VideoWriter_fourcc(*'avc1')  
        caminho_saida = 'sinalizadas\\' + nomevideo + 'mp4'
        print("Sinalizadas salvo em: " + str(caminho_saida))
        out = cv2.VideoWriter(caminho_saida, fourcc, fps, (largura, altura), isColor=False)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        if frame_number % 4 == 0:
            for numero_larva, larva in enumerate(cordenadas_larvas, start=0):
                centro = larva["center"]
                raio = larva["radius"]
                largura = raio*2
                x = centro[0] - raio
                y = centro[1] - raio        
                frame = cv2.rectangle(frame, (x, y), (x+largura, y+largura), (255, 0, 0), 2) 
                frame = cv2.putText(frame, ('Larva ' + str(numero_larva)), (x, y + largura + 10), cv2.FONT_HERSHEY_SIMPLEX , 1, (255, 0, 0), 2, cv2.LINE_AA) 


            if len(frame.shape) == 3:
                h, w, _ = frame.shape
            elif len(frame.shape) == 2:
                h, w = frame.shape

            if DEBUG:
                cv2.namedWindow('Mortas', cv2.WINDOW_NORMAL)
                cv2.imshow('Mortas', frame)
                cv2.resizeWindow('Mortas', int(h//3), int(w//3))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            if SINALIZAR:
                out.write(frame)
    cap.release()
    if SINALIZAR:
        out.release()

    cv2.destroyAllWindows()

def aplicar_threshold(frame):
    if VERBOSO:
        print("Aplicanto threshold.")
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresholded_frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
    return thresholded_frame