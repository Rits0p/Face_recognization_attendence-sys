import cv2
import pickle
import numpy as np
import os

# --- Configuration ---
FACE_SAMPLES_COUNT = 100
RESIZE_DIM = (50, 50)
SKIP_FRAMES = 10
DATA_DIR = 'data/'
HAARCASCADE_PATH = 'haarcascade_frontalface_default.xml'

# --- Initialization ---
video = cv2.VideoCapture(0)
# Ensure the cascade file exists
if not os.path.exists(HAARCASCADE_PATH):
    print(f"Error: Cascade file not found at {HAARCASCADE_PATH}")
    exit()
facedetect = cv2.CascadeClassifier(HAARCASCADE_PATH)

face_data_samples = []
frame_counter = 0

# Get user input and sanitize
while True:
    name = input("Enter Your Name (Alphanumeric only): ").strip()
    if name.isalnum():
        break
    print("Invalid name. Please use only letters and numbers.")

print(f"Collecting 100 face samples for {name}...")

# --- Main Collection Loop ---
while True:
    ret, frame = video.read()
    if not ret:
        print("Failed to grab frame.")
        break
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect faces
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
        
        # Only collect a sample on specific frames
        if frame_counter % SKIP_FRAMES == 0:
            if len(face_data_samples) < FACE_SAMPLES_COUNT:
                # Crop, resize, and store the image
                crop_img = frame[y:y + h, x:x + w]
                resized_img = cv2.resize(crop_img, RESIZE_DIM)
                face_data_samples.append(resized_img)
        
        # Display feedback
        count_text = f"Samples: {len(face_data_samples)}/{FACE_SAMPLES_COUNT}"
        cv2.putText(frame, count_text, (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 0.7, (50, 50, 255), 2)

    frame_counter += 1
    cv2.imshow("Add Faces - Press 'q' to stop", frame)
    
    k = cv2.waitKey(1)
    if k == ord('q') or len(face_data_samples) >= FACE_SAMPLES_COUNT:
        break

# --- Cleanup ---
video.release()
cv2.destroyAllWindows()

if len(face_data_samples) < FACE_SAMPLES_COUNT:
    print(f"Only collected {len(face_data_samples)} samples. Exiting without saving.")
    exit()

# --- Data Processing and Saving ---

# Convert to NumPy array and reshape: (100, 50*50*3) = (100, 7500)
faces_data_array = np.asarray(face_data_samples)
faces_data_array = faces_data_array.reshape(FACE_SAMPLES_COUNT, -1)
print(f"Reshaped face data to: {faces_data_array.shape}")

# 1. Update Names (Labels)
names_path = os.path.join(DATA_DIR, 'names.pkl')
new_names = [name] * FACE_SAMPLES_COUNT

if not os.path.exists(names_path):
    all_names = new_names
    print("Created new names data file.")
else:
    with open(names_path, 'rb') as f:
        all_names = pickle.load(f)
    all_names.extend(new_names)
    print(f"Appended {FACE_SAMPLES_COUNT} names to existing data.")

with open(names_path, 'wb') as f:
    pickle.dump(all_names, f)

# 2. Update Faces Data (Features)
faces_path = os.path.join(DATA_DIR, 'faces_data.pkl')

if not os.path.exists(faces_path):
    final_faces = faces_data_array
    print("Created new faces data file.")
else:
    with open(faces_path, 'rb') as f:
        existing_faces = pickle.load(f)
    # Append the new faces data vertically (axis=0)
    final_faces = np.append(existing_faces, faces_data_array, axis=0)
    print(f"Appended face data. New total shape: {final_faces.shape}")

with open(faces_path, 'wb') as f:
    pickle.dump(final_faces, f)

print("Face data collection complete and saved successfully.")