# 📄 AI-Powered Intelligent Resume Screener & Parser

A production-grade Python NLP application designed to automate candidate screening, match resumes against target Job Descriptions (JD), and perform interactive skills gap analysis using TF-IDF vectorization and Cosine Similarity.

## 🛠️ Tech Stack & Architecture
- **Language:** Python 3.14
- **UI Framework:** Streamlit
- **NLP & ML:** Scikit-Learn (TF-IDF Vectorizer, Cosine Similarity), Regex
- **PDF Extraction:** `pdfplumber`, `pypdf`
- **Architecture:** Modular (`src/parser.py`, `src/matcher.py`, `src/evaluator.py`, `app.py`)

## ⚡ Features
- **Automated Text & Contact Extraction:** Parses PDF resumes and extracts Candidate Email and Phone numbers via regex.
- **Semantic Matching Score:** Calculates cosine similarity percentage between Resume and JD text.
- **Skills Gap Analysis:** Identifies overlapping matched technical skills and flags missing target keywords.
- **Interactive Streamlit Dashboard:** Clean web-based interface for recruiters and hiring managers.
