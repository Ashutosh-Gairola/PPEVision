
import os
import streamlit as st
from PIL import Image
import pandas as pd
from datetime import datetime
import io
import subprocess

st.set_page_config(layout="centered")

# Add CSS styles for the heading and the table
st.markdown(
    """
    <style>
    .heading-box {
        padding: 10px;
        background-color: #f0f0f0;
        border-radius: 5px;
        text-align: center;
    }
    .table {
        border-collapse: collapse;
    }
    .table th, .table td {
        padding: 8px;
        border: 1px solid #ddd;
        text-align: left;
    }
    .table th {
        background-color: #f2f2f2;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


#st.set_page_config(page_title="Log generate", layout="centered")

# Add the heading "Log generated" inside a box
st.markdown("<div class='heading-box'><h2>Log generated</h2></div>", unsafe_allow_html=True)

# Define the folder path where the images are stored
folder_path = './NON_APP/'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Get the list of image files in the folder
image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]

# Create a table with sno, name, date, time, and checkbox columns
table_data = []
for i, image_file in enumerate(image_files, start=1):
    file_name = os.path.splitext(image_file)[0]
    image_path = os.path.join(folder_path, image_file)
    creation_timestamp = os.path.getctime(image_path)
    creation_datetime = datetime.fromtimestamp(creation_timestamp)
    formatted_creation_date = creation_datetime.strftime("%d %B, %Y")
    formatted_creation_time = creation_datetime.strftime("%I:%M:%S %p")

    # Extract the appliance name from the file name
    appliance_name = file_name.split("_")[1]
    table_data.append([i, file_name, formatted_creation_date, formatted_creation_time, appliance_name, False])

# Create a DataFrame with the table data
df = pd.DataFrame(table_data, columns=["sno", "name", "date", "time", "compliance Not available", "checkbox"])
# df=df.set_index("sno")

# Display the table
edited_df = st.data_editor(df)

col1,col2,col3=st.columns(3)

# Add a "CSV_Download" button
if col1.button("CSV_Download"):
    # Create a new DataFrame with selected columns
    selected_df = edited_df[["sno", "name", "date", "time", "compliance Not available"]]

    # Add the "Image path" column
    selected_df["Image path"] = folder_path + selected_df["name"] + ".jpg"
                                #[os.path.join(folder_path, f"{row['name']}.jpg") for _, row in selected_df.iterrows()]
    # Convert the DataFrame to CSV content as a string
    csv_string = selected_df.to_csv(index=False)

    # Create a BytesIO object to hold the CSV data
    csv_bytes = io.BytesIO(csv_string.encode())

    # Create a download button to download the CSV file
    st.download_button(
        label="Download CSV",
        data=csv_bytes,
        file_name="selected_images.csv",
        mime="text/csv"
    )

# Add a button to open the folder where images are saved
if col2.button("Open Folder"):
    try:
        # Replace 'explorer' with 'nautilus' for Linux or 'open' for macOS.
        subprocess.Popen(["explorer", os.path.abspath(folder_path)])
    except Exception as e:
        st.error(f"Error opening folder: {e}")

# Get the selected rows where the checkbox is checked
selected_rows = edited_df[edited_df["checkbox"] == True]

# Display the selected images when the checkbox is clicked
if selected_rows.shape[0] > 0:
    for index, row in selected_rows.iterrows():
        image_file = f"{row['name']}.jpg"  # Assuming the images have a .jpg extension
        image_path = os.path.join(folder_path, image_file)
        if os.path.exists(image_path):
            image = Image.open(image_path)
            st.image(image, caption=row['name'])
        else:
            st.write(f"Image not found: {image_file}")

