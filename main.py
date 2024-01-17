import cv2
import time
import numpy as np 

def circulos_internos(circulos):
    circulos = sorted(circulos, key=lambda x: x['radius'], reverse=True) 

    indices_para_remover = set()

    for i in range(len(circulos)):
        for j in range(i + 1, len(circulos)):
            distancia_entre_centros = ((circulos[i]['center'][0] - circulos[j]['center'][0]) ** 2 +
                                       (circulos[i]['center'][1] - circulos[j]['center'][1]) ** 2) ** 0.5

            if distancia_entre_centros + circulos[j]['radius'] <= circulos[i]['radius']:
                indices_para_remover.add(j)
            elif distancia_entre_centros < circulos[i]['radius'] + circulos[j]['radius']:
                indices_para_remover.add(j)

    circulos_filtrados = [circulos[i] for i in range(len(circulos)) if i not in indices_para_remover]

    radii = [circulos_filtrados['radius'] for circulos_filtrados in circulos_filtrados]
    media_radius = sum(radii) / len(radii)

    circulos_filtrados = [circle for circle in circulos_filtrados if abs(circle['radius'] - media_radius) <= 0.9 * media_radius]
                  
    return circulos_filtrados

def mapear(imagem, contornos):
    dadosCirculo = []
    for contorno in contornos:
        (x, y), radius = cv2.minEnclosingCircle(contorno)
        center = (int(x), int(y))
        radius = int(radius)
        data = { "center" : center,
                  "radius" :  radius}
        dadosCirculo.append(data)

    circulos_filtrados =  circulos_internos(dadosCirculo)

    i = 1
    for circulo in circulos_filtrados:
        cv2.circle(imagem, circulo['center'], circulo['radius'], (0, 0, 255), 2)
        cv2.putText(imagem, str(i), circulo['center'], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv2.namedWindow('Circuladas', cv2.WINDOW_NORMAL)
        cv2.imshow('Circuladas', imagem)
        cv2.resizeWindow('Circuladas', 1440//2, 1440//2)
        i = i + 1
    return imagem

def erosion(image):
    kernel = np.ones((5, 5), np.uint8) 
    image = cv2.dilate(image, kernel, iterations=1) 
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
        imagem = mapear(frame, contornos)
        cv2.imwrite(('img_contagem\\' + str(i) + '.png'), imagem)

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
