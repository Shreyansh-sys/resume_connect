# Lessume

Lessume takes a PDF file of the users resume and interprets the text. It then organizes the information in a database with which companies and recruiters can use to search for the right applicants.

Lessume is a web application built using Streamlit that allows candidates to submit resumes and answer questions. It uses MongoDB to store resume and form data, and OpenAI GPT models to analyze and generate insights from resumes. 
Recruiters can search through the database of resumes using semantic search powered by OpenAI embeddings.

## Features

- **Resume Upload**: Candidates can upload PDF resumes.
- **Form Submission**: Candidates answer multiple questions about job preferences, sponsorship, and personal details.
- **OpenAI GPT Analysis**: The application uses OpenAI to analyze resumes and generate insights on key skills, qualifications, and technologies.
- **Embedding and Semantic Search**: Resumes and form answers are embedded using OpenAI embeddings, and recruiters can search resumes by entering a prompt, which returns the most relevant candidates.
- **MongoDB Storage**: All resumes, form answers, embeddings, and analyses are stored in MongoDB.
- **Search Resumes** : The recruiter can search for resumes based on sentence based prompt or job description

## Technologies Used

- **Frontend**: [Streamlit](https://streamlit.io/) for the user interface.
- **Backend**: 
  - [MongoDB](https://www.mongodb.com/) for database storage.
  - [OpenAI GPT-4](https://openai.com/) for resume analysis and embedding generation.
- **Python Libraries**:
  - `pymongo` for MongoDB integration.
  - `PyPDF2` for extracting text from PDFs.
  - `scikit-learn` for cosine similarity calculations.
  - `dotenv` for environment variable management.
  - `OpenAI` Python client for interacting with the GPT model.

## Setup Instructions

### Prerequisites

- Python 3.7+
- MongoDB Atlas account (or any MongoDB instance)
- OpenAI API Key (Get from [OpenAI])

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/hired-app.git
   cd hired-app

2. Create virtual environment
    ```
    python3 -m venv env
    ```
- Activate virtual environment
  bash:
  
  Linux
  ```
  source  env/bin/activate
  ```

  Powershell:

  ```
  .\env\Scripts\Activate
  ```

3. Install the dependencies

    ```
    pip3 install -r requirements.txt
    ```

  - Create .env

  ```
  touch .env
  ```
  Add the following to the .env file:
  ```
  OPENAI_KEY = "add key"
  OPENAI_PROMPT = "add prompt"
  MONGO_URI="mongodb+srv://<username>:<password>@cluster0.mongodb.net/hired_db?retryWrites=true&w=majority"
  ```

5. Run the Streamlit app:
  ```
  streamlit run app.py
  ```

## MongoDB Setup

  1. Create a MongoDB Atlas account at MongoDB Atlas.
  2.  Set up a new cluster and create a database (e.g., hired_db).
  3.  Whitelist IP addresses to allow access (use 0.0.0.0/0 to allow all for development).
  4.  Create a database user with a username and password.
  5.  Replace `<username>`, `<password>`, and `hired_db` in the MONGO_URI in your .env file with your MongoDB credentials.

## Usage
### Candidate View

  - Submit Resume: Upload a resume in PDF format.
  - Answer Form Questions: Fill out questions related to sponsorship, job preferences, citizenship, and more.
  - Submit: The resume and form responses are analyzed and stored in the MongoDB database, along with an embedding for semantic search.

### Recruiter View
 
  - Search for Resumes: Recruiters can enter a search prompt (e.g., "Python developer with AI experience") and the app will return the most relevant candidates, based on their resume content and form responses.

## File Structure
```
├── app.py                   # Main application file
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (not included in repo)
├── README.md                 # This README file
└── utils                     # Utility functions (if applicable)
```

## Environment Variables

The app requires the following environment variables to function, stored securely in a .env file or in Streamlit's secrets management:

  - OPENAI_API_KEY: Your OpenAI API key.
  - MONGO_URI: MongoDB connection string to your database.
  - OPENAI_PROMPT: The prompt used to send to OpenAI for resume analysis.

## Deployment on Streamlit Cloud

  - Push your code to a GitHub repository.
  - Go to Streamlit Cloud and create a new app by connecting it to your GitHub repository.
  - Add your MongoDB and OpenAI API keys in Streamlit Cloud's Secrets management.
  - Deploy the app and share the link with users!

## Security Considerations

  - Make sure that your .env file or any sensitive information (API keys, MongoDB URIs) are not committed to the repository.
  - Use Streamlit Cloud Secrets to securely store environment variables when deploying the app.