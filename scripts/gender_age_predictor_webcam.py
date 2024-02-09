import cv2
from deepface import DeepFace
import numpy as np
import json

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

if __name__ == "__main__":
    # Open the webcam
    cap = cv2.VideoCapture(0)

    # Load Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        # Capture video from webcam
        ret, frame = cap.read()

        # Check if frame is valid
        if not ret:
            print("Error: Couldn't capture frame from the webcam.")
            break

        # Apply face detection and gender/age analysis to the frame
        frame = extract_gender_and_age(frame, face_cascade)

        # Display the processed frame
        cv2.imshow('Webcam Feed with Gender and Age Analysis', frame)

        # Break the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all windows
    cap.release()
    cv2.destroyAllWindows()