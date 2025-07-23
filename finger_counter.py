# Importa le librerie necessarie
import cv2
import mediapipe as mp

# Inizializza MediaPipe Hands e il modulo per disegnare
mp_hands = mp.solutions.hands
# Aggiunto max_num_hands=2 per essere sicuri di rilevarle entrambe
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Inizializza la cattura video
cap = cv2.VideoCapture(0)

# Indici dei landmark per le punte delle dita
tip_ids = [4, 8, 12, 16, 20]

print("Avvio Contatore Dita... Premi 'q' per uscire.")

while True:
    success, image = cap.read()
    if not success:
        continue

    # Specchia l'immagine per una visualizzazione corretta e converti i colori
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Elabora l'immagine per trovare le mani
    results = hands.process(image_rgb)
    
    # NUOVO: Variabile per il conteggio totale, inizializzata a 0 ad ogni frame
    total_fingers_across_hands = 0

    if results.multi_hand_landmarks:
        # Itera su ogni mano rilevata
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Disegna i landmark sulla mano
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Lista per memorizzare quali dita sono alzate per la mano corrente
            fingers = []
            
            # NUOVO: Rileva se la mano è destra o sinistra per una logica del pollice corretta
            handedness_info = results.multi_handedness[idx]
            hand_label = handedness_info.classification[0].label

            # --- Logica per il Pollice (ora robusta per entrambe le mani) ---
            if hand_label == "Right":
                # Se la punta del pollice (x) è a sinistra del suo punto più basso, è alzato
                if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:  # Left Hand
                # Se la punta del pollice (x) è a destra del suo punto più basso, è alzato
                if hand_landmarks.landmark[tip_ids[0]].x > hand_landmarks.landmark[tip_ids[0] - 1].x:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # --- Logica per le altre 4 dita (invariata) ---
            for id in range(1, 5):
                if hand_landmarks.landmark[tip_ids[id]].y < hand_landmarks.landmark[tip_ids[id] - 2].y:
                    fingers.append(1)
                else:
                    fingers.append(0)
            
            # NUOVO: Aggiunge il conteggio di questa mano al totale
            total_fingers_across_hands += fingers.count(1)

    # NUOVO: Mostra il conteggio totale UNA SOLA VOLTA, fuori dal loop delle mani
    cv2.putText(image, str(total_fingers_across_hands), (30, 90), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0), 5)

    # Mostra l'immagine
    cv2.imshow("Contatore Dita Totale", image)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()