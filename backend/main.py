"""
Smart Resume Screener Backend API

This FastAPI application provides AI-powered resume analysis using Google's Gemini API.
It supports PDF, DOCX, and TXT file formats and stores analysis results in SQLite.

Author: Ishaan Pearpie
Repository: https://github.com/ishaanpearpie/Smart-Resume-Parser
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
import json
import PyPDF2
from docx import Document
import google.generativeai as genai
from dotenv import load_dotenv
from typing import List
import io

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI application with metadata
app = FastAPI(
    title="Smart Resume Screener API",
    description="AI-powered resume analysis and ranking system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:80"],  # Include Docker frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./analysis_results.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database model for storing resume analysis results
class ResumeAnalysis(Base):
    """
    SQLAlchemy model for storing resume analysis results.
    
    Fields:
        id: Primary key (auto-increment)
        filename: Name of the uploaded resume file
        job_description: The job description used for analysis
        score: AI-generated score (1-10)
        justification: AI-generated explanation for the score
        created_at: Timestamp when the analysis was performed
    """
    __tablename__ = "resume_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    job_description = Column(Text)
    score = Column(Integer)
    justification = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create database tables on startup
Base.metadata.create_all(bind=engine)

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def parse_resume_file(file: UploadFile) -> str:
    """
    Parse uploaded resume file and extract text content.
    
    Supports multiple file formats:
    - PDF: Uses PyPDF2 library
    - DOCX: Uses python-docx library  
    - TXT: Direct text reading
    
    Args:
        file (UploadFile): The uploaded file from FastAPI
        
    Returns:
        str: Extracted text content from the file
        
    Raises:
        HTTPException: If file type is not supported
    """
    # Read file content into memory
    content = file.file.read()
    file.file.seek(0)  # Reset file pointer for potential reuse
    
    if file.filename.endswith('.pdf'):
        # Parse PDF files using PyPDF2
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    elif file.filename.endswith('.docx'):
        # Parse DOCX files using python-docx
        doc = Document(io.BytesIO(content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    elif file.filename.endswith('.txt'):
        # Parse plain text files
        return content.decode('utf-8')
    
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.filename}")

def get_analysis(resume_text: str, jd_text: str) -> dict:
    """
    Analyze resume against job description using Google Gemini API.
    
    This function sends a structured prompt to Gemini AI to get a scored analysis
    of how well a resume matches a job description.
    
    Args:
        resume_text (str): Extracted text content from the resume
        jd_text (str): Job description text
        
    Returns:
        dict: Analysis result with 'score' (1-10) and 'justification' fields
        
    Raises:
        HTTPException: If API call fails or returns invalid response
    """
    # Initialize Gemini model (using the latest stable version)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Construct structured prompt for consistent AI responses
    prompt = f"""You are an expert HR recruitment assistant. Compare the resume text with the job description.

You MUST return your answer in a single, minified JSON object. Do not use markdown. The JSON object must have exactly two keys:
1. "score": a number from 1 to 10
2. "justification": a concise 2-3 sentence justification for the score

Job Description:
---
{jd_text}
---

Resume Text:
---
{resume_text}
---

JSON Output:"""
    
    try:
        response = model.generate_content(prompt)
        print(f"Gemini response: {response.text}")
        print(f"Response length: {len(response.text) if response.text else 0}")
        
        if not response.text or response.text.strip() == "":
            raise HTTPException(status_code=500, detail="Empty response from Gemini API")
        
        # Parse the JSON response - handle markdown code blocks
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith('```json'):
            response_text = response_text[7:]  # Remove ```json
        if response_text.startswith('```'):
            response_text = response_text[3:]   # Remove ```
        if response_text.endswith('```'):
            response_text = response_text[:-3]  # Remove trailing ```
        
        response_text = response_text.strip()
        print(f"Cleaned response: {response_text}")
        
        result = json.loads(response_text)
        return result
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Response text: '{response.text}'")
        raise HTTPException(status_code=500, detail=f"Invalid JSON response from Gemini: {str(e)}") from e
    except Exception as e:
        print(f"Gemini API error: {e}")
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}") from e

@app.post("/analyze")
async def analyze_resumes(
    job_description: str = Form(...),
    files: List[UploadFile] = File(...)
):
    """
    Main API endpoint for analyzing resumes against a job description.
    
    This endpoint:
    1. Validates uploaded files (PDF, DOCX, TXT only)
    2. Parses each file to extract text content
    3. Sends resume text and job description to Gemini AI for analysis
    4. Stores results in SQLite database
    5. Returns analysis results to frontend
    
    Args:
        job_description (str): The job description text (from form data)
        files (List[UploadFile]): List of uploaded resume files
        
    Returns:
        dict: JSON response containing analysis results for each file
        
    Raises:
        HTTPException: For various validation and processing errors
    """
    # Log request details for debugging
    print(f"Received request with {len(files)} files")
    print(f"Job description length: {len(job_description)}")
    
    # Validate that files were uploaded
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    
    # Enforce file limit to prevent abuse
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 files allowed")
    
    # Validate file types - only allow supported formats
    allowed_extensions = ['.pdf', '.docx', '.txt']
    for file in files:
        if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.filename}")
    
    # Initialize database session
    db = SessionLocal()
    results = []
    
    try:
        # Process each uploaded file
        for file in files:
            # Extract text content from the file
            resume_text = parse_resume_file(file)
            
            # Get AI analysis from Gemini API
            analysis = get_analysis(resume_text, job_description)
            
            # Save analysis result to database
            db_analysis = ResumeAnalysis(
                filename=file.filename,
                job_description=job_description,
                score=analysis['score'],
                justification=analysis['justification']
            )
            db.add(db_analysis)
            db.commit()
            
            # Add result to response list
            results.append({
                "filename": file.filename,
                "score": analysis['score'],
                "justification": analysis['justification']
            })
        
        return {"results": results}
    
    except Exception as e:
        # Rollback database transaction on error
        db.rollback()
        print(f"Error processing files: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing files: {str(e)}") from e
    
    finally:
        # Always close database connection
        db.close()

@app.get("/")
async def root():
    return {"message": "Smart Resume Screener API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
