import cv2
import numpy as np
import mediapipe as mp
import os

mp_face_mesh = mp.solutions.face_mesh

def get_embedding(image):
    """
    Extracts face mesh landmarks and converts them into a numeric embedding.
    Returns None if face is not detected clearly.
    """
    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True
    ) as face_mesh:

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb)

        if not result.multi_face_landmarks:
            return None

        landmarks = result.multi_face_landmarks[0].landmark
        embedding = np.array(
            [[lm.x, lm.y, lm.z] for lm in landmarks]
        ).flatten()

        return embedding


def load_known_faces():
    """
    Loads stored face embeddings from data/faces directory
    """
    embeddings = []
    names = []

    base_path = os.path.join("data", "faces")

    if not os.path.exists(base_path):
        return embeddings, names

    for person in os.listdir(base_path):
        person_dir = os.path.join(base_path, person)
        if not os.path.isdir(person_dir):
            continue

        for img in os.listdir(person_dir):
            img_path = os.path.join(person_dir, img)
            image = cv2.imread(img_path)

            if image is None:
                continue

            emb = get_embedding(image)
            if emb is not None:
                embeddings.append(emb)
                names.append(person)

    return embeddings, names


def cosine_similarity(a, b):
    """
    SAFE cosine similarity
    Returns -1 if any embedding is invalid
    """
    if a is None or b is None:
        return -1

    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return -1

    return np.dot(a, b) / denom
