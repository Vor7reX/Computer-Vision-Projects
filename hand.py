# Importa le librerie necessarie
import cv2
import mediapipe as mp

# Inizializza MediaPipe Hands
mp_hands = mp.solutions.hands
# 'Hands' è il modulo per il rilevamento della mano.
# - static_image_mode=False: Ottimizzato per video in tempo reale.
# - max_num_hands=2: Rileva al massimo due mani.
# - min_detection_confidence=0.5: Soglia minima di confidenza per considerare il rilevamento riuscito.
# - min_tracking_confidence=0.5: Soglia minima di confidenza per il tracciamento della mano.
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Inizializza il modulo per disegnare i landmark sulla mano
mp_drawing = mp.solutions.drawing_utils

# Inizializza la cattura video dalla fotocamera del PC (l'indice 0 è solitamente la camera di default)
cap = cv2.VideoCapture(0)

# Controlla se la fotocamera è stata aperta correttamente
if not cap.isOpened():
    print("Errore: Impossibile aprire la fotocamera.")
    exit()

print("Avvio della cattura video... Premi 'q' per uscire.")

# Loop principale per leggere i frame dalla fotocamera
while True:
    # Legge un frame dalla fotocamera
    # 'success' è un booleano (True se il frame è stato letto correttamente)
    # 'image' è il frame catturato
    success, image = cap.read()
    if not success:
        print("Ignoro un frame vuoto della fotocamera.")
        # Se si sta leggendo da un file, 'break' potrebbe essere più appropriato
        continue

    # Per migliorare le prestazioni, l'immagine viene passata per riferimento (non modificabile)
    image.flags.writeable = False
    
    # Converte l'immagine da BGR (formato di OpenCV) a RGB (formato richiesto da MediaPipe)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Elabora l'immagine e rileva le mani
    results = hands.process(image_rgb)

    # L'immagine può essere nuovamente resa scrivibile per disegnare i risultati
    image.flags.writeable = True

    # Disegna i landmark della mano sull'immagine
    # 'results.multi_hand_landmarks' contiene i landmark di tutte le mani rilevate
    if results.multi_hand_landmarks:
        # Itera su ogni mano rilevata
        for hand_landmarks in results.multi_hand_landmarks:
            # 'mp_drawing.draw_landmarks' disegna i punti e le connessioni
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS) # Disegna le connessioni tra i punti

    # Specchia l'immagine orizzontalmente per una visualizzazione "a specchio" più intuitiva
    flipped_image = cv2.flip(image, 1)

    # Mostra l'immagine in una finestra chiamata 'Rilevamento Mano'
    cv2.imshow('Rilevamento Mano - Premi q per uscire', flipped_image)

    # Interrompe il loop se viene premuto il tasto 'q'
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Rilascia le risorse
cap.release()
cv2.destroyAllWindows()
hands.close()

print("Script terminato.")