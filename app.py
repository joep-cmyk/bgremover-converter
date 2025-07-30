import streamlit as st
from rembg import remove
from PIL import Image
import io
import zipfile
import os
from datetime import datetime

st.set_page_config(page_title="Achtergrondverwijderaar JPG Converter", layout="centered")
st.title("🧼 Achtergrond verwijderen & converteren naar JPG")
st.markdown("Upload meerdere afbeeldingen. De achtergrond wordt wit gemaakt, en je krijgt JPG's terug als ZIP-download.")

uploaded_files = st.file_uploader(
    "📁 Upload afbeeldingen",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    with st.spinner("Bezig met verwerken..."):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for file in uploaded_files:
                # Lees originele afbeelding als bytes
                input_bytes = file.read()

                # Achtergrond verwijderen
                result_bytes = remove(input_bytes)

                # Converteer naar afbeelding
                result_image = Image.open(io.BytesIO(result_bytes)).convert("RGBA")
                white_bg = Image.new("RGB", result_image.size, (255, 255, 255))
                white_bg.paste(result_image, mask=result_image.split()[3])

                # Opslaan als JPG in memory
                img_io = io.BytesIO()
                base_name = os.path.splitext(file.name)[0]
                white_bg.save(img_io, format="JPEG", quality=95)
                img_io.seek(0)

                # Voeg toe aan ZIP
                zip_file.writestr(f"{base_name}.jpg", img_io.read())

        zip_buffer.seek(0)

        # ✅ HIER staat de correcte regel:
        tijd = datetime.now().strftime("%Y%m%d%H%M%S")

        st.success("✅ Afbeeldingen zijn verwerkt!")
        st.download_button(
            label="📥 Download ZIP met JPG's",
            data=zip_buffer,
            file_name=f"verwerkt_{tijd}.zip",
            mime="application/zip"
        )
