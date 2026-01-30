from flask import Flask, render_template, request
import cv2
import os
import mediapipe as mp

from models.face_embedder import (
    get_embedding,
    load_known_faces,
    cosine_similarity
)
from models.liveness import is_blinking
from utils.attendance import (
    init_attendance,
    mark_attendance
)

app = Flask(__name__)

# Initialize attendance CSV and folders
init_attendance()

# MediaPipe FaceMesh (single face)
mp_face = mp.solutions.face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True
)

# ---------------- HOME ----------------
@app.route("/")
def index():
    return render_template("index.html")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"].strip()

        if not name:
            return render_template(
                "attendance.html",
                message="Invalid name. Please try again."
            )

        save_dir = os.path.join("data", "faces", name)
        os.makedirs(save_dir, exist_ok=True)

        cam = cv2.VideoCapture(0)
        count = 0

        while count < 10:
            ret, frame = cam.read()
            if not ret:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = mp_face.process(rgb)

            if result.multi_face_landmarks:
                cv2.imwrite(os.path.join(save_dir, f"{count}.jpg"), frame)
                count += 1

                cv2.putText(
                    frame,
                    f"Capturing {count}/10",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

            cv2.imshow("Face Registration", frame)

            if cv2.waitKey(1) == 27:
                break

        cam.release()
        cv2.destroyAllWindows()

        return render_template(
            "attendance.html",
            message=f"{name} registered successfully!"
        )

    return render_template("register.html")

# ---------------- ATTENDANCE ----------------
@app.route("/attendance/<punch>")
def attendance(punch):
    known_embeddings, known_names = load_known_faces()
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = mp_face.process(rgb)

        if result.multi_face_landmarks:
            embedding = get_embedding(frame)

            # 🔒 SAFETY: embedding can be None
            if embedding is None:
                cv2.putText(
                    frame,
                    "Face not clear. Please look at the camera",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2
                )
                cv2.imshow("Attendance", frame)
                cv2.waitKey(1)
                continue

            matched_name = None
            for known_emb, name in zip(known_embeddings, known_names):
                similarity = cosine_similarity(embedding, known_emb)
                if similarity > 0.90:
                    matched_name = name
                    break

            # ❌ NOT REGISTERED
            if matched_name is None:
                cam.release()
                cv2.destroyAllWindows()
                return render_template(
                    "attendance.html",
                    message="Face not registered. Please register first."
                )

            # 👁️ LIVENESS CHECK
            if not is_blinking(result.multi_face_landmarks[0].landmark):
                cv2.putText(
                    frame,
                    "Please blink to verify liveness",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2
                )
                cv2.imshow("Attendance", frame)
                cv2.waitKey(1)
                continue

            # 🕒 BUSINESS RULE CHECK
            status = mark_attendance(matched_name, punch)

            cam.release()
            cv2.destroyAllWindows()

            if status == "NOT_PUNCHED_IN":
                return render_template(
                    "attendance.html",
                    message="You have not punched in today."
                )

            return render_template(
                "attendance.html",
                message=f"{matched_name} {punch.upper()} marked successfully!"
            )

        cv2.imshow("Attendance", frame)

        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

    return render_template(
        "attendance.html",
        message="Attendance failed. Please try again."
    )

# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(debug=True)
