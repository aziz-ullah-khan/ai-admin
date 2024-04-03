import streamlit as st
import requests
import base64
import json
import os
import io
from PyPDF2 import PdfFileReader, PdfFileWriter

API_URL = "https://app-backend-v3zxsfhx557qe.azurewebsites.net/"
# API_URL = 'http://localhost:50505'

st.title("AI Pediatrician | Admin App")

headers = {
        'Content-Type': 'application/json'
        }


def split_and_encode_pdf(pdf_file):
    pdf_reader = PdfFileReader(pdf_file)
    num_pages = pdf_reader.numPages

    encoded_sub_files = []

    for i in range(0, num_pages, 10):
        pdf_writer = PdfFileWriter()

        for page_num in range(i, min(i+10, num_pages)):
            pdf_writer.addPage(pdf_reader.getPage(page_num))

        output_pdf_bytes = io.BytesIO()
        pdf_writer.write(output_pdf_bytes)
        output_pdf_bytes.seek(0)

        encoded_data = base64.b64encode(output_pdf_bytes.read()).decode()
        encoded_sub_files.append({
            "name": f"{os.path.splitext(pdf_file.name)[0]}_{i+1}-{min(i+10, num_pages)}.pdf",
            "data": encoded_data
        })

    return encoded_sub_files

uploaded_files = st.file_uploader("Upload Files", type=["pdf"], accept_multiple_files=False)

# Process Button
if st.button("Process Files"):
    if uploaded_files:
        with st.spinner('Processing files...'):
            try:
                api_url = f"{API_URL}/process"
                headers = {"Content-Type": "application/json"}

                encoded_files = []
                for file in uploaded_files:
                    if file.type == 'application/pdf':
                        encoded_sub_files = split_and_encode_pdf(file)
                        encoded_files.extend(encoded_sub_files)
                    else:
                        # For other file types, encode the entire file
                        encoded_files.append({
                            "name": file.name,
                            "data": base64.b64encode(file.read()).decode()
                        })

                data = {
                    "files": encoded_files
                }

                response = requests.post(api_url, data=json.dumps(data), headers=headers)

                if response.status_code == 200:
                    st.success("Files processed successfully!")
                else:
                    st.error(f"An error occurred while processing files. {response.json()}")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please upload files to proceed.")
