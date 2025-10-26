# 🧠 Face Recognition Attendance System | Python + OpenCV

A real-time face recognition-based attendance system built using Python, OpenCV, and scikit-learn. The system automatically detects, recognizes, and records attendance using a webcam.

---

## 📌 Project Overview

This project uses computer vision and machine learning to automate attendance tracking.  
It detects faces in real-time, identifies registered users, and stores attendance records with timestamps.  
The project includes two key modules — **face registration** and **real-time recognition**.

---

## 🎯 Goals and Objectives

- Automate attendance marking using facial recognition  
- Store and retrieve user faces securely  
- Provide visual and voice-based feedback  
- Maintain daily attendance records in CSV format  

---

## 🧰 Tools and Libraries

- **Python**  
- **OpenCV** – for real-time face detection  
- **scikit-learn (KNN)** – for face recognition  
- **NumPy** – for numerical operations  
- **pywin32** – for optional voice feedback (Windows only)

---

## ⚙️ Workflow

### Step 1: Data Collection (Face Registration)
- Capture face samples using webcam  
- Detect and crop faces using Haar Cascade  
- Resize and flatten faces into feature vectors  
- Save trained data into pickle files (`faces_data.pkl`, `names.pkl`)

### Step 2: Real-Time Recognition
- Load trained data and recognize faces live through webcam  
- Display user names above recognized faces  
- Record attendance with timestamp into CSV file  
- Provide optional voice feedback  

---


Files are automatically stored inside the `Attendance/` folder  
with the format: `Attendance_DD-MM-YYYY.csv`

---

## 🧠 Key Features

- Real-time face recognition using webcam  
- Automatic attendance marking  
- Voice confirmation (optional)  
- Timestamped attendance logs  
- Simple and easy-to-use interface  

---

## 🛠 Technologies Used

- **Language:** Python  
- **Libraries:** OpenCV, scikit-learn, NumPy  
- **Algorithm:** K-Nearest Neighbors (KNN)  
- **Storage:** CSV and Pickle Files  

---

## 🚀 Future Enhancements

- Automate attendance without manual trigger  
- Add deep learning (FaceNet / CNN) for better accuracy  
- Create a web dashboard for data visualization  
- Replace CSV with a database (MySQL / Firebase)  

---

## 🙋‍♂️ Author

**Rits0p**  
Engineering Student | Python Developer | Data Enthusiast  
[GitHub](https://github.com/yourusername) • [LinkedIn](https://linkedin.com/in/yourprofile)

---




