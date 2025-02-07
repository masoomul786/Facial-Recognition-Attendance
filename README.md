# Facial Recognition Attendance System

## Overview
The Facial Recognition Attendance System is a Python-based application that uses OpenCV and the face_recognition library to register and recognize faces for attendance tracking. It allows users to register their faces, take attendance using a webcam, and store attendance records in an Excel file.

## Features
- **Face Registration**: Register new faces with a name.
- **Attendance Tracking**: Detect and recognize faces to mark attendance.
- **View Attendance Records**: Display attendance records.
- **View Registered Profiles**: List registered profiles.
- **Delete Profiles**: Remove stored profiles.
- **Data Persistence**: Saves attendance records in an Excel file.

## Installation
### Prerequisites
Ensure you have Python installed. Then, install the required dependencies:
```sh
pip install opencv-python numpy face-recognition pandas tkinter
```

## Usage
### Running the Application
1. Clone the repository:
   ```sh
   git clone https://github.com/masoomul786/Facial-Recognition-Attendance.git
   cd Facial-Recognition-Attendance
   ```
2. Run the script:
   ```sh
   python attendance_system.py
   ```

### Register a New Face
1. Enter the name of the person in the input field.
2. Click "Register New Face."
3. The system will capture and encode the face.

### Take Attendance
1. Click "Take Attendance."
2. The system will use the webcam to recognize faces and mark attendance.

### View Attendance
Click "View Attendance" to see the recorded attendance list.

### View Registered Profiles
Click "View Profiles" to see all registered users.

### Delete a Profile
Click "Delete Profile" and enter the name of the profile you want to delete.

## File Storage
- **students.pkl**: Stores registered face encodings.
- **attendance_YYYY-MM-DD.xlsx**: Stores daily attendance records.

## License
This project is licensed under the MIT License.

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## Author
- **Your Name**  
  [GitHub Profile](https://github.com/masoomul786)

