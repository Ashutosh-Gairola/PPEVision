#!/usr/bin/env python
import cv2
import numpy as np
import os
import pythoncom
import yaml
from yaml.loader import SafeLoader
import win32com.client as win32
import datetime
import time
import threading
from pygame import mixer


class YOLO_Pred():

    def __init__(self, onnx_model, data_yaml):
        # Load YAML
        with open(data_yaml, mode='r') as f:
            data_yaml = yaml.load(f, Loader=SafeLoader)

        self.labels = data_yaml['names']
        self.nc = data_yaml['nc']
        self.class_counts = {}

        # Load YOLO model
        self.yolo = cv2.dnn.readNetFromONNX(onnx_model)
        self.yolo.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.yolo.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        # Initialize the object_counts and object_counts_temp dictionaries
        self.object_counts = {class_label: 0 for class_label in self.labels}
        self.object_counts_temp = {class_label: 0 for class_label in self.labels}
        self.count_increased = {class_label: False for class_label in self.labels}

        # Path to the folder where images with count increase will be saved
        self.save_folder = "apliance_data"
        os.makedirs(self.save_folder, exist_ok=True)

        # Path to the folder where images with "No helmet" and "No vest" will be saved
        self.non_app_folder = "non_applicance"
        os.makedirs(self.non_app_folder, exist_ok=True)

        # Initialize variables for email alert
        self.alert_sent_time = {class_label: 0 for class_label in self.labels}
        self.message_alert_threshold = 60  # Threshold in seconds to control message alert frequency
        self.Mail_id = "exampl123@gmail.com"  # Replace with your Mail Id


    def get_next_object_id(self):
        self.object_id += 1
        return self.object_id

    def predictions(self, image):
        row, col, d = image.shape
        # Get the YOLO prediction from the image
        # Step 1: Convert the image into a square image (array)
        max_rc = max(row, col)
        input_image = np.zeros((max_rc, max_rc, 3), dtype=np.uint8)
        input_image[0:row, 0:col] = image
        # Step 2: Get predictions from the square array
        INPUT_WH_YOLO = 640
        blob = cv2.dnn.blobFromImage(input_image, 1/255, (INPUT_WH_YOLO, INPUT_WH_YOLO), swapRB=True, crop=False)
        self.yolo.setInput(blob)
        preds = self.yolo.forward()  # Detection or prediction from YOLO

        # Non-Maximum Suppression (NMS)
        # Step 1: Filter detections based on confidence (0.4) and probability score (0.25)
        detections = preds[0]
        boxes = []
        confidences = []
        classes = []

        # Width and height of the image (input_image)
        image_w, image_h = input_image.shape[:2]
        x_factor = image_w / INPUT_WH_YOLO
        y_factor = image_h / INPUT_WH_YOLO

        self.object_id = 0  # Reset object ID counter for each frame

        for i in range(len(detections)):
            row = detections[i]
            confidence = row[4]  # Confidence of detecting an object
            if confidence > 0.4:
                class_score = row[5:].max()  # Maximum probability from 20 objects
                class_id = row[5:].argmax()  # Get the index position at which max probability occurs

                if class_score > 0.45:
                    cx, cy, w, h = row[0:4]
                    # Construct bounding box from four values
                    # Left, top, width, and height
                    left = int((cx - 0.5 * w) * x_factor)
                    top = int((cy - 0.5 * h) * y_factor)
                    width = int(w * x_factor)
                    height = int(h * y_factor)

                    box = np.array([left, top, width, height])

                    # Append values into the list
                    confidences.append(confidence)
                    boxes.append(box)
                    classes.append(class_id)

        # Clean
        boxes_np = np.array(boxes).tolist()
        confidences_np = np.array(confidences).tolist()

        # NMS
        index = np.array(cv2.dnn.NMSBoxes(boxes_np, confidences_np, 0.25, 0.45)).flatten()

        # Initialize count variables for each object class
        object_counts = {class_label: 0 for class_label in self.labels}

        # Get the class label and count "No helmet" and "No vest"
        for ind in index:
            x, y, w, h = boxes_np[ind]
            bb_conf = int(confidences_np[ind] * 100)
            classes_id = classes[ind]
            class_name = self.labels[classes_id]
            color = (0, 0, 255)  # Default color: Blue

            # Check if the class is helmet (0) or vest (2)
            if classes_id == 0 or classes_id == 2:
                color = (0, 255, 0)  # Green color for helmet or vest
            else:
                color = (0, 0, 255)  # Red color for other classes

            object_id = self.get_next_object_id()  # Get the next object ID
            id_text = f'ID:{object_id}'  # Format the ID text

            # Draw ID text in yellow color to the left of the bounding box
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 5)
            cv2.rectangle(image, (x - 65, y - 30), (x, y), color, -1)
            cv2.putText(image, id_text, (x - 55, y - 10), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 255), 2)
            cv2.putText(image, f'{class_name}: {bb_conf}%', (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 34), 2)

            # Increment count for detected object class
            object_counts[class_name] += 1

        # Check if the count of "No helmet" or "No vest" increased or went to zero and then increased again
        for class_label in self.labels:
            if object_counts[class_label] > self.object_counts_temp[class_label]:
                self.count_increased[class_label] = True
            elif object_counts[class_label] == 0 and self.object_counts_temp[class_label] > 0:
                # The count went to 0 and then increased again
                self.count_increased[class_label] = True
            else:
                self.count_increased[class_label] = False

        # Check if any count increased for any class
        if any(self.count_increased.values()):
            # Save the image in the 'saved_data' folder or 'NON_APP' folder based on class label
            self.current_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            for class_label in self.labels:
                if self.count_increased[class_label]:
                    if class_label in ["No helmet", "No vest"]:
                        save_folder =self.non_app_folder
                        filename = os.path.join(save_folder, f"{class_label.replace(' ', '_')}_{self.current_timestamp}.jpg")
                        cv2.imwrite(filename, image)

                        # Check if a message alert should be sent
                        if (time.time() - self.alert_sent_time[class_label]) > self.message_alert_threshold:
                            play_mp3_file()
                            thread1=threading.Thread(target=self.send_email_alert,args=(class_label, id_text, filename))


                            thread1.start()

                            # Send a message alert
                            #self.send_message_alert(class_label, id_text, filename)
                            # Update the time of last sent message alert
                            self.alert_sent_time[class_label] = time.time()
                        
                    else:
                        save_folder = self.save_folder
                        # Generate a unique filename using the current timestamp and class label
                        filename = os.path.join(save_folder, f"{class_label.replace(' ', '_')}_{self.current_timestamp}.jpg")
                        cv2.imwrite(filename, image)

        # Check if the count of "No helmet" and "No vest" is 0
        if all(count == 0 for count in object_counts.values()):
            # Reset object_counts_temp and count_increased to 0
            self.object_counts_temp = {class_label: 0 for class_label in self.labels}
            self.count_increased = {class_label: False for class_label in self.labels}

        # Update object_counts_temp with the current counts
        self.object_counts_temp = object_counts.copy()

        # Draw the count of "No helmet" and "No vest" detections
        font_scale = 0.5
        text_color = (255, 165, 0)
        font_thickness = 2
        y_offset = 10

        for class_label, count in object_counts.items():
            cv2.putText(image, '{}: {}'.format(class_label, count), (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, font_thickness)
            y_offset += 20  # Decrease the y-offset between each line of text

        return image
    
    def send_email_alert(self, class_label, id_text, image_filename):
        pythoncom.CoInitialize()
        time.sleep(3)
        # Message content
        message = f'''Dear User,<br><br>
        <b>ALERT: {class_label} detected!</b><br><br>
        We would like to bring to your attention that during a recent safety compliance Check, it was noticed that a <b>Person ID: {id_text}</b> is found with <b>{class_label}</b> on the premises.</b><br>
        To ensure the safety and well-being of everyone, we kindly request you to take appropriate action and remind all personnel to strictly adhere to safety protocols.<br><br>
        Stay safe and secure.<br><br>
        Regards,<br>
        <u>Safety Compliance Monitoring Team</u>'''

        # Create an Outlook instance and send the email with the image attachment
        outlook = win32.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)
        mail.To = self.Mail_id
        mail.Subject = f"ALERT: {class_label} detected!"
        mail.HTMLBody = message
        
            # Get the absolute path for the image file
        image_filename = os.path.abspath(image_filename)

        # Debugging: Check if the image file exists
        if not os.path.exists(image_filename):
            print(f"Error: Image file '{image_filename}' does not exist.")
            return

        # Attach the image to the email
        mail.Attachments.Add(Source=image_filename)


        mail.Send()
        print("Message alert sent successfully!")
        pythoncom.CoUninitialize()

def play_mp3_file():
    
    mixer.init()
    mixer.music.load("./VOICE_Alert.mp3")
    mixer.music.play(0)
    
def stop_mp3_file():
    mixer.music.stop()


