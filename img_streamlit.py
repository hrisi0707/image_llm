# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st
from PIL import Image
#from openai import OpenAI
import base64
import requests
from io import BytesIO

api_key='your-api-key'
# Streamlit UI
st.title("Image Question and Answer App")

# Upload image
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

#st.chat_input(placeholder="Ask me a question!")
def call_gpt4(base64_image,prompt):
    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
    }
    payload = {
      "model": "gpt-4o",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": prompt
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 300
    }
#    print(payload)
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()
if uploaded_image is not None:
    image = Image.open(uploaded_image)
    buff = BytesIO()
    st.image(image, caption='This is your image:')
    image.save(buff, format="JPEG")
    base64_image = base64.b64encode(buff.getvalue()).decode('utf-8')
#    print("type upload image:",type(uploaded_image))
#    print("type image:",image)
#    with open(uploaded_image.read(), "rb") as f:
#        base64_image = base64.b64encode(f.read()).decode('utf-8')
#    print("BAse64Image:",base64_image)
    if prompt := st.chat_input(placeholder="Ask me a question!"):
        st.chat_message("user").write(prompt)
        json_response = call_gpt4(base64_image,prompt)
        st.write("Answer", json_response["choices"][0]["message"]["content"])
