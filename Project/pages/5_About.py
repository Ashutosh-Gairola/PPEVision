import streamlit as st

st.set_page_config(page_title="About",
                   layout='wide',
                   page_icon='./Images/abouticon.jpg')



def main():
    st.title("About")
    st.write("## Hi there! I'm Ashutosh Gairola.")
    st.write("Welcome to my application powered by YOLO (You Only Look Once) - an object detection algorithm that detects helmets and reflective vests. This project combines computer vision with real-time and image analysis to enhance safety measures in various scenarios.")
    st.write("### 1. Detect from Image")
    st.write("With this application, you can easily detect helmets and reflective vests in static images. Simply upload an image, and the YOLO algorithm will analyze it, identify the objects of interest, and highlight them for you. Whether it's a construction site, a biking event, or any other situation where helmets and reflective vests are essential, this feature can help ensure compliance with safety protocols.")
    st.write("### 2. Detect in Real Time")
    st.write("Safety monitoring becomes even more effective with the real-time detection capability of this application. You can use your webcam to scan your surroundings and receive immediate feedback on the presence of helmets and reflective vests. This functionality is invaluable for situations that require continuous monitoring, such as factory floors, work zones, or sports events.")
    st.write("### 3. Detect from Video")
    st.write("Sometimes, analyzing a series of images or frames is necessary for a more comprehensive understanding of safety compliance. In the video mode of this application, you can upload a video file, and the algorithm will perform object detection on each frame. This enables you to visualize and review safety practices over time, allowing for more accurate assessments and improvements.")
    st.write("## Why YOLO?")
    st.write("YOLO is a state-of-the-art object detection algorithm known for its speed and accuracy. It processes images and video frames in real time, providing near-instantaneous results. By utilizing YOLO as the backbone of this application, I aim to provide a user-friendly and efficient solution for enhancing safety protocols.")
    st.write("## How to Use")
    st.write("Using this application is straightforward. You'll find three tabs corresponding to the three detection modes: 'Image Detection,' 'Live detection,' and 'Video Detection.' Choose the desired mode, follow the instructions on each tab, and let the algorithm do its magic. The detected objects will be highlighted, making them easily distinguishable from the rest of the scene.")
    st.write("## About Me")
    st.write("My name is Ashutosh Gairola, and I'm passionate about leveraging technology to improve safety in various domains. This project is a culmination of my interest in computer vision and my desire to contribute to the well-being of individuals in potentially hazardous environments.")
    st.write("If you have any questions, feedback, or suggestions, please don't hesitate to reach out. I hope this application proves useful in promoting safety and helps prevent accidents in different settings.")
    st.write("Stay safe!")
    
if __name__ == "__main__":
    main()
