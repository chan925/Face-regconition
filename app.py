from flask import Flask, render_template, request
import face_recognition
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
KNOWN_FOLDER = 'known'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load known face once when app starts
known_face_image = face_recognition.load_image_file(os.path.join(KNOWN_FOLDER, "known_person.jpg"))
known_face_encoding = face_recognition.face_encodings(known_face_image)[0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    unknown_image = face_recognition.load_image_file(filepath)
    unknown_encodings = face_recognition.face_encodings(unknown_image)

    if not unknown_encodings:
        return "No face detected in the uploaded image."

    # Compare uploaded face(s) to the known face
    results = face_recognition.compare_faces([known_face_encoding], unknown_encodings[0])

    if results[0]:
        return "Face matched with known person."
    else:
        return "Face does NOT match the known person."

@app.route('/capture', methods=['GET'])
def capture():
    os.system("termux-camera-photo -c 0 uploads/captured.jpg")
    return "Photo captured from camera. You can now upload it for recognition."
