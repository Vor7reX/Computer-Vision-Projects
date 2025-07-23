# OpenCV & MediaPipe - Computer Vision Projects

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)


A collection of interactive Python scripts that leverage **OpenCV** and **MediaPipe** for real-time hand, face, and gesture detection via your webcam.

![Project Demo](assets/Hand_output.png)


---

## 📋 Projects Overview

Inside the `src/` directory, you will find the following scripts:

* `hand.py`: Performs basic hand landmark detection.
* `eyes.py`: Isolates and draws the contours of the eyes and irises.
* `mouth.py`: Isolates and draws the contour of the mouth.
* `nose.py`: Isolates and draws the contour of the nose.
* `finger_counter.py`: Counts raised fingers on one or two hands and displays the total on screen.
* `volume_hand_controller.py`: Controls the Windows system volume by measuring the distance between the thumb and index finger.

---

## 🚀 Tech Stack

* **Python 3.11**
* **OpenCV** - For video capture and image processing.
* **MediaPipe** - For pre-trained Machine Learning models (Hands, Face Mesh).
* **pycaw** - For system audio control on Windows.
* **NumPy** - For numerical calculations and value mapping.

---

## ⚙️ Setup and Usage

Follow these steps to run the scripts on your local machine.

### 1. Prerequisites

Make sure you have the following installed:
* [Python](https://www.python.org/downloads/release/python-3110/) (this project was developed with version 3.11)
* [Git](https://git-scm.com/)

### 2. Clone the Repository

Open your terminal and clone this repository:
```bash
git clone [https://github.com/Vor7reX/Computer-Vision-Projects.git](https://github.com/Vor7reX/Computer-Vision-Projects.git)
cd Computer-Vision-Projects
```

### 3. Create a Virtual Environment

Create a virtual environment to isolate project dependencies:
```bash
# For Windows
py -m venv venv
```

### 4. Activate the Virtual Environment

Activate the newly created environment:
```bash
# For Windows
.\venv\Scripts\activate
```

### 5. Install Dependencies

Install all required libraries in one command using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 6. Run a Script

To run any of the scripts, use the following command (making sure the environment is active):
```bash
python src/your_script_name.py
```
For example, to start the finger counter:
```bash
python src/finger_counter.py
```
Press the **'q'** key to close the script's window.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
