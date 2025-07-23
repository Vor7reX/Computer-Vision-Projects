# Importa le librerie necessarie
import cv2
import mediapipe as mp

# Inizializza il modulo per il disegno e la soluzione Face Mesh
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

# Prepara le specifiche per il disegno del naso (colore, spessore)
# Usiamo un colore giallo/ciano per distinguerlo
drawing_spec = mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=1, circle_radius=1)

# Inizializza FaceMesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# Inizializza la cattura video dalla fotocamera del PC
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Errore: Impossibile aprire la fotocamera.")
    exit()

print("Avvio della cattura video... Premi 'q' per uscire.")

# Loop principale
while True:
    success, image = cap.read()
    if not success:
        continue

    # Converte l'immagine e la elabora con MediaPipe
    image.flags.writeable = False
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)
    image.flags.writeable = True

    # Disegna solo i landmark del naso
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Disegna il contorno del naso
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_NOSE,
                landmark_drawing_spec=None,
                connection_drawing_spec=drawing_spec)

    # Mostra l'immagine
    flipped_image = cv2.flip(image, 1)
    cv2.imshow('Rilevamento Naso - Premi q per uscire', flipped_image)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Rilascia le risorse
cap.release()
cv2.destroyAllWindows()
face_mesh.close()