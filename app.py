from flask import Flask, render_template, Response
import cv2
from deepface import DeepFace
import webbrowser

app = Flask(__name__)

def extract_gender_and_age(frame, face_cascade):
    try:
        # Convert the frame to RGB (required by DeepFace)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Use Haar Cascade to detect faces
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            # Extract face region
            face_roi = frame[y:y+h, x:x+w]

            # Use DeepFace to analyze gender and age
            result = DeepFace.analyze(face_roi, actions=['gender', 'age'])

            gender_stats = result[0]['gender']
            age = int(result[0]['age'])
            print("Predicted Gender:", gender_stats)
            print("Predicted Age:", age)

            # Select the dominant gender label
            gender = max(gender_stats, key=gender_stats.get)

            # Display gender and age information on the frame
            cv2.putText(frame, f"Gender: {gender} - {gender_stats[gender]:.2f}%", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, f"Age: {age} years", (x, y + h + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            # Draw rectangle around the face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        return frame

    except Exception as e:
        print(f"Error: {e}")
        return frame

def generate_frames():
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = extract_gender_and_age(frame, face_cascade)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=True, use_reloader=False)
