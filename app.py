import streamlit as st
import os
import PyPDF2 as pdf
from mistralai import Mistral
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Mistral client
api_key = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=api_key)

# Function to extract text from uploaded PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Function to get response from Mistral API
def get_mistral_response(input_prompt):
    response = client.chat.complete(
        model="mistral-large-latest",  # or "mistral-small-latest"
        messages=[
            {"role": "system", "content": "You are a skilled ATS (Applicant Tracking System) specialized in tech jobs."},
            {"role": "user", "content": input_prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# Prompt template
input_prompt_template = """
Hey, act like a skilled or very experienced ATS (Applicant Tracking System)
with a deep understanding of the tech field, software engineering, data science, data analysis,
and big data engineering. Your task is to evaluate the resume based on the given job description.
You must consider that the job market is very competitive, and you should provide 
the best assistance for improving the resume. Assign the percentage match based 
on the job description and
list the missing keywords with high accuracy.
resume: {text}
description: {jd}

I want the response in a single string structured as follows:
{{"JD Match": "X%", "MissingKeywords": ["keyword1", "keyword2"], "Profile Summary": "summary text"}}
"""

# Streamlit UI
st.title("Smart ATS (Powered by Mistral)")
st.text("Improve Your Resume for ATS")

jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload a PDF")

if st.button("Submit"):
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        input_prompt = input_prompt_template.format(text=text, jd=jd)
        response = get_mistral_response(input_prompt)
        st.subheader("ATS Evaluation")
        st.text_area("Response", value=response, height=250)
    else:
        st.warning("Please upload your resume first.")
