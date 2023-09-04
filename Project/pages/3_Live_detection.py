import time
import streamlit as st
import cv2
import os

# Get the absolute path to the parent directory of yolo_predictions.py
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to the Python path
sys.path.append(parent_dir)

# Now you can import yolo_predictions
from yolo_predictions import YOLO_Pred



# Custom CSS styles
custom_css = """
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
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Centered header with borders
st.markdown("<div class='header-container centered-text'><h1>Get Detection in Real Time</h1></div>", unsafe_allow_html=True)
st.caption('This can detect Helmet and Vest')

with st.spinner('Please wait while your model is loading'):
    yolo = YOLO_Pred(onnx_model="./Models/best150.onnx",
                     data_yaml="./Models/data.yaml")

def select_camera():
    # Get the number of connected cameras
    num_cameras = 0
    for i in range(10):  # Check up to 10 cameras (you can adjust this value if needed)<--------------
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            num_cameras += 1
            cap.release()

    if num_cameras == 0:
        st.error("No camera found.")
        return None

    if num_cameras == 1:
        st.info("Found 1 camera.")
        return cv2.VideoCapture(0)

    # If multiple cameras are available, ask the user to select one or show all cameras
    camera_choices = [f"Camera {i}" for i in range(num_cameras)]
    camera_choices.append("Show All Cameras")
    selected_camera = st.selectbox("Select Camera:", camera_choices)

    if selected_camera == "Show All Cameras":
        return [cv2.VideoCapture(i) for i in range(num_cameras)]
    else:
        return cv2.VideoCapture(int(selected_camera.split()[-1]))

def main():
    # Ask the user to select the camera(s)
    cameras = select_camera()
    if cameras is None:
        return

    # Add the starting time and frame_skip variables
    starting_time = time.time()
    frame_id = 0
    
    frame_skip = 1
    fps = 15

    if isinstance(cameras, list):
        stframe = st.empty()

        while True:
            frames = [cap.read()[1] for cap in cameras]

            # Increment frame_id and calculate the elapsed time
            frame_id += 1
            elapsed_time = time.time() - starting_time

            # Check if it's time to skip frames
            if frame_id % frame_skip != 0:
                continue

            # Predictions should be done on every frame_skip interval
            pred_imgs = [yolo.predictions(frame) for frame in frames]

            # Display the prediction images on the Streamlit app side by side
            combined_img = cv2.hconcat(pred_imgs)
            stframe.image(combined_img, channels="BGR")

            # Press 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    else:
        stframe = st.empty()

        while True:
            ret, frame = cameras.read()
            if not ret:
                break

            # Increment frame_id and calculate the elapsed time
            frame_id += 1
            elapsed_time = time.time() - starting_time

            # Check if it's time to skip frames
            if frame_id % frame_skip != 0:
                continue

            # Predictions should be done on every frame_skip interval
            pred_img = yolo.predictions(frame)

            # Display the prediction image on the Streamlit app
            stframe.image(pred_img, channels="BGR")

            # Press 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release the cameras and close the Streamlit app
    if isinstance(cameras, list):
        for cap in cameras:
            cap.release()
    else:
        cameras.release()

if __name__ == "__main__":
    main()

