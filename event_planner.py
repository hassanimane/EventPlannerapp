import qrcode

# Update this URL with your deployed app's public URL
url = "https://eventplannerapp-942s.onrender.com"

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("event_qr.png")
print("QR code saved as event_qr.png")
