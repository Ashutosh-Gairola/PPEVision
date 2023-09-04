import streamlit as st

# Custom CSS to add a border around the title
title_style = """
    <style>
    .title-border {
        border: 2px solid #555555;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #008080;
        text-decoration: underline;
    }
    .subtitle {
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: #333333;
        margin-top: 20px;
    }
    .info-text {
        font-size: 18px;
        color: #444444;
        margin-top: 10px;
    }
    .link {
        font-size: 18px;
        color: #008080;
        font-weight: bold;
        text-decoration: none;
    }
    .link:hover {
        color: #006666;
        text-decoration: underline;
    }
    .content-box {
        background-color: #f2f2f2;
        border-radius: 10px;
        padding: 20px;
        margin-top: 30px;
    }
    .options-heading {
        font-weight: bold;
        text-decoration: underline;
    }
    </style>
"""


st.set_page_config(page_title="Home Page",
                   layout='wide',
                   page_icon="./Images/homeicon.jpg")

# Inject the custom CSS into the Streamlit app
st.markdown(title_style, unsafe_allow_html=True)

# Title with border
st.markdown('<div class="title-border">PPE DETECTION</div>', unsafe_allow_html=True)

# Subtitle
st.markdown('<div class="subtitle">Detect wheather person is  wearing a Safety Helmet & vest</div>', unsafe_allow_html=True)

# Create two columns for layout
col1, col2 = st.columns([2, 1])

# Left column (text)
# Content section with improved styling
with col1:
    st.markdown("""
    <div class="content-box">
        <p><strong><u>PPE Detection App</u></strong></p>
        <p>This app can automatically detect whether a person is wearing a Safety Helmet & vest or not.</p>
        <p>You can upload photos or videos for detection.</p>
        <p><strong class="options-heading"><u>Things which can be detected</u></strong></p>
        <ul>
            <li>Helmet</li>
            <li>No Helmet</li>
            <li>Reflective vest</li>
            <li>No vest</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Right column (GIF)
with col2:
    # You can use the 'image' element with the GIF URL or local file path
    st.image("./Images/Safety.gif", use_column_width=True)

# Footer
st.markdown("---")
st.markdown("<div class='info-text'>Created by Ashutosh Gairola</div>", unsafe_allow_html=True)
