import cv2
import face_recognition
import numpy as np
from tkinter import Tk, Label, Button, Listbox, StringVar, Entry, messagebox, simpledialog, Toplevel
import os
import pickle
import threading
import pandas as pd
from datetime import datetime

class AttendanceSystem:
    def __init__(self, master):
        self.master = master
        master.title("Facial Recognition Attendance System")

        self.name_var = StringVar()

        # Name input label and entry
        self.name_label = Label(master, text="Enter Name:")
        self.name_label.grid(row=0, column=0, padx=10, pady=10)

        self.name_entry = Entry(master, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.register_button = Button(master, text="Register New Face", command=self.start_register_face)
        self.register_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.attendance_button = Button(master, text="Take Attendance", command=self.take_attendance)
        self.attendance_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.view_button = Button(master, text="View Attendance", command=self.view_attendance)
        self.view_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.view_profiles_button = Button(master, text="View Profiles", command=self.view_profiles)
        self.view_profiles_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.delete_profile_button = Button(master, text="Delete Profile", command=self.delete_profile)
        self.delete_profile_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.attendance_list = Listbox(master)
        self.attendance_list.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.students = {}
        self.load_data()

    def start_register_face(self):
        name = self.name_var.get()
        if not name:
            messagebox.showerror("Error", "Please enter a name.")
            return

        self.animation_window = Toplevel(self.master)
        self.animation_window.title("Registering Face")
        Label(self.animation_window, text="Preparing to register face...").pack(padx=10, pady=10)

        # Start the face registration in a new thread
        threading.Thread(target=self.register_face, args=(name,)).start()

    def register_face(self, name):
        cap = cv2.VideoCapture(0)
        frames = []
        detected_faces = 0

        while detected_faces < 3:  # Capture 3 valid frames
            ret, frame = cap.read()
            if not ret:
                break
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)

            if face_locations:
                # Capture only if a face is detected
                top, right, bottom, left = face_locations[0]
                cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)  # Blue box
                cv2.putText(frame, "Scanning...", (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

                frames.append(rgb_frame)
                detected_faces += 1

            cv2.imshow("Registering Face", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit if 'q' is pressed
                break

        cap.release()
        cv2.destroyAllWindows()

        if len(frames) == 3:
            # Process frames to create a face encoding
            encodings = [face_recognition.face_encodings(frame)[0] for frame in frames if face_recognition.face_encodings(frame)]
            if encodings:
                self.students[name] = np.mean(encodings, axis=0)  # Use average encoding
                with open('students.pkl', 'wb') as f:
                    pickle.dump(self.students, f)
                messagebox.showinfo("Success", f"Registered {name} successfully!")
            else:
                messagebox.showerror("Error", "No face detected. Please try again.")
        else:
            messagebox.showerror("Error", "Not enough valid frames captured. Please try again.")

    def take_attendance(self):
        cap = cv2.VideoCapture(0)
        recognized_students = set()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding, face_location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(list(self.students.values()), face_encoding)

                if True in matches:
                    first_match_index = matches.index(True)
                    name = list(self.students.keys())[first_match_index]
                    recognized_students.add(name)

                    # Draw a box around the face
                    top, right, bottom, left = face_location
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            cv2.imshow("Taking Attendance", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
                break

        cap.release()
        cv2.destroyAllWindows()

        if recognized_students:
            for student in recognized_students:
                self.attendance_list.insert(0, student)
            self.store_attendance(recognized_students)
            messagebox.showinfo("Attendance", f"Attendance taken for: {', '.join(recognized_students)}")
        else:
            messagebox.showwarning("Attendance", "No students recognized.")

    def store_attendance(self, recognized_students):
        # Get today's date
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = f"attendance_{date_str}.xlsx"

        # Load existing attendance or create a new DataFrame
        if os.path.exists(filename):
            df = pd.read_excel(filename)
        else:
            df = pd.DataFrame(columns=["Date", "Name"])

        # Append new attendance data
        for student in recognized_students:
            df = df.append({"Date": date_str, "Name": student}, ignore_index=True)

        # Save to Excel
        df.to_excel(filename, index=False)

    def view_attendance(self):
        attendance = self.attendance_list.get(0, 'end')
        messagebox.showinfo("Attendance List", "\n".join(attendance))

    def view_profiles(self):
        profiles = "\n".join(self.students.keys())
        messagebox.showinfo("Registered Profiles", profiles if profiles else "No profiles registered.")

    def delete_profile(self):
        name = simpledialog.askstring("Delete Profile", "Enter the name of the profile to delete:")
        if name in self.students:
            del self.students[name]
            with open('students.pkl', 'wb') as f:
                pickle.dump(self.students, f)
            messagebox.showinfo("Success", f"Deleted profile for {name}.")
        else:
            messagebox.showwarning("Error", f"No profile found for {name}.")

    def load_data(self):
        if os.path.exists('students.pkl'):
            with open('students.pkl', 'rb') as f:
                self.students = pickle.load(f)

if __name__ == "__main__":
    root = Tk()
    attendance_system = AttendanceSystem(root)
    root.mainloop()
