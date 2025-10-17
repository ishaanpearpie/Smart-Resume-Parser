# Smart Resume Screener

An AI-powered resume screening application that intelligently ranks candidates based on job descriptions using Google's Gemini API. The application features a clean, minimal UI and supports PDF, DOCX, and TXT file formats.

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/ishaanpearpie/Smart-Resume-Parser)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.13+-green)](https://python.org/)
[![React](https://img.shields.io/badge/React-18+-blue)](https://reactjs.org/)

## 🚀 Features

- **Clean, Minimal UI**: Intuitive interface with drag-and-drop file upload
- **AI-Powered Analysis**: Uses Google Gemini API for intelligent resume scoring
- **Multiple File Formats**: Supports PDF, DOCX, and TXT files
- **Database Storage**: SQLite database to store all analysis results
- **Real-time Results**: Clean, human-readable output with scores and justifications
- **File Validation**: Automatic file type and size validation
- **Docker Support**: Easy deployment with Docker and Docker Compose
- **Responsive Design**: Works on desktop and mobile devices

## 🏗️ Architecture

The Smart Resume Screener follows a modern microservices architecture with the following components:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   External      │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   Services      │
│                 │    │                 │    │                 │
│ • File Upload   │    │ • File Parsing  │    │ • Gemini API    │
│ • UI/UX         │    │ • AI Analysis   │    │ • Google AI     │
│ • Results Display│   │ • Database      │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│   Nginx         │    │   SQLite        │
│   (Production)  │    │   Database      │
└─────────────────┘    └─────────────────┘
```

### Component Details

- **Frontend (React)**: Clean, responsive UI with drag-and-drop file upload
- **Backend (FastAPI)**: RESTful API with file parsing and AI integration
- **Database (SQLite)**: Lightweight storage for analysis results
- **AI Service (Gemini)**: Google's advanced language model for resume analysis
- **Docker**: Containerized deployment for easy setup and scaling

## 🚀 Quick Start

### Option 1: Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ishaanpearpie/Smart-Resume-Parser.git
   cd Smart-Resume-Parser
   ```

2. **Set up environment variables:**
   ```bash
   cp backend/env.example .env
   # Edit .env and add your Google Gemini API key
   ```

3. **Run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Option 2: Manual Setup (Linux - Arch-based)

These instructions are for Arch Linux and its derivatives (like Manjaro, EndeavourOS, etc.).

#### 1. System Dependencies

```bash
sudo pacman -S python-pip python nodejs npm
```

#### 2. Backend Setup

```bash
cd Smart-Resume-Parser
python -m venv venv
source venv/bin/activate
cd backend
pip install -r requirements.txt
cp env.example .env
# Edit .env with your Google Gemini API key
```

#### 3. Frontend Setup

```bash
cd ../frontend
npm install
```

#### 4. Running the Application

**Terminal 1 (Backend):**
```bash
cd backend
uvicorn main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm start
```

Access at http://localhost:3000

## 🤖 AI Integration & LLM Prompts

### Google Gemini API Integration

The application uses Google's Gemini 2.0 Flash model for intelligent resume analysis. The AI is prompted to act as an expert HR recruitment assistant and provides structured JSON responses.

### Core LLM Prompt

```text
You are an expert HR recruitment assistant. Compare the resume text with the job description.

You MUST return your answer in a single, minified JSON object. Do not use markdown. The JSON object must have exactly two keys:
1. "score": a number from 1 to 10
2. "justification": a concise 2-3 sentence justification for the score

Job Description:
---
[Job description text]
---

Resume Text:
---
[Resume text content]
---

JSON Output:
```

### Prompt Engineering Features

- **Structured Output**: Forces JSON response for reliable parsing
- **Scoring System**: 1-10 scale for easy comparison
- **Justification**: Provides reasoning for transparency
- **Context-Aware**: Compares specific job requirements with resume content
- **Concise**: 2-3 sentence explanations for readability

### AI Analysis Process

1. **Text Extraction**: Parse uploaded files (PDF/DOCX/TXT)
2. **Prompt Construction**: Build structured prompt with job description and resume
3. **API Call**: Send to Gemini 2.0 Flash model
4. **Response Processing**: Parse JSON and handle markdown formatting
5. **Storage**: Save results to SQLite database
6. **Display**: Present clean results to user

## 📁 Project Structure

```
Smart-Resume-Parser/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile          # Backend container
│   ├── env.example         # Environment variables template
│   └── analysis_results.db # SQLite database (auto-created)
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js          # Main React component
│   │   ├── App.css         # Styling
│   │   ├── index.js        # React entry point
│   │   └── index.css       # Global styles
│   ├── package.json        # Node.js dependencies
│   ├── Dockerfile          # Frontend container
│   └── nginx.conf          # Nginx configuration
├── docker-compose.yml      # Docker orchestration
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🔧 API Endpoints

### POST /analyze
Analyze resumes against a job description.

**Request:**
- `job_description` (form field): Job description text
- `files` (form field): Resume files (PDF, DOCX, TXT)

**Response:**
```json
{
  "results": [
    {
      "filename": "resume.pdf",
      "score": 8,
      "justification": "Strong match with required skills and experience."
    }
  ]
}
```

### GET /
Health check endpoint.

**Response:**
```json
{
  "message": "Smart Resume Screener API is running"
}
```

## 🗄️ Database Schema

```sql
CREATE TABLE resume_analyses (
    id INTEGER PRIMARY KEY,
    filename VARCHAR,
    job_description TEXT,
    score INTEGER,
    justification TEXT,
    created_at DATETIME
);
```

## 🐳 Docker Deployment

### Development
```bash
docker-compose up --build
```

### Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables
- `GOOGLE_API_KEY`: Your Google Gemini API key (required)

## 🧪 Testing

### Backend Testing
```bash
cd backend
python test_setup.py
```

### Manual Testing
1. Upload a PDF/DOCX/TXT resume
2. Enter a job description
3. Click "Analyze & Rank Candidates"
4. Review the AI-generated scores and justifications

## 🛠️ Development

### Backend Development
- FastAPI with automatic API documentation at `/docs`
- SQLAlchemy ORM for database operations
- PyPDF2 for PDF parsing
- python-docx for DOCX parsing

### Frontend Development
- React 18 with functional components
- react-dropzone for file uploads
- Responsive CSS with modern design
- Real-time state management

### Code Quality
- Comprehensive comments throughout
- Type hints in Python
- Error handling and validation
- Clean, readable code structure

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the API documentation at `/docs`
- Review the troubleshooting section below

## 🔍 Troubleshooting

### Common Issues

1. **PDF parsing errors**: Ensure all dependencies are installed
2. **CORS errors**: Check that backend is running on correct port
3. **API key errors**: Verify your `.env` file contains the correct `GOOGLE_API_KEY`
4. **File upload errors**: Check file format and size limits

### Logs

- Backend logs: Check terminal where you ran the backend
- Frontend logs: Check browser console (F12)
- Docker logs: `docker-compose logs [service_name]`

## 🎯 Future Enhancements

- [ ] Support for more file formats (RTF, ODT)
- [ ] Batch processing capabilities
- [ ] Advanced filtering and sorting
- [ ] Export results to CSV/PDF
- [ ] User authentication and profiles
- [ ] Multi-language support
- [ ] Advanced AI models integration