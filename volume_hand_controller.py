import cv2
import mediapipe as mp
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# --- Inizializzazione Controllo Volume ---
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol_range = volume.GetVolumeRange() # Range del volume, es: (-65.25, 0.0)
min_vol = vol_range[0]
max_vol = vol_range[1]

# --- Inizializzazione MediaPipe ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# --- Inizializzazione OpenCV ---
cap = cv2.VideoCapture(0)
cap.set(3, 1280) # Imposta larghezza
cap.set(4, 720) # Imposta altezza

print("Avvio Controllo Volume... Premi 'q' per uscire.")

while True:
    success, image = cap.read()
    if not success:
        continue

    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Estrai le coordinate di pollice e indice
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            
            h, w, _ = image.shape
            # Converte le coordinate normalizzate in coordinate pixel
            thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
            index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)

            # Disegna cerchi e una linea per feedback visivo
            cv2.circle(image, (thumb_x, thumb_y), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(image, (index_x, index_y), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(image, (thumb_x, thumb_y), (index_x, index_y), (255, 0, 255), 3)

            # Calcola la distanza tra i due punti
            distance = math.hypot(index_x - thumb_x, index_y - thumb_y)

            # Mappa la distanza al range del volume
            # Range distanza mano: da ~50 (vicini) a ~300 (lontani). Da calibrare se necessario.
            vol = np.interp(distance, [50, 300], [min_vol, max_vol])
            vol_bar = np.interp(distance, [50, 300], [400, 150])
            vol_perc = np.interp(distance, [50, 300], [0, 100])
            
            # Imposta il volume di sistema
            volume.SetMasterVolumeLevel(vol, None)

            # Disegna la barra del volume e la percentuale
            cv2.rectangle(image, (50, 150), (85, 400), (0, 255, 0), 3)
            cv2.rectangle(image, (50, int(vol_bar)), (85, 400), (0, 255, 0), cv2.FILLED)
            cv2.putText(image, f'{int(vol_perc)} %', (40, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)

    cv2.imshow("Controllo Volume", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release() 
cv2.destroyAllWindows()