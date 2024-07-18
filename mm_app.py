import pandas as pd
import os
import io
from google.colab import userdata
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import streamlit as st
from dotenv import find_dotenv, load_dotenv
from PIL import Image as PILImage
import weaviate
from weaviate.auth import AuthApiKey
from weaviate.classes.config import Property, DataType, Configure, Multi2VecField
from io import BytesIO
import base64
import requests
from weaviate.classes.query import Filter
from weaviate.classes.query import HybridFusion

# Load environment variables from .env file
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Retrieve the Studio API key from environment variables
studio_key = os.environ["STUDIO_APIKEY"]
 
# Path to the Google Vertex AI credentials JSON file
key_path = "mm-rag-recommender-05d612029f32.json"

# Function to obtain Google Vertex AI credentials
def get_credentials() -> Credentials:
    credentials = Credentials.from_service_account_file(
        key_path,
        scopes=[
            "https://www.googleapis.com/auth/generative-language",
            "https://www.googleapis.com/auth/cloud-platform",
        ],
    )
    request = Request()
    credentials.refresh(request)
    return credentials

# Initialize credentials and get the access token
credentials = get_credentials()
token = credentials.token

# Connect to the Weaviate client using the provided credentials
client = weaviate.connect_to_wcs(
    cluster_url = os.environ["WCS_URL"],                       # `weaviate_url`: your Weaviate URL
    auth_credentials = AuthApiKey(os.environ["WCS_API_KEY"]),      # `weaviate_key`: your Weaviate API key
    headers={
        "X-Google-Vertex-Api-Key": token,
        "X-Google-Studio-Api-Key": studio_key,
    }
)

# Connect to a specific Weaviate collection
fashion_collection = client.collections.get("FashionCollection")

# Function to save the uploaded image to the Assets folder
def saveImage(image, file_name):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()

    # Define the directory and file path
    directory = "/content/Assets"
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, file_name)

    # Write the uploaded file to the Assets Folder
    with open(file_path, 'wb') as f:
        f.write(img_byte_arr)

    reference_url = os.path.join(directory, file_name)
    return reference_url

# Function to convert media query into a base64 string
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode('utf-8')

# Function to get recommendations from image query
def get_image_recommendations(reference_image_url, gender, clothing_types):
    query_b64 = image_to_base64(reference_image_url)

    # Create a Filters object
    filters = (
        Filter.by_property("gender").contains_any(gender) 
        & Filter.by_property("subCategory").contains_any(clothing_types)
    )

    response = fashion_collection.query.near_image(
    near_image=query_b64,
    filters=filters,
    limit=3)

    for obj in response.objects:
        st.write(obj.properties["productDisplayName"])
        img = PILImage.open(BytesIO(requests.get((obj.properties['link'])).content))
        img = img.resize((500, 500))
        st.image(img)

# Function to get recommendations from text query
def get_text_recommendations(query, gender, clothing_types):
    # Create a Filters object
    filters = (
        Filter.by_property("gender").contains_any(gender) 
        & Filter.by_property("subCategory").contains_any(clothing_types)
    )
    
    response = fashion_collection.query.hybrid(
        query=query,
        filters=filters,  # Pass the Filters object
        fusion_type=HybridFusion.RANKED,
        alpha=0.75, #default value
        limit=3
    )

    for obj in response.objects:
        st.write(obj.properties["productDisplayName"])
        # st.write(obj.properties["subCategory"])
        img = PILImage.open(BytesIO(requests.get((obj.properties['link'])).content))
        img = img.resize((500, 500))
        st.image(img)

# Function to deploy app
def main():
  # Streamlit UI
  st.set_page_config(page_title="Fashion Finder", page_icon="🛍️", layout="wide")

  # Custom CSS for better UI
  st.markdown("""
      <style>
      .stButton button {
          background-color: #4CAF50; /* Green */
          border: none;
          color: white;
          padding: 15px 32px;
          text-align: center;
          text-decoration: none;
          display: inline-block;
          font-size: 16px;
          margin: 4px 2px;
          transition-duration: 0.4s;
          cursor: pointer;
      }

      .stButton button:hover {
          background-color: white;
          color: black;
          border: 2px solid #4CAF50;
      }

      .stRadio > div {
          display: flex;
          justify-content: center;
      }

      .stTextInput > div > div {
          display: flex;
          justify-content: center;
      }

      .stFileUploader > div {
          display: flex;
          justify-content: center;
      }

      .stImage > div {
          display: flex;
          justify-content: center;
      }
      </style>
  """, unsafe_allow_html=True)

  # Page title and description
  st.title("👜👔🛍️ Find your next outfit...")
  st.write("Get recommendations by either uploading an image of an outfit or a piece of clothing, or typing a text query.")

  # Add Filters
  # Add Clothing Filters header
  with st.sidebar:
      st.image('/content/Logo.png')
      st.header("Apparel Filters")

      # Gender selection
      gender_option = st.radio("Select a Gender:",("Women", "Men", "I'm gender agnostic/ non-confirming"))
      if gender_option == "I'm gender agnostic/ non-confirming":
        gender = ['Men', 'Women']
      else:
        gender = [gender_option]

      # Clothing type selection
      categories = ['Topwear', 'Bottomwear', 'Shoes', 'Watches', 'Bags']
      clothing_options = st.multiselect(
          "Select Types of Apparel:",
          categories,
          categories)
      if clothing_options:
        clothing_types = clothing_options
      else:
        st.error("Please select atleast one apparel category.")

  
  # Radio buttons for input method selection
  input_option = st.radio("Choose input method:", ["Upload an Image", "Type a Text Query"])

  if input_option == "Upload an Image":
    # Drag and drop file uploader
    uploaded_file = st.file_uploader("Upload any outfit or piece of clothing...", type=["jpg", "png", "jpeg"])

    # Display uploaded file
    if uploaded_file is not None:
        file_name = uploaded_file.name
        image = PILImage.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Button to trigger embedding and search
        if st.button('Recommend Products'):
            with st.spinner('Finding similar products...'):
                reference_image_url = saveImage(image, file_name)
                get_image_recommendations(reference_image_url, gender, clothing_types)

  elif input_option == "Type a Text Query":        
    user_input = st.text_input("Type your product query:")
    # Button to trigger embedding and search
    if st.button('Recommend Products'):
        with st.spinner('Finding similar products...'):
            if user_input:
                get_text_recommendations(user_input, gender, clothing_types)
            else:
                st.error("Please enter a query to get recommendations.")
                  
if __name__ == "__main__":
    main()
