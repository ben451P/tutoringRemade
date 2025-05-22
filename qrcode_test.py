from flask import Flask, render_template, send_file
import qrcode
import io
import base64

app = Flask(__name__)

@app.route('/qr')
def qr():
    # The link you want to encode
    link = "https://example.com"

    # Generate the QR code
    qr_img = qrcode.make(link)
    
    # Save it to a bytes buffer
    buffer = io.BytesIO()
    qr_img.save(buffer, format="PNG")
    buffer.seek(0)

    # Encode the image to base64
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    # Pass the image string to the template
    return render_template('qr_display.html', qr_image=img_base64)
