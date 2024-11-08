import cv2
import face_recognition
import numpy as np
import pickle
from datetime import datetime, date
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QPushButton, QCalendarWidget, QDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
import sys
import os

class PeopleCounterSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.known_face_encodings = []
        self.known_face_dates = []
        self.people_counted = set()
        self.attendance_history = {}
        self.load_data()
        self.init_ui()
        self.start_camera()

    def init_ui(self):
        self.setWindowTitle('People Counter System')
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
            }
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
        """)

        layout = QVBoxLayout()

        # Add history controls above the main layout
        history_controls = QHBoxLayout()
        
        self.view_history_btn = QPushButton("View History")
        self.view_history_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.view_history_btn.clicked.connect(self.show_history_dialog)
        history_controls.addWidget(self.view_history_btn)
        
        layout.insertLayout(1, history_controls)

        # Counter display at the top
        self.counter_label = QLabel('People Counted Today: 0')
        self.counter_label.setAlignment(Qt.AlignCenter)
        self.counter_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #4a4a4a;
            background-color: #e0e0e0;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 10px;
        """)
        layout.addWidget(self.counter_label)

        main_layout = QHBoxLayout()

        # Left side - camera feed
        left_layout = QVBoxLayout()
        self.camera_label = QLabel()
        self.camera_label.setFixedSize(640, 480)  # Set fixed size for camera feed
        self.camera_label.setStyleSheet("border: 2px solid #4CAF50; border-radius: 8px;")
        self.camera_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.camera_label)

        main_layout.addLayout(left_layout)

        # Right side - counter log
        right_layout = QVBoxLayout()
        log_label = QLabel("Counter Log")
        log_label.setAlignment(Qt.AlignCenter)
        log_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #4a4a4a; margin-bottom: 10px;")
        right_layout.addWidget(log_label)
        self.log_table = QTableWidget()
        self.log_table.setColumnCount(2)
        self.log_table.setHorizontalHeaderLabels(['Face ID', 'Time'])
        self.log_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        right_layout.addWidget(self.log_table)

        main_layout.addLayout(right_layout)

        layout.addLayout(main_layout)

        self.setLayout(layout)

        # Initialize camera
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def start_camera(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                face_id = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    face_id = f"Face_{first_match_index + 1}"
                    if self.known_face_dates[first_match_index] != date.today():
                        self.known_face_dates[first_match_index] = date.today()
                        self.log_face(face_id)
                        self.people_counted.add(face_id)
                        self.update_counter()
                else:
                    face_id = f"Face_{len(self.known_face_encodings) + 1}"
                    self.known_face_encodings.append(face_encoding)
                    self.known_face_dates.append(date.today())
                    self.log_face(face_id)
                    self.people_counted.add(face_id)
                    self.update_counter()

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, face_id, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(q_image)
            self.camera_label.setPixmap(pixmap.scaled(self.camera_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def log_face(self, face_id):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_date = date.today().strftime("%Y-%m-%d")
        
        # Store in attendance history
        if current_date not in self.attendance_history:
            self.attendance_history[current_date] = []
        self.attendance_history[current_date].append({
            'face_id': face_id,
            'time': current_time
        })
        
        # Update current log table
        row_count = self.log_table.rowCount()
        self.log_table.insertRow(row_count)
        self.log_table.setItem(row_count, 0, QTableWidgetItem(face_id))
        self.log_table.setItem(row_count, 1, QTableWidgetItem(current_time))
        self.log_table.scrollToBottom()

    def update_counter(self):
        count = len(self.people_counted)
        self.counter_label.setText(f'People Counted Today: {count}')

    def load_data(self):
        try:
            with open('face_data.pkl', 'rb') as f:
                data = pickle.load(f)
                self.known_face_encodings = data['encodings']
                self.known_face_dates = data['dates']
                self.attendance_history = data.get('attendance_history', {})
                if self.known_face_dates and self.known_face_dates[-1] != date.today():
                    self.people_counted.clear()
        except FileNotFoundError:
            print("No previous data found. Starting fresh.")

    def save_data(self):
        data = {
            'encodings': self.known_face_encodings,
            'dates': self.known_face_dates,
            'attendance_history': self.attendance_history
        }
        with open('face_data.pkl', 'wb') as f:
            pickle.dump(data, f)

    def closeEvent(self, event):
        if self.cap is not None:
            self.cap.release()
        self.save_data()
        event.accept()

    def show_history_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Attendance History")
        dialog.setMinimumSize(600, 400)
        
        layout = QVBoxLayout()
        
        # Add calendar for date selection
        calendar = QCalendarWidget()
        calendar.setGridVisible(True)
        layout.addWidget(calendar)
        
        # Add table for showing historical data
        history_table = QTableWidget()
        history_table.setColumnCount(2)
        history_table.setHorizontalHeaderLabels(['Face ID', 'Time'])
        history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(history_table)
        
        def update_history_table(selected_date):
            history_table.setRowCount(0)
            date_str = selected_date.toString("yyyy-MM-dd")
            if date_str in self.attendance_history:
                for entry in self.attendance_history[date_str]:
                    row = history_table.rowCount()
                    history_table.insertRow(row)
                    history_table.setItem(row, 0, QTableWidgetItem(entry['face_id']))
                    history_table.setItem(row, 1, QTableWidgetItem(entry['time']))
        
        calendar.clicked.connect(update_history_table)
        dialog.setLayout(layout)
        dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PeopleCounterSystem()
    ex.show()
    sys.exit(app.exec_())