from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import os
from encrypt import encrypt_image
from decrypt import decrypt_image

app = Flask(__name__)
app.secret_key = "your_secret_key"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/encrypt", methods=["GET", "POST"])
def encrypt():
    if request.method == "POST":
        if "image" not in request.files:
            flash("No image uploaded!")
            return redirect(url_for("encrypt"))

        image = request.files["image"]
        message = request.form["message"]
        passcode = request.form["passcode"]

        if not message or not passcode:
            flash("Message and passcode are required!")
            return redirect(url_for("encrypt"))

        image_path = os.path.join(UPLOAD_FOLDER, "input_image.jpg")
        encrypted_image_path = os.path.join(UPLOAD_FOLDER, "encrypted_image.png")

        image.save(image_path)

        success = encrypt_image(image_path, encrypted_image_path, message, passcode)
        if success:
            flash("✅ Encryption successful! Download your encrypted image.")
            return send_file(encrypted_image_path, as_attachment=True)
        else:
            flash("❌ Encryption failed!")
            return redirect(url_for("encrypt"))

    return render_template("encrypt.html")

@app.route("/decrypt", methods=["GET", "POST"])
def decrypt():
    if request.method == "POST":
        if "image" not in request.files:
            flash("No image uploaded!")
            return redirect(url_for("decrypt"))

        image = request.files["image"]
        passcode = request.form["passcode"]

        if not passcode:
            flash("Passcode is required!")
            return redirect(url_for("decrypt"))

        image_path = os.path.join(UPLOAD_FOLDER, "uploaded_encrypted_image.png")
        image.save(image_path)

        message = decrypt_image(image_path, passcode)
        if message is None:
            flash("❌ Decryption failed! Incorrect passcode or corrupted image.")
            return redirect(url_for("decrypt"))

        flash(f"✅ Decrypted Message: {message}")
        return redirect(url_for("decrypt"))

    return render_template("decrypt.html")

if __name__ == "__main__":
    app.run(debug=True)
