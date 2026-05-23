# Django-Object-Detection-with-Latest-YOLO-Ultralytics-
Real-time Django object detection web application powered by the latest Ultralytics YOLO model, featuring live webcam detection, image upload detection, bounding box predictions, and a beginner-friendly VS Code setup

Real-time object detection web application built with **Django** and the **latest YOLO (Ultralytics)** model. This project supports:

- Live webcam object detection
- Image upload object detection
- Real-time bounding box predictions
- Browser-based detection interface
- Django backend integration
- VS Code friendly project structure

---

# Features

✅ Real-time webcam object detection  
✅ Upload image for object detection  
✅ Uses latest Ultralytics YOLO model  
✅ Django web framework backend  
✅ Clean project structure for easy development  
✅ Ready to run in VS Code  
✅ Beginner-friendly setup  

---

# Project Structure

```bash
django_object_detection/
│
├── detector/
│   ├── migrations/
│   ├── templates/
│   │   └── detector/
│   │       ├── index.html
│   │       ├── result.html
│   │
│   ├── static/
│   │   └── detector/
│   │       ├── css/
│   │       └── js/
│   │
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── yolo_detect.py
│
├── django_object_detection/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── media/
├── requirements.txt
├── manage.py
└── README.md
```

---

# Technologies Used

- Python 3.10+
- Django
- Ultralytics YOLO
- OpenCV
- Pillow
- NumPy
- HTML/CSS/JavaScript
- VS Code

---

# YOLO Version

This project uses the **latest Ultralytics YOLO implementation** instead of the older YOLOv5 repository structure.

Example supported models:

- YOLOv8n
- YOLOv8s
- YOLOv8m
- YOLOv8l
- YOLOv8x

Default model:

```python
yolov8n.pt
```

You can change the model inside:

detector/yolo_detect.py

Example:

```python
model = YOLO("yolov8s.pt")
```

---

# System Requirements

Make sure your system has:

- Windows 10 / Windows 11
- Python installed
- VS Code installed
- Internet connection (first-time model download)

Optional:

- NVIDIA GPU (for faster detection)

---

# Installation Guide (No Command Line Knowledge Required)

## Step 1: Download the Project

Download ZIP from GitHub:

Click:

Code → Download ZIP

Extract the ZIP file.

## Step 2: Open in VS Code

Open VS Code.

Click:

File → Open Folder

Select:

django_object_detection

---

## Step 3: Install Python

If Python is not installed:

Download from:

https://www.python.org/downloads/

During installation, check:

```bash
Add Python to PATH
```

---

## Step 4: Install Required Extensions in VS Code

Install:

- Python
- Pylance
- Code Runner

Go to:

Extensions Icon → Search → Install

---

## Step 5: Create Virtual Environment

Open terminal in VS Code:

Terminal → New Terminal

Run:

python -m venv venv

Activate:

For Windows:

venv\Scripts\activate

---

## Step 6: Install Dependencies

Run:

pip install -r requirements.txt

---

# Required Packages

The requirements include:

Django
ultralytics
opencv-python
numpy
Pillow
torch
torchvision

---

# Database Setup

Run:

python manage.py migrate

---

# Run the Django Server

Start server:

python manage.py runserver

Open browser:

http://127.0.0.1:8000/
---

# Using the Application

## Image Detection

1. Open homepage
2. Click upload image
3. Select image
4. Click detect
5. View detection result

---

## Webcam Detection

1. Open homepage
2. Click webcam detection
3. Allow camera permission
4. Real-time detection starts

---

# Changing YOLO Model

Edit:

detector/yolo_detect.py

Example:

From:

```python
model = YOLO("yolov8n.pt")
```

To:

```python
model = YOLO("yolov8m.pt")
```

Available models:

yolov8n.pt
yolov8s.pt
yolov8m.pt
yolov8l.pt
yolov8x.pt

---

# Common Errors & Fixes

## Error: Python not recognized

Fix:

Reinstall Python and enable:

Add Python to PATH


---

## Error: No module named ultralytics

Fix:

Run:

pip install ultralytics

---

## Error: No module named cv2

Fix:

Run:

pip install opencv-python

---

## Error: Torch installation issue

Fix:

Install manually:

pip install torch torchvision

---

## Error: Webcam not opening

Fix:

- Check browser camera permissions
- Close other apps using webcam
- Restart browser

---

## Error: Slow detection

Fix:

Use smaller model:

```python
yolov8n.pt
```

Or use GPU.

---

# Deployment Notes

For production deployment, consider:

- Gunicorn
- Nginx
- Docker
- AWS / Azure / DigitalOcean

For static files:

python manage.py collectstatic

---

# GitHub Upload Guide

## Create Repository

On GitHub:

Click:

New Repository

Example repository name:

django-yolo-object-detection

---

## Upload Project

Click:

Add File → Upload Files

Drag and drop project files.

Commit:

Initial project upload

---

# .gitignore Recommendation

Create:

.gitignore

Add:

```gitignore
venv/
__pycache__/
*.pyc
db.sqlite3
media/
.idea/
.vscode/
```

---

# Future Improvements

Possible upgrades:

- Video file detection
- Custom trained YOLO model
- Multiple object tracking
- Face detection
- License plate recognition
- PDF report export
- User authentication
- Detection history storage

---

# License

This project is open-source for educational and development purposes.

---

# Author

Developed by:

C. Joshua Ojukwu

GitHub:

https://github.com/CJoshua-Oj

