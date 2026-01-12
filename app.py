import streamlit as st
from PIL import Image
from processor import create_photo_strip
import os

st.set_page_config(page_title="Photo Booth", layout="centered")
st.title("📸 Photo Booth – Cloud Version")

os.makedirs("photos", exist_ok=True)
os.makedirs("strips", exist_ok=True)

uploaded_files = st.file_uploader(
    "Upload photos",
    type=["jpg", "png"],
    accept_multiple_files=True
)

photo_paths = []

if uploaded_files:
    for file in uploaded_files:
        path = f"photos/{file.name}"
        with open(path, "wb") as f:
            f.write(file.read())
        photo_paths.append(path)

    st.success(f"{len(photo_paths)} photos uploaded")

    if st.button("Create Photo Strip"):
        strip_path = create_photo_strip(photo_paths)
        img = Image.open(strip_path)
        st.image(img, caption="Generated Photo Strip")
        st.download_button(
            "Download Photo Strip",
            open(strip_path, "rb"),
            file_name="photo_strip.jpg"
        )
