from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_input,prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response =model.generate_content([input,pdf_input[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        #convert the pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        #convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]

        return pdf_parts    
    else:
        raise FileNotFoundError("No file uploaded")
    
## streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF) ",type=["pdf"])
if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell me about my resume")
submit2 = st.button("How can I improve my skills")
#submit3 = st.button("What are the keywords that are missing")
submit3 = st.button("Percentage match")

input_prompt1 = """
You are an experienced HR professional with technical expertise in Data Science recruitment. 
Your task is to evaluate resumes for profiles such as Full-Stack Web Development, Big Data Engineering, DevOps, and Data Analysis. 
Please provide a comprehensive evaluation of how well the candidates qualifications, skills, and experience align with the job description. 
Highlight key strengths, weaknesses, and areas of improvement for the applicant concerning the specified role.
"""
input_prompt2 = """
You are a Technical Human Resource Manager specializing in data science and related fields. 
Your role is to analyze the provided resume against the job description and assess the candidate's suitability for the role. 
Your task is to evaluate resumes for profiles such as Full-Stack Web Development, Big Data Engineering, DevOps, and Data Analysis. 
Please include insights on the candidates strengths, areas for development, and any gaps in their profile. 
Additionally, suggest actionable steps for the candidate to enhance their skills and improve alignment with the role.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) simulator with expertise in evaluating resumes for roles in Data Science, Web Development, Big Data Engineering, DevOps, and Data Analysis. 
Your task is to assess the provided resume against the job description, calculating the percentage match between the two. 
Additionally, identify missing keywords or skills in the resume that are critical for the role. 
Provide your output in the following format:
1. Percentage match: [e.g., 85%]
2. Missing keywords: [list the keywords or skills]
3. Suggestions for improvement: [actionable recommendations for the candidate to enhance their resume alignment with the job description]
"""
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")


elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")


