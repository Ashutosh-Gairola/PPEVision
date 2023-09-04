import streamlit as st
import cv2

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
                   page_icon='./Images/vicon.jpeg')
st.markdown("""
<style>
    .centered-text {
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px solid black;
        padding: 20px;
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

description = """
## About PPE Detection

This application uses YOLO (You Only Look Once), a real-time object detection algorithm, to detect and identify
the presence of Personal Protective Equipment (PPE) in an uploaded Video. Specifically, it can detect Helmets and
Vests, which are important safety gear in various scenarios such as construction sites, industrial environments,
and sports activities.

The model used in this application is powered by YOLOv5, which is based on the ONNX (Open Neural Network Exchange)
format. It has been trained on a diverse dataset to achieve accurate and reliable detections.

Please upload an Video to see the PPE detection in action!
"""

st.markdown('<div class="centered-text"><h1>Get Detection for Video</h1></div>', unsafe_allow_html=True)

st.write('Please Upload Video to get detections')
st.caption('This can detect Helmet and Vest')

with st.spinner('Please wait while your model is loading'):
    yolo = YOLO_Pred(onnx_model="./Models/best150.onnx",
                     data_yaml="./Models/data.yaml")
def upload_video():
    uploaded_file = st.file_uploader("Upload Video", type=["mp4"])
    st.markdown("<hr style='height:2px;border-width:0;color:#f63366;background-color:#f63366;'>", unsafe_allow_html=True)
    st.markdown(description, unsafe_allow_html=True)
    return uploaded_file

def main():
    video_file = upload_video()

    if video_file is not None:
        temp_file = './temp.mp4'
        with open(temp_file, 'wb') as f:
            f.write(video_file.getvalue())

        cap = cv2.VideoCapture(temp_file)
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        out = cv2.VideoWriter('./output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame_width, frame_height))
        stframe = st.empty()
        paused = False
        stopped = False

        col1, col2 = st.columns(2)  # Create two columns

        start_button = col1.button('Start')  # Assign button to col1
        stop_button = col2.button('Stop')  # Assign button to col2

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if start_button:
                paused = False
            elif stop_button:
                stopped = True
                break

            if not paused:
                output_frame = yolo.predictions(frame)
                out.write(output_frame)
                stframe.image(output_frame, channels="BGR")

        cap.release()
        out.release()
        if stopped:
            st.success('Video processing stopped!')
        else:
            st.success('Video processed successfully!')
            st.video('./output.mp4')
    else:
        st.warning('Please upload a video file.')

if __name__ == "__main__":
    main()
