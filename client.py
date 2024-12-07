import streamlit as st
import requests
import base64


def detect(data):
    url = 'http://localhost:3000/render'
    image_base64 = base64.b64encode(data)
    response = requests.post(
        url=url,
        json={
            'image_base64': image_base64.decode('utf-8')
        }
    )
    if response.status_code == 200:
        st.image(base64.b64decode(response.content))


def run():
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        data = uploaded_file.getvalue()
        st.image(data)
        st.button(
            label="Detect",
            on_click=detect,
            args=[data]
        )


if __name__ == "__main__":
    run()
