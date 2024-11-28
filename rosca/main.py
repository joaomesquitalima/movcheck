import mediapipe as mp
import cv2 as cv
import numpy as np
import math
import threading

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

webcam = cv.VideoCapture(0)
# ip = "https://192.168.233.241:8080/video"

# webcam.open(ip)
azul = (255,0,0)
vermelho = (0,0,255)
cor = azul
b = 1
while True:
    _, image = webcam.read()

    image_rgb = cv.cvtColor(image,cv.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

        # Verifica se algum ponto foi detectado
    if results.pose_landmarks:
        for id, landmark in enumerate(results.pose_landmarks.landmark):
            landmarks = results.pose_landmarks.landmark
            # Obtém a posição dos pontos
            if id == 12 or id  == 14 or id == 16:
                h, w, _ = image.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                # print(f'ID: {id}, X: {cx}, Y: {cy}, Z: {landmark.z}')

                # Desenha os pontos na imagem
                cv.circle(image, (cx, cy), 5, (0, 255, 0), cv.FILLED)
                ponto12 = landmarks[12]
                ponto14 = landmarks[14]
                ponto16 = landmarks[16]
                dx = ponto16.x - ponto12.x
                dy = ponto12.y - ponto16.y
                p_x = math.sqrt(dx**2 + dy**2)
                x_12 = ponto12.x*w
                x_14 = ponto14.x*w
                distancia1 = x_14 - x_12
                # print(p_x)
                print(distancia1)
                if abs(distancia1) > 50 and b == 1:
                    cor = vermelho
                    # play_sound('teste.mp3')
                    # threading.Thread(target=play_sound, args=('teste.mp3',)).start()
                    # print('t')
                    # b+=1
                else:
                    cor = azul
                cv.line(image, (int(ponto12.x*w),int(ponto12.y*h)), (int(ponto14.x*w),int(ponto14.y*h)), cor,thickness=5)
                cv.line(image, (int(ponto14.x*w),int(ponto14.y*h)), (int(ponto16.x*w),int(ponto16.y*h)),cor,thickness=5)


        # Desenha os pontos e conexões na imagem
                # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)



    cv.imshow("tela",image)

    tecla = cv.waitKey(1)

    if tecla == ord("b"):
        break