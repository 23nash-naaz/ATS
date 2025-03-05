from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import io
import base64
from PIL import Image
from pdf2image import convert_from_bytes
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-2.0-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    images=convert_from_bytes(uploaded_file.read(),poppler_path=r'C:\Program Files\poppler\Library\bin')

    first_page=images[0]

    img_byte_arr=io.BytesIO()
    first_page.save(img_byte_arr,format='JPEG')
    img_byte_arr=img_byte_arr.getvalue()

    pdf_parts=[
        {
            "mime_type":"image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
        }
    ]
    return pdf_parts


st.set_page_config(page_title="ATS Resume expert")
st.header("ATS TRACKER")
input_text=st.text_area("Job Description:", key="input")
uploaded_file=st.file_uploader("Upload your resume",type=['pdf'])

if uploaded_file is not None:
    st.write("Resume uploaded successfully")

submit1=st.button("Tell me about the resume")
submit2=st.button("How can i improve my skills")
submit3=st.button("What are the keywords that are missing")
submit4=st.button("Percentage match")
input_prompt1="""
The resume is a good fit for the job. It has the required skills and experience.
You are an experienced ML developer so select profiles with a strong ML and give description about their projects.
"""
input_prompt2="""To meet the resume ceiling you can improve ML fundamentals and deep learning concepts.
"""

input_prompt3="""
ML engineer
Data scientist
Deep learning engineer

"""

input_prompt4="""You are a ATS scanner and you are looking for a resume that has a 90% match with the job description.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_prompt1)
        st.subheader("The response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")
elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_prompt2)
        st.subheader("The response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")
elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_prompt3)
        st.subheader("The response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")
elif submit4:   
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt4,pdf_content,input_prompt4)
        st.subheader("The response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")
