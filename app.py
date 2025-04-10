import streamlit as st
import qrcode
from PIL import Image
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import tempfile

st.set_page_config(page_title="QR Code App", layout="centered")
st.title("🔳 QR Code Generator & Scanner")

tab1, tab2 = st.tabs(["Generate QR Code", "Scan QR Code"])

# --- Generate QR Code Tab ---
with tab1:
    data = st.text_input("Enter data to encode")
    if st.button("Generate"):
        if data:
            qr = qrcode.make(data).convert("RGB")  # Ensure it's a proper PIL image
            st.image(qr, caption="Your QR Code", use_column_width=True)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                qr.save(tmp.name)
                st.download_button(
                    "⬇️ Download QR Code",
                    open(tmp.name, "rb"),
                    file_name="qrcode.png",
                    mime="image/png"
                )
        else:
            st.warning("⚠️ Please enter some data to generate a QR Code.")

# --- Scan QR Code Tab ---
with tab2:
    uploaded_file = st.file_uploader("📤 Upload an image containing a QR Code", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_column_width=True)

        frame = np.array(image)
        decoded_objects = decode(frame)

        if decoded_objects:
            for obj in decoded_objects:
                st.success(f"✅ Decoded Data: {obj.data.decode('utf-8')}")
        else:
            st.warning("❌ No QR code found in the uploaded image.")

