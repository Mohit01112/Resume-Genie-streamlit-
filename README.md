# 🧞 Resume Genie

Resume Genie is an AI-powered career assistant built with **Streamlit, LangChain, and Groq API**. It helps job seekers analyze their resumes, match them with job descriptions, generate personalized cover letters, and receive AI-powered career guidance.

## 🚀 Features

### 📄 Resume Checker

- Upload your resume in PDF format
- Get an AI-powered resume score out of 100
- Analyze clarity, relevance, formatting, keywords, and ATS-friendliness
- Identify resume strengths and weaknesses
- Extract explicitly mentioned skills
- Get recommended additional skills
- Receive suggested career paths and roles

### 📊 Resume-JD Matcher

- Upload your resume
- Paste a job description
- Get an overall resume-to-JD match score
- Identify matched keywords
- Find missing keywords and skills
- Get readability and ATS compatibility scores
- Perform skill-gap analysis
- Receive actionable resume improvement suggestions
- Get industry-specific feedback

### ✉️ Cover Letter Generator

- Upload your resume
- Paste a job description
- Generate a personalized cover letter
- Match resume experience and skills with the job requirements
- Avoid fabricating experience or qualifications
- Stream the generated response
- Download the generated cover letter

### 💬 AI Career Coach

- Upload your resume
- Chat with an AI career advisor
- Get resume-specific career guidance
- Prepare for interviews
- Identify skill gaps
- Get job-search strategies
- Explore suitable career paths
- Receive professional development recommendations

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **LangChain**
- **Groq API**
- **OpenAI GPT-OSS-20B**
- **PyPDF**
- **Sentence Transformers**
- **python-dotenv**

## 🏗️ Architecture

```text
User
  │
  ▼
Streamlit Interface
  │
  ├── Resume Checker
  │
  ├── Resume-JD Matcher
  │
  ├── Cover Letter Generator
  │
  └── AI Career Coach
  │
  ▼
LangChain
  │
  ▼
Groq API
  │
  ▼
openai/gpt-oss-20b
  │
  ▼
AI Response
