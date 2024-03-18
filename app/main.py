import streamlit as st
import requests
import base64
import json

API_URL = "https://app-backend-v3zxsfhx557qe.azurewebsites.net"

st.title("AI Pediatrician | Admin App")

headers = {
        'Content-Type': 'application/json'
        }

uploaded_files = st.file_uploader("Upload Files", type=["pdf", "txt", "docx"], accept_multiple_files=True)
# Process Button
if st.button("Process Files"):
    if uploaded_files:
        api_url = f"{API_URL}/process"
        # Create a list to store file data as base64-encoded strings
        encoded_files = [{"name": f.name, "data": base64.b64encode(f.read()).decode()} for f in uploaded_files]
        data = {
            "files": encoded_files
        }
        
        # headers = {"Content-Type": "application/json"}
        with st.spinner('Processing files...'):
            try:
                response = requests.post(api_url, data=json.dumps(data), headers=headers)
                if response.status_code == 200:
                    st.success("Files processed successfully!")
                else:
                    st.error("An error occurred while processing files.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please upload files to proceed.")