import cv2
import numpy as np 
def mapear(imagem, contornos):
    for contorno in contornos:
        (x, y), radius = cv2.minEnclosingCircle(contorno)
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(imagem, center, radius, (0, 0, 255), 2)

        cv2.namedWindow('Circuladas', cv2.WINDOW_NORMAL)
        cv2.imshow('Circuladas', imagem)
        cv2.resizeWindow('Circuladas', 1440//2, 1440//2)

def erosion(image):
    kernel = np.ones((0, 0), np.uint8) 
    image = cv2.erode(image, kernel, iterations=1) 
    return image

def numero_de_larvas_frame(image):
    arestas = cv2.Canny(image, 50,200)
    contornos, _ = cv2.findContours(arestas.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    numero_de_larvas = len(contornos)
    cv2.putText(image, str(numero_de_larvas), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    
    cv2.namedWindow('Contagem', cv2.WINDOW_NORMAL)
    cv2.imshow('Contagem', image)
    cv2.resizeWindow('Contagem', 1440//2, 1440//2)
    return numero_de_larvas, contornos

def aplicar_threshold(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresholded_frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
    return thresholded_frame

def crop_video(caminho_video, x, y, width, height):
    cap = cv2.VideoCapture(caminho_video)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    i = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cropped_frame = frame

        cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
        cv2.imshow('Original', cropped_frame)
        cv2.resizeWindow('Original', 1440//2, 1440//2)

        image = aplicar_threshold(cropped_frame)
        image = erosion(image)

        numero_de_larvas, contornos = numero_de_larvas_frame(image)
        mapear(frame, contornos)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        i = i + 1 

    cap.release()
    cv2.destroyAllWindows()

caminho_video = 'videoalta.mov'

crop_x = 0
crop_y = 330
crop_largura = 450
crop_altura = 680
crop_video(caminho_video, crop_x, crop_y, crop_largura, crop_altura)
