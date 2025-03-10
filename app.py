from dotenv import load_dotenv
import streamlit as st
import os
import io
import base64
import pdfplumber  # Alternative to pdf2image
import google.generativeai as genai

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Check if API key is set
if not GOOGLE_API_KEY:
    st.error("❌ Google API key not found. Please set it in the environment variables.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text if text else "No text found in the PDF."
    except Exception as e:
        st.error(f"❌ Error processing PDF: {str(e)}")
        return None

# Function to get AI response
def get_gemini_response(input_prompt, resume_text):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content([input_prompt, resume_text])
        return response.text
    except Exception as e:
        return f"❌ Error generating response: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="ATS Resume Checker")
st.title("📄 ATS Resume Fit Checker")
st.write("Upload your resume and compare it with a job description to analyze fit.")

input_text = st.text_area("📌 Paste Job Description:", key="job_desc")
uploaded_file = st.file_uploader("📂 Upload your Resume (PDF only)", type=['pdf'])

if uploaded_file is not None:
    st.success("✅ Resume uploaded successfully")

# Define Prompts
input_prompts = {
    "submit1": "Analyze this resume and provide a summary of the candidate's qualifications for the given job description.",
    "submit2": "Suggest improvements to align the resume with the job description.",
    "submit3": "List missing keywords in this resume compared to the job description.",
    "submit4": "Provide a percentage match score between the resume and job description."
}

# Buttons
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    submit1 = st.button("📌 Resume Summary")
with col2:
    submit2 = st.button("📈 Improvement Suggestions")
with col3:
    submit3 = st.button("🔑 Missing Keywords")
with col4:
    submit4 = st.button("📊 Match Percentage")

# Handle Button Clicks
if any([submit1, submit2, submit3, submit4]):
    if uploaded_file and input_text:
        resume_text = extract_text_from_pdf(uploaded_file)
        if resume_text:
            selected_prompt = input_prompts["submit1"] if submit1 else \
                              input_prompts["submit2"] if submit2 else \
                              input_prompts["submit3"] if submit3 else \
                              input_prompts["submit4"]

            response = get_gemini_response(selected_prompt, resume_text)
            st.subheader("📌 AI Response:")
            st.write(response)
    else:
        st.warning("⚠️ Please upload a resume and provide a job description.")


