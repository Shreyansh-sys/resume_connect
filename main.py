import streamlit as st
from pymongo import MongoClient
from PyPDF2 import PdfReader
from bson import Binary
from openai import OpenAI
import os
import dotenv
import hashlib
from streamlit.components.v1 import html


# html(
#     '<img src="dino.jpg" alt="Description of the image" />'
# )
import numpy as np
from bson import Binary
import re
from sklearn.metrics.pairwise import cosine_similarity

dotenv.load_dotenv()
# Set up OpenAI API key
openai_key = os.getenv("OPENAI_API_KEY")
openai_prompt = os.getenv("OPENAI_PROMPT")

# Connect to MongoDB
client = MongoClient('localhost:27017')  # Replace with your MongoDB connection string
db = client['hired_db']  # Database
collection = db['resumes']  # Collection

# Helper function to extract text from resume (PDF)
def extract_resume_text(uploaded_file):
    if uploaded_file is not None:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    return None

# Function for analyzing resume using OpenAI
def analyze_resume(resume_text):
    openai_client = OpenAI()
    if resume_text:
        cleaned_text = clean_resume_text(resume_text)
        prompt = openai_prompt.format(resume_text=cleaned_text)
        
        # Call the OpenAI API
        completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that analyzes resumes."},
            {
                "role": "user",
                "content": prompt
            }
        ]
        )
        # Extract the analysis from OpenAI's response
        return completion.choices[0].message.content, cleaned_text
    
    return "No resume text provided for analysis.", resume_text

# Function to encode text using OpenAI's embeddings API
def get_text_embedding(text):
    openai_client = OpenAI()
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

# Function to calculate hash of a file to detect changes
def hash_file(file):
    hasher = hashlib.md5()
    hasher.update(file.read())
    return hasher.hexdigest()

def clean_resume_text(resume_text):
    """
    Clean the given resume text by removing unnecessary characters and formatting.

    Parameters:
        resume_text (str): The original resume text.

    Returns:
        str: The cleaned resume text.
    """
    # Remove section headers (like ### 1. Key Skills)
    cleaned_text = re.sub(r'###?\s*\d*\.?\s*', '', resume_text)
    
    # Remove bullet points and asterisks
    cleaned_text = re.sub(r'-\s*|\*\*\s*|\*\s*', '', cleaned_text)
    
    # Remove any additional unwanted characters
    cleaned_text = re.sub(r'[\n]{2,}', '\n\n', cleaned_text)  # Reduce multiple newlines to a maximum of two
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # Remove excess whitespace
    cleaned_text = cleaned_text.strip()  # Remove leading and trailing whitespace
    
    return cleaned_text

# Streamlit UI
st.title('Hired Simple Version')

st.markdown("""
    <style>
    body {
        background-color: #1A0800;
        color: #E8E8E8;
    }
    .stAppHeader{
        background-color: #2BFF00
                }
    .st-emotion-cache-1r4qj8v{
        background-color: #1A0800;    
            }        
    .st-emotion-cache-ue6h4q {
        color: #2BFF00;
                    }
            .st-emotion-cache-12h5x7g.e1nzilvr5{
            color: white;}
    h1, h2, h3, h4, .st-emotion-cache-12h5x7g{
        color: #2BFF00;
    }
    .stTextInput, .stTextArea, .stFileUploader {
        background-color: #2C3E50;
        color: #ECF0F1;
        border: 1px solid #2BFF00;
        padding: 10px;
        border-radius: 5px;
    }
    .stButton button {
        background-color: #E74C3C;
        color: #FFF;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #C0392B;
    }
    .stRadio > div {
        color: #E8E8E8;
    }
            
    .stSidebar{
        background-color: #424242;
            }
    .sidebar .sidebar-content {
        background-color: #2BFF00;
        color: #ECF0F1;
    }
    .sidebar .sidebar-content .stRadio {
        color: #ECF0F1;
    }
    .stAlert {
        background-color: #27AE60;
        color: white;
    }
    .stTextInput > div, .stFileUploader > div {
        color: #FFF;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for selecting user type
user_type = st.sidebar.radio("Are you a:", ("Candidate", "Recruiter"))

### Candidate Session ###
if user_type == "Candidate":

    st.subheader('Submit your Resume and Answer Questions')

    # Candidate Info
    candidate_name = st.text_input('Name')
    candidate_email = st.text_input('Email')

    # Resume Upload
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

    # Use session state to store the analysis result so that it only happens once when the resume is uploaded
    if "analysis" not in st.session_state:
        st.session_state.analysis = None
        st.session_state.resume_hash = None
        st.session_state.cleaned_text = None 

    # If a resume is uploaded, calculate its hash
    if uploaded_file:
        current_resume_hash = hash_file(uploaded_file)

        # Reanalyze if the resume has changed
        if current_resume_hash != st.session_state.resume_hash:
            st.session_state.resume_hash = current_resume_hash  # Update hash in session state
            uploaded_file.seek(0)  # Reset file pointer after hashing
            resume_text = extract_resume_text(uploaded_file)
            
            if resume_text:
                analysis,cleaned_text = analyze_resume(resume_text)
                st.session_state.analysis = analysis
                st.session_state.cleaned_text = cleaned_text
        else:
            st.success("Resume unchanged, no re analysis needed.")

    # # Resume Analysis - only perform if it's the first time or the resume is re-uploaded
    # if uploaded_file and resume_text and st.session_state.analysis is None:
    #     analysis = analyze_resume(resume_text)
    #     st.session_state.analysis = analysis

    # Display the analysis in a non-editable text area
    if st.session_state.analysis:
        st.text_area("Resume Analysis", st.session_state.analysis, height=200, disabled=True)
        resume_embedding = get_text_embedding(st.session_state.cleaned_text)

    # Questions
    st.subheader("Please answer the following questions:")
    question1 = st.text_input("Do you require sponsorship to work in the US?")
    question2 = st.text_input("Are you currently in the USA")
    question3 = st.text_input("What is your expected salary range?")

    # Submit button
    if st.button('Submit'):
        if candidate_name and candidate_email and uploaded_file and question1 and question2 and question3:
            # Convert uploaded resume to binary
            resume_binary = Binary(uploaded_file.read())

            # Create document for MongoDB
            resume_data = {
                "candidate_name": candidate_name,
                "email": candidate_email,
                "resume": resume_binary,  # Store resume as binary
                "answers": {
                    "question1": question1,
                    "question2": question2,
                    "question3": question3
                },
                "embedding": resume_embedding,
                "cleaned_text": st.session_state.cleaned_text, 
                "analysis": st.session_state.analysis
            }

            # Insert into MongoDB
            collection.insert_one(resume_data)
            
            st.success("Your resume and answers have been submitted successfully!")
        else:
            st.error("Please fill in all the fields and upload a resume.")

### Recruiter Session ###
elif user_type == "Recruiter":
    st.header("Search for Resumes")

    # Search input
    search_term = st.text_input("Search by prompt")

    # Search button
    if st.button("Search"):
        if search_term:
            # Get embedding for the search term
            search_embedding = get_text_embedding(search_term)

            # Retrieve all resume embeddings from the database
            resumes = list(collection.find({}, {"candidate_name": 1, "email": 1, "resume_text": 1, "embedding": 1,"analysis": 1}))

            # Prepare the embeddings and calculate similarity
            if resumes:
                resume_embeddings = np.array([resume['embedding'] for resume in resumes])
                search_embedding = np.array([search_embedding])  # Convert to 2D array for cosine similarity

                # Step 3: Calculate cosine similarity between the search embedding and resume embeddings
                similarities = cosine_similarity(search_embedding, resume_embeddings)[0]
                
                # Sort by similarity
                similar_resumes = sorted(zip(resumes, similarities), key=lambda x: x[1], reverse=True)

                # Display top results
                st.write(f"Found {len(similar_resumes)} resumes:")
                for resume, similarity in similar_resumes[:5]:  # Show top 5 matches
                    st.subheader(f"Candidate: {resume['candidate_name']} (Similarity: {similarity:.2f})")
                    st.write(f"Email: {resume['email']}")
                    st.write(f"Resume Text: {resume['analysis'][:1000]}...")  # Show first 500 chars
                    st.write("---")
            else:
                st.write("No resumes found in the database.")
        else:
            st.error("Please enter a search term.")
