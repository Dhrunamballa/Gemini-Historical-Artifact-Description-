import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("your api key")

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Artifact AI Analyzer", layout="centered")

st.title("🏛️ Artifact AI Analyzer")
st.write("Upload an artifact image and generate AI-based analysis.")

# Image upload (UI purpose)
image_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if image_file:
    st.image(image_file, caption="Uploaded Image", width="stretch")

# Prompt input
prompt = st.text_area(
    "Enter your prompt",
    placeholder="Example: Analyze this bronze statue from ancient India."
)

if st.button("Generate Description"):
    if prompt:
        with st.spinner("Generating response..."):
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert historian. When given a prompt about an artifact, provide a detailed analysis including possible origin, era, material, cultural significance, and historical context."
                    },
                    {
                        "role": "user",
                        "content": f"Artifact Analysis Request: {prompt}"
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )

            result = completion.choices[0].message.content

        st.success("Analysis Complete ✅")
        st.write(result)

        st.download_button(
            "Download Report",
            result,
            file_name="artifact_analysis.txt"
        )

    else:
        st.warning("Please enter a prompt.")
