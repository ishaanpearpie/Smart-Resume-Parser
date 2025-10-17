/**
 * Smart Resume Screener Frontend
 * 
 * A React application that provides a clean, minimal UI for uploading resumes
 * and job descriptions to get AI-powered analysis and ranking.
 * 
 * Features:
 * - Drag-and-drop file upload for PDF, DOCX, and TXT files
 * - Job description input with example text
 * - Real-time analysis results with scores and justifications
 * - Responsive design matching the provided UI mockup
 * 
 * Author: Ishaan Pearpie
 * Repository: https://github.com/ishaanpearpie/Smart-Resume-Parser
 */

import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import './App.css';

function App() {
  // State management for the application
  const [jobDescription, setJobDescription] = useState('');        // Job description text
  const [resumeFiles, setResumeFiles] = useState([]);             // Uploaded resume files
  const [analysisResults, setAnalysisResults] = useState([]);     // Analysis results from API
  const [isAnalyzing, setIsAnalyzing] = useState(false);          // Loading state

  /**
   * Handle file drop/selection for resume uploads
   * Filters files to only allow supported formats (PDF, DOCX, TXT)
   * 
   * @param {Array} acceptedFiles - Files accepted by react-dropzone
   */
  const onDrop = (acceptedFiles) => {
    // Filter files to only allow PDF, DOCX, and TXT
    const validFiles = acceptedFiles.filter(file => {
      const extension = file.name.toLowerCase().split('.').pop();
      return ['pdf', 'docx', 'txt'].includes(extension);
    });
    
    // Show warning if some files were rejected
    if (validFiles.length !== acceptedFiles.length) {
      alert('Only PDF, DOCX, and TXT files are allowed');
    }
    
    setResumeFiles(validFiles);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    maxFiles: 10
  });

  /**
   * Handle the analysis request to the backend API
   * Validates inputs, sends data to backend, and processes results
   */
  const handleAnalyze = async () => {
    // Validate job description input
    if (!jobDescription.trim()) {
      alert('Please enter a job description');
      return;
    }

    // Validate that files were uploaded
    if (resumeFiles.length === 0) {
      alert('Please upload at least one resume');
      return;
    }

    // Set loading state and clear previous results
    setIsAnalyzing(true);
    setAnalysisResults([]);

    try {
      // Prepare form data for multipart request
      const formData = new FormData();
      formData.append('job_description', jobDescription);
      
      // Add all uploaded files to form data
      resumeFiles.forEach(file => {
        formData.append('files', file);
      });

      // Send request to backend API (works with both local and Docker setups)
      const apiUrl = process.env.NODE_ENV === 'production' 
        ? '/api/analyze'  // Docker nginx proxy
        : 'http://127.0.0.1:8000/analyze';  // Local development
      
      const response = await fetch(apiUrl, {
        method: 'POST',
        body: formData,
      });

      // Handle API errors
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Analysis failed');
      }

      // Process successful response
      const data = await response.json();
      setAnalysisResults(data.results);
    } catch (error) {
      console.error('Error analyzing resumes:', error);
      alert('Error analyzing resumes: ' + error.message);
    } finally {
      // Always reset loading state
      setIsAnalyzing(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 8) return '#10b981'; // green
    if (score >= 6) return '#f59e0b'; // yellow
    return '#ef4444'; // red
  };

  return (
    <div className="app">
      <div className="container">
        {/* Header */}
        <div className="header">
          <div className="title">
            Smart Resume Screener
          </div>
          <p className="subtitle">
            AI-powered intelligent candidate ranking powered by advanced language models
          </p>
        </div>

        {/* Main Input Area */}
        <div className="input-section">
          {/* Job Description Card */}
          <div className="input-card">
            <div className="card-header">
              <span className="card-icon">📄</span>
              <h3>Job Description</h3>
            </div>
            <textarea
              className="job-description-input"
              placeholder="Paste the job description here...

Example:
- Required skills:
Python, FastAPI, React
- Experience: 3+ years in full-stack
development
- Education: Bachelor's in Computer Science"
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
            />
          </div>

          {/* Upload Resumes Card */}
          <div className="input-card">
            <div className="card-header">
              <span className="card-icon">☁️</span>
              <h3>Upload Resumes</h3>
            </div>
            <div
              {...getRootProps()}
              className={`dropzone ${isDragActive ? 'active' : ''}`}
            >
              <input {...getInputProps()} />
              <div className="upload-icon">⬆️</div>
              <p className="upload-text">
                {isDragActive
                  ? 'Drop the files here...'
                  : 'Drag and drop resumes here, or click to browse'}
              </p>
              <p className="file-support">
                Supports PDF, DOCX, and TXT files (max 10 files)
              </p>
            </div>
            {resumeFiles.length > 0 && (
              <div className="file-list">
                <p className="file-count">{resumeFiles.length} file(s) selected:</p>
                <ul>
                  {resumeFiles.map((file, index) => (
                    <li key={index} className="file-item">
                      📄 {file.name}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>

        {/* Analyze Button */}
        <div className="analyze-section">
          <button
            className={`analyze-button ${isAnalyzing ? 'analyzing' : ''}`}
            onClick={handleAnalyze}
            disabled={isAnalyzing}
          >
            <span className="analyze-icon">📊</span>
            {isAnalyzing ? 'Analyzing...' : 'Analyze & Rank Candidates'}
          </button>
        </div>

        {/* Results Section */}
        {analysisResults.length > 0 && (
          <div className="results-section">
            <h2 className="results-title">Analysis Results</h2>
            <div className="results-grid">
              {analysisResults.map((result, index) => (
                <div key={index} className="result-card">
                  <div className="result-header">
                    <h3 className="result-filename">{result.filename}</h3>
                    <div 
                      className="result-score"
                      style={{ backgroundColor: getScoreColor(result.score) }}
                    >
                      {result.score}/10
                    </div>
                  </div>
                  <p className="result-justification">{result.justification}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
