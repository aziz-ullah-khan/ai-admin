import streamlit as st
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

# Set up the Streamlit app
st.set_page_config(page_title="File Processing App", page_icon=":file_folder:", layout="wide")

# Custom CSS styles
st.markdown(
    """
    <style>
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #2F4F4F;
        margin-bottom: 20px;
    }
    .success-message {
        color: #2E8B57;
        font-weight: bold;
    }
    .error-message {
        color: #DC143C;
        font-weight: bold;
    }
    .warning-message {
        color: #FF8C00;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

import time
# App title

st.header('AI Pediatrician | Admin App', divider='rainbow')

# Create a "data" folder if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# File uploader
uploaded_files = st.file_uploader("Choose files to upload", accept_multiple_files=True)

# Process button
if st.button("Process"):
    try:
        if uploaded_files:
            # Display a progress bar
            with st.spinner('Processing Files...'):
                # Save uploaded files to the "data" folder
                for i, uploaded_file in enumerate(uploaded_files):
                    file_path = os.path.join("data", uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getvalue())

                # Call the prepdocs.sh script
                try:
                    subprocess.run(["bash", "./prepdocs.sh"], check=True)
                    time.sleep(5)
                except subprocess.CalledProcessError as e:
                    st.markdown(f'<div class="error-message">Error occurred while processing files: {str(e)}</div>', unsafe_allow_html=True)

                # Delete the processed files
                for file_name in os.listdir("data"):
                    file_path = os.path.join("data", file_name)
                    os.remove(file_path)

                st.markdown('<div class="success-message">Files processed successfully!</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-message">No files uploaded.</div>', unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f'<div class="error-message">Error occurred: {str(e)}</div>', unsafe_allow_html=True)
        # Delete the processed files
        for file_name in os.listdir("data"):
            file_path = os.path.join("data", file_name)
            os.remove(file_path)