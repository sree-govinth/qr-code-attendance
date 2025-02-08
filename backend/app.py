from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Allow frontend to call backend APIs

# Dictionary to store registrations
registrations = {}

UPLOAD_FOLDER = "data"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

''' @app.route('/api/upload-excel', methods=['POST'])
def upload_excel():
    """ Handles Excel upload and stores data in memory."""
    global registrations
    file = request.files['file']
    
    if not file:
        return jsonify({"success": False, "message": "No file uploaded"})

    df = pd.read_excel(file)

    print(f"file uploaded at {file_path}")
    
    # Ensure there's an 'ID' column in the uploaded file
    if "ID" not in df.columns:
        return jsonify({"success": False, "message": "Excel must contain 'ID' column!"})
    
    registrations = df.set_index("ID").to_dict(orient="index")
    
    return jsonify({"success": True, "message": "Excel uploaded successfully!"}) '''

@app.route("/api/upload-excel", methods=["POST"])
def upload_excel():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save the file
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    return jsonify({"success": True, "message": "File uploaded!", "file_path": file_path}), 200    

# Load the registration data
REGISTRATION_FILE = "data/registration.xlsx"

def load_registered_users():
    if os.path.exists(REGISTRATION_FILE):
        return pd.read_excel(REGISTRATION_FILE)
    return pd.DataFrame()

@app.route("/api/mark-attendance", methods=["POST"])
def mark_attendance():
    data = request.get_json()
    scanned_id = data.get("scanned_id")

    # Clean the scanned ID by removing unnecessary text and symbols
    scanned_id = scanned_id.replace("ID:", "").strip(", ").strip()

    # Load registered users
    df = load_registered_users()

    print("\n==== DEBUG: Cleaned Scanned ID ====")
    print(scanned_id)

    if "ID" not in df.columns:
        return jsonify({"success": False, "message": "ID column missing in Excel!"})

    # Convert both to string for accurate comparison
    df["ID"] = df["ID"].astype(str)
    scanned_id = str(scanned_id)

    # Check if scanned ID exists
    if scanned_id in df["ID"].values:
        df.loc[df["ID"] == scanned_id, "Attendance"] = "Present"
        df.to_excel(REGISTRATION_FILE, index=False)
        print("\n==== DEBUG: Attendance Marked! ====")
        return jsonify({"success": True, "message": "Attendance marked!"})

    print("\n==== DEBUG: ID Not Found! ====")
    return jsonify({"success": False, "message": "User not found!"})

if __name__ == '__main__':
    app.run(debug=True)
