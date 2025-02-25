from stegano import lsb

def decrypt_image(image_path, passcode):
    try:
        # Extract hidden data
        extracted_data = lsb.reveal(image_path)

        if extracted_data is None:
            return None

        # Extract passcode and message
        stored_passcode, secret_message = extracted_data.split(':', 1)

        # Check if passcode matches
        if stored_passcode == passcode:
            return secret_message
        else:
            return None
    except Exception as e:
        print(f"Error during decryption: {str(e)}")
        return None
