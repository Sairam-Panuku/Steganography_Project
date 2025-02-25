from flask import Flask, render_template, request, redirect, url_for, send_file, flash, session
import os
from encrypt import encrypt_image
from decrypt import decrypt_image

app = Flask(__name__)
app.secret_key = "your_secret_key"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    decrypted_message = session.pop("decrypted_message", None)  # Get message if available
    return render_template("index.html", decrypted_message=decrypted_message)

@app.route("/encrypt", methods=["POST"])
def encrypt():
    if "image" not in request.files:
        flash("No image uploaded!")
        return redirect(url_for("index"))
    
    image = request.files["image"]
    message = request.form["message"]
    passcode = request.form["passcode"]

    if not message or not passcode:
        flash("Message and passcode are required!")
        return redirect(url_for("index"))
    
    image_path = os.path.join(UPLOAD_FOLDER, "input_image.jpg")
    encrypted_image_path = os.path.join(UPLOAD_FOLDER, "encrypted_image.png")
    
    image.save(image_path)
    
    success = encrypt_image(image_path, encrypted_image_path, message, passcode)
    if success:
        flash("✅ Encryption successful! Download your encrypted image.")
        return send_file(encrypted_image_path, as_attachment=True)
    else:
        flash("❌ Encryption failed!")
        return redirect(url_for("index"))

@app.route("/decrypt", methods=["POST"])
def decrypt():
    if "image" not in request.files:
        flash("No image uploaded!")
        return redirect(url_for("index"))

    image = request.files["image"]
    passcode = request.form["passcode"]

    if not passcode:
        flash("Passcode is required!")
        return redirect(url_for("index"))

    image_path = os.path.join(UPLOAD_FOLDER, "uploaded_encrypted_image.png")
    image.save(image_path)

    message = decrypt_image(image_path, passcode)
    if message is None:
        flash("❌ Decryption failed! Incorrect passcode or corrupted image.")
        return redirect(url_for("index"))
    
    session["decrypted_message"] = message  # Store message in session
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
