import base64
from io import BytesIO
from flask import Flask, request, jsonify, render_template
from PIL import Image
import numpy as np
import cv2 as cv
import mediapipe as mp

app = Flask(__name__)

# Configuração do MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_frame', methods=['POST'])
def process_frame_route():
    data = request.json
    image_data = data.get('image')

    if not image_data:
        return jsonify({'error': 'Nenhuma imagem recebida'}), 400

    try:
        # Verifica o formato da imagem
        if not image_data.startswith('data:image/png;base64,'):
            raise ValueError("Formato de imagem inválido")

        # Remove o prefixo e decodifica a imagem base64
        image_data = image_data.replace('data:image/png;base64,', '')
        image_bytes = base64.b64decode(image_data)

        # Abre a imagem usando PIL
        image = Image.open(BytesIO(image_bytes))
        image_np = np.array(image)

        # Converte para o formato OpenCV BGR
        image_bgr = cv.cvtColor(image_np, cv.COLOR_RGB2BGR)

        # Processa a imagem com MediaPipe
        results = pose.process(cv.cvtColor(image_bgr, cv.COLOR_BGR2RGB))
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            for id, landmark in enumerate(landmarks):
                if id in [12, 14, 16]:  # Por exemplo, ombros e cotovelos
                    h, w, _ = image_bgr.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    cv.circle(image_bgr, (cx, cy), 5, (0, 255, 0), cv.FILLED)

            # Desenha linhas entre os pontos
            if len(landmarks) > 2:
                ponto12 = landmarks[12]
                ponto14 = landmarks[14]
                ponto16 = landmarks[16]
                cv.line(image_bgr, (int(ponto12.x * w), int(ponto12.y * h)),
                        (int(ponto14.x * w), int(ponto14.y * h)), (255, 0, 0), 2)
                cv.line(image_bgr, (int(ponto14.x * w), int(ponto14.y * h)),
                        (int(ponto16.x * w), int(ponto16.y * h)), (255, 0, 0), 2)

        # Codifica a imagem processada em base64 para retornar ao cliente
        _, buffer = cv.imencode('.png', image_bgr)
        processed_image = base64.b64encode(buffer).decode('utf-8')

        return jsonify({'image': processed_image})
    except Exception as e:
        print(f"Erro no processamento da imagem: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
