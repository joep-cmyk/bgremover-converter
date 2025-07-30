import streamlit as st
from rembg import remove
from PIL import Image
import io
import zipfile
import os
from datetime import datetime

st.set_page_config(page_title="Achtergrondverwijderaar JPG Converter", layout="centered")
st.title("Achtergrond verwijderen & converteren naar JPG")
st.markdown("Upload meerdere afbeeldingen. De achtergrond wordt wit gemaakt, en je krijgt JPG's terug als ZIP-download.")

uploaded_files = st.file_uploader("📁 Upload afbeeldingen", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    with st.spinner("Bezig met verwerken..."):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for file in uploaded_files:
                # Lees de afbeelding als bytes
                input_bytes = file.read()

                # Verwijder achtergrond
                result_bytes = remove(input_bytes)

                # Converteer terug naar afbeelding
                result = Image.open(io.BytesIO(result_bytes)).convert("RGBA")

                # Transparantie → wit
                background = Image.new("RGB", result.size, (255, 255, 255))
                background.paste(result, mask=result.split()[3])  # Gebruik alpha-kanaal als masker

                # Opslaan als JPG in geheugen
                img_bytes = io.BytesIO()
                clean_name = os.path.splitext(file.name)[0]
                background.save(img_bytes, format="JPEG", quality=95)
                img_bytes.seek(0)

                # Voeg toe aan ZIP-bestand
                zip_file.writestr(f"{clean_name}.jpg", img_bytes.read())

        zip_buffer.seek(0)
        tijd = datetime.no
