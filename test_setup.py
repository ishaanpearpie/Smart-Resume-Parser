#!/usr/bin/env python3
"""
Test script to verify the Smart Resume Screener setup
Run this after installing dependencies to check if everything is working
"""

import sys
import os

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing package imports...")
    
    try:
        import fastapi
        print("✓ FastAPI imported successfully")
    except ImportError as e:
        print(f"✗ FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("✓ Uvicorn imported successfully")
    except ImportError as e:
        print(f"✗ Uvicorn import failed: {e}")
        return False
    
    try:
        import sqlalchemy
        print("✓ SQLAlchemy imported successfully")
    except ImportError as e:
        print(f"✗ SQLAlchemy import failed: {e}")
        return False
    
    try:
        import PyPDF2
        print("✓ PyPDF2 imported successfully")
    except ImportError as e:
        print(f"✗ PyPDF2 import failed: {e}")
        return False
    
    try:
        import docx
        print("✓ python-docx imported successfully")
    except ImportError as e:
        print(f"✗ python-docx import failed: {e}")
        return False
    
    try:
        import google.generativeai
        print("✓ google-generativeai imported successfully")
    except ImportError as e:
        print(f"✗ google-generativeai import failed: {e}")
        return False
    
    try:
        import dotenv
        print("✓ python-dotenv imported successfully")
    except ImportError as e:
        print(f"✗ python-dotenv import failed: {e}")
        return False
    
    return True

def test_env_file():
    """Test if .env file exists and has API key"""
    print("\nTesting environment configuration...")
    
    env_path = os.path.join("backend", ".env")
    if not os.path.exists(env_path):
        print("✗ .env file not found in backend directory")
        print("  Please copy env.example to .env and add your API key")
        return False
    
    with open(env_path, 'r') as f:
        content = f.read()
        if "GOOGLE_API_KEY=your_gemini_api_key_here" in content:
            print("✗ .env file contains placeholder API key")
            print("  Please replace with your actual Google Gemini API key")
            return False
        elif "GOOGLE_API_KEY=" in content:
            print("✓ .env file found with API key configured")
            return True
        else:
            print("✗ .env file missing GOOGLE_API_KEY")
            return False

def test_database_creation():
    """Test if database can be created"""
    print("\nTesting database setup...")
    
    try:
        from sqlalchemy import create_engine
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy import Column, Integer, String, Text, DateTime
        from datetime import datetime
        
        # Test database creation
        engine = create_engine("sqlite:///./test_db.db")
        Base = declarative_base()
        
        class TestModel(Base):
            __tablename__ = "test_table"
            id = Column(Integer, primary_key=True)
            name = Column(String)
        
        Base.metadata.create_all(bind=engine)
        print("✓ Database creation test passed")
        
        # Clean up test database
        os.remove("test_db.db")
        return True
        
    except Exception as e:
        print(f"✗ Database creation test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Smart Resume Screener - Setup Test")
    print("=" * 40)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test environment file
    if not test_env_file():
        all_passed = False
    
    # Test database
    if not test_database_creation():
        all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("✓ All tests passed! Your setup looks good.")
        print("\nNext steps:")
        print("1. Make sure your .env file has a valid Google Gemini API key")
        print("2. Start the backend: cd backend && uvicorn main:app --reload")
        print("3. Start the frontend: cd frontend && npm start")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        print("\nTo fix:")
        print("1. Install missing packages: pip install -r backend/requirements.txt")
        print("2. Set up your .env file with a valid API key")
        print("3. Run this test again: python test_setup.py")

if __name__ == "__main__":
    main()
