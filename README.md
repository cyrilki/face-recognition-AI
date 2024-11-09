# People Counter System

The People Counter System is an AI-powered application that uses face recognition technology to count and log people. It captures real-time video feed using a webcam and detects and recognizes faces. The system keeps track of unique individuals encountered and maintains an attendance history for reference.

## Features
- Real-time face detection and recognition
- Maintains a log of unique faces counted per day
- User interface built with PyQt5
- Ability to view attendance history with a calendar widget
- Saves and loads known face encodings and attendance history
## How It Works
- **Face Recognition**: The application uses the `face_recognition` library to detect and recognize faces in a video stream.
- **Camera Feed**: Captures live video from a webcam using `cv2.VideoCapture()` from OpenCV.
- **People Counting**: Each recognized face is assigned a unique ID. The system keeps track of the count of unique faces encountered on a given day.
- **Data Persistence**: Uses `pickle` to save and load face encodings and attendance history.
- **User Interface**: Built with PyQt5, providing an intuitive GUI to view the live camera feed, the people counted, and attendance history.
## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/cyrilki/face-recognition-AI.git
   ```
2. **Navigate to the project directory**:
   ```bash
   cd face-recognition-AI
   ```
3. **Install dependencies**:
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```
   The `requirements.txt` file should include all necessary libraries like `opencv-python`, `face-recognition`, `PyQt5`, and `numpy`.

4. **Run the application**:
   ```bash
   python main.py
   ```

### 5. **Usage**
- Launch the application and make sure your webcam is connected.
- The camera feed will start automatically, and the system will detect and recognize faces.
- The people counter will update whenever a new face is detected.
- Click "View History" to see past attendance records using a calendar view.

## Technologies Used
- **Python**: Core programming language
- **OpenCV**: For capturing and processing video
- **face_recognition**: For face detection and recognition
- **PyQt5**: For building the graphical user interface

  ## Future Improvements
- Add the ability to export attendance history to a CSV or PDF file
- Implement a more efficient face recognition model
- Enhance the UI with more customizable options

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## Contact
For questions or support, please reach out to:
- **Name**: Cyril Kiptoo
- **Email**: mellycyril52@gmail.com



