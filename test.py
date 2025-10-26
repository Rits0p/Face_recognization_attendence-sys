from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
from datetime import datetime
import time

# For Windows TTS
try:
    from win32com.client import Dispatch
    def speak(str1):
        """Uses Windows SAPI to speak the given string."""
        Dispatch("SAPI.SpVoice").Speak(str1)
    SPEAK_AVAILABLE = True
except ImportError:
    print("Warning: win32com not found. Voice feedback is disabled.")
    def speak(str1): pass
    SPEAK_AVAILABLE = False


# --- Configuration ---
DATA_DIR = 'data/'
ATTENDANCE_DIR = 'Attendance/'
HAARCASCADE_PATH = 'haarcascade_frontalface_default.xml'
BACKGROUND_IMG_PATH = 'background.png'
COL_NAMES = ['NAME', 'TIME']

# --- Initialization and Model Loading ---
if not (os.path.exists(os.path.join(DATA_DIR, 'names.pkl')) and 
        os.path.exists(os.path.join(DATA_DIR, 'faces_data.pkl'))):
    print("Error: Face data files (names.pkl or faces_data.pkl) not found in 'data/' directory.")
    print("Please run 'add_faces.py' first.")
    exit()

if not os.path.exists(HAARCASCADE_PATH):
    print(f"Error: Cascade file not found at {HAARCASCADE_PATH}")
    exit()

if not os.path.exists(BACKGROUND_IMG_PATH):
    print(f"Error: Background image not found at {BACKGROUND_IMG_PATH}")
    exit()


with open(os.path.join(DATA_DIR, 'names.pkl'), 'rb') as w:
    LABELS = pickle.load(w)
with open(os.path.join(DATA_DIR, 'faces_data.pkl'), 'rb') as f:
    FACES = pickle.load(f)

print(f'Shape of Faces matrix --> {FACES.shape}')
print(f'Number of unique people: {len(set(LABELS))}')

# Train the KNN model
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)
print("KNN Model trained successfully.")

imgBackground = cv2.imread(BACKGROUND_IMG_PATH)
video = cv2.VideoCapture(0)

# --- Attendance Recording Function ---
def record_attendance(name):
    """Saves the attendance record to a daily CSV file."""
    ts = time.time()
    date_str = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
    timestamp_str = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
    
    attendance_path = os.path.join(ATTENDANCE_DIR, f"Attendance_{date_str}.csv")
    attendance_record = [name, timestamp_str]

    file_exists = os.path.isfile(attendance_path)
    
    try:
        # Use 'a' for append mode.
        with open(attendance_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write column headers only if the file is new
            if not file_exists:
                writer.writerow(COL_NAMES)
            
            # Write the attendance record
            writer.writerow(attendance_record)
        
        print(f"Attendance recorded for {name} at {timestamp_str}")
        if SPEAK_AVAILABLE:
            speak(f"Attendance recorded for {name}")

    except Exception as e:
        print(f"Error recording attendance: {e}")

# --- Main Recognition Loop ---
facedetect = cv2.CascadeClassifier(HAARCASCADE_PATH)
last_recorded_name = None # Prevents immediate re-recording
recording_delay = 5 # seconds to wait before recording for the same person again

while True:
    ret, frame = video.read()
    if not ret:
        break
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    recognized_name = "Unknown"
    
    for (x, y, w, h) in faces:
        # Preprocessing for prediction
        crop_img = frame[y:y + h, x:x + w]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        
        # Prediction
        output = knn.predict(resized_img)
        recognized_name = str(output[0])
        
        # Draw UI
        color = (0, 255, 0) if recognized_name != "Unknown" else (0, 0, 255)
        
        # Name background
        cv2.rectangle(frame, (x, y - 40), (x + w, y), color, -1)
        # Bounding box
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        # Name text
        cv2.putText(frame, recognized_name, (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
        
        # Only record attendance for the first detected face if it's a known person
        break 

    # Overlay video on background image
    try:
        # Assuming frame size matches the section of the background image
        # Note: This slicing might need adjustment based on your 'background.png' resolution
        imgBackground[162:162 + 480, 55:55 + 640] = frame 
    except ValueError:
        print("Warning: Frame size mismatch with background image slice. Displaying frame directly.")
        imgBackground = frame

    cv2.imshow("Attendance System", imgBackground)
    
    k = cv2.waitKey(1)
    
    if k == ord('o'): # Manual trigger for attendance
        if recognized_name != "Unknown":
            # Check for delay to prevent spamming the record button
            current_time = time.time()
            if last_recorded_name != recognized_name or (current_time - last_record_time) > recording_delay:
                record_attendance(recognized_name)
                last_recorded_name = recognized_name
                last_record_time = current_time
            else:
                print(f"Attendance for {recognized_name} recently recorded. Please wait {recording_delay} seconds.")
                if SPEAK_AVAILABLE:
                    speak("Please wait a moment before recording again.")
        else:
            print("Cannot record attendance: Face is Unknown.")
            if SPEAK_AVAILABLE:
                speak("Face not recognized.")

    if k == ord('q'):
        break

# --- Final Cleanup ---
video.release()
cv2.destroyAllWindows()