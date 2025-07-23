# Importa le librerie necessarie
import cv2
import mediapipe as mp

# Inizializza il modulo per il disegno e la soluzione Face Mesh
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

# Prepara le specifiche per il disegno delle labbra (colore, spessore)
# Usiamo un colore rosso per distinguerlo dagli script precedenti
drawing_spec = mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1)

# Inizializza FaceMesh.
# - refine_landmarks=True: Attiva il rilevamento specifico di iridi e labbra.
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# Inizializza la cattura video dalla fotocamera del PC
cap = cv2.VideoCapture(0)

# Controlla se la fotocamera è stata aperta correttamente
if not cap.isOpened():
    print("Errore: Impossibile aprire la fotocamera.")
    exit()

print("Avvio della cattura video... Premi 'q' per uscire.")

# Loop principale per leggere i frame dalla fotocamera
while True:
    success, image = cap.read()
    if not success:
        print("Ignoro un frame vuoto della fotocamera.")
        continue

    # Converte l'immagine da BGR a RGB e la passa per riferimento
    image.flags.writeable = False
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Elabora l'immagine e rileva il face mesh
    results = face_mesh.process(image_rgb)

    # Rende di nuovo l'immagine scrivibile
    image.flags.writeable = True

    # Disegna solo i landmark delle labbra sull'immagine
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Disegna il contorno delle labbra
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_LIPS,
                landmark_drawing_spec=None, # Non disegna i punti, solo le connessioni
                connection_drawing_spec=drawing_spec)

    # Specchia l'immagine per una visualizzazione "a specchio"
    flipped_image = cv2.flip(image, 1)

    # Mostra l'immagine in una finestra
    cv2.imshow('Rilevamento Bocca - Premi q per uscire', flipped_image)

    # Interrompe il loop se viene premuto il tasto 'q'
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Rilascia le risorse
cap.release()
cv2.destroyAllWindows()
face_mesh.close()

print("Script terminato.")