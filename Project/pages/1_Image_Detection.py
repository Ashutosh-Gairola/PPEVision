import streamlit as st
from PIL import Image
import numpy as np

# Import yolo_predictions using an absolute import
import sys
import os

# Get the absolute path to the parent directory of yolo_predictions.py
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to the Python path
sys.path.append(parent_dir)

# Now you can import yolo_predictions
from yolo_predictions import YOLO_Pred




st.set_page_config(page_title="Detection",
                   layout='wide',
                   page_icon='./Images/imageicon.jpg')

# Custom CSS styles
st.markdown(
    """
    <style>
    .header-container {
        border: 2px solid #555555;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #008080;
        text-decoration: underline;
    }
    .centered-text {
        text-align: center;
    }
    .caption {
        font-style: italic;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

description = """
## About PPE Detection

This application uses YOLO (You Only Look Once), a real-time object detection algorithm, to detect and identify
the presence of Personal Protective Equipment (PPE) in an uploaded image. Specifically, it can detect Helmets and
Vests, which are important safety gear in various scenarios such as construction sites, industrial environments,
and sports activities.

The model used in this application is powered by YOLOv5, which is based on the ONNX (Open Neural Network Exchange)
format. It has been trained on a diverse dataset to achieve accurate and reliable detections.

Please upload an image to see the PPE detection in action!
"""


header_html = """
<div class='header-container'>
    <h1 class='centered-text'>Get Detection for Image</h1>
</div>
"""

st.markdown(header_html, unsafe_allow_html=True)
st.markdown("<p class='centered-text'>Please Upload Image to get detections</p>", unsafe_allow_html=True)
with st.spinner('Please wait while your model is loading'):
    yolo = YOLO_Pred(onnx_model="./Models/best150.onnx",
                     data_yaml="./Models/data.yaml")



def upload_image():
    # Upload Image
    
    image_file = st.file_uploader(label='Upload Image')
    if image_file is not None:
        size_mb = image_file.size / (1024 ** 2)
        file_details = {
            "filename": image_file.name,
            "filetype": image_file.type,
            "filesize": "{:,.2f} MB".format(size_mb)
        }

        # Validate file
        if file_details['filetype'] in ('image/png', 'image/jpeg'):
            st.success('VALID IMAGE file type (png or jpeg)')
            return {"file": image_file, "details": file_details}
        else:
            st.error('INVALID Image file type')
            st.error('Upload only png, jpg, jpeg')
            return None
    st.warning('Please upload a Image file.')
    st.markdown("<hr style='height:2px;border-width:0;color:#f63366;background-color:#f63366;'>", unsafe_allow_html=True)
    st.markdown(description, unsafe_allow_html=True)


def main():
    object = upload_image()

    if object:
        prediction = False
        image_obj = Image.open(object['file'])

        col1, col2 = st.columns(2)

        with col1:
            st.info('Preview of Image')
            st.image(image_obj)

        with col2:
            st.subheader('Check below for file details')
            st.json(object['details'])
            button = st.button('Get Detection from YOLO')
            if button:
                with st.spinner("Getting Objects from the image. Please wait..."):
                    # Convert object to array
                    image_array = np.array(image_obj)
                    pred_img = yolo.predictions(image_array)
                    pred_img_obj = Image.fromarray(pred_img)
                    prediction = True

        if prediction:
            st.subheader("Predicted Image")
            st.caption("Object detection from YOLO V5 model")
            st.image(pred_img_obj)





if __name__ == "__main__":
    main()

    

#@main_________________________________________________________________________________________


