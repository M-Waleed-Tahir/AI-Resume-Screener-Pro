import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Import custom modular engines from src folder
from src.parser import ResumeParser
from src.matcher import ResumeMatcher
from src.evaluator import ResumeEvaluator

# Streamlit Page Setup
st.set_page_config(
    page_title="Intelligent Resume Screener Pro",
    page_icon="📄",
    layout="wide"
)

def main():
    st.title("📄 AI-Powered Intelligent Resume Screener & Parser")
    st.markdown("##### Production-grade NLP Pipeline for Candidate Screening and Job Description Match Analysis")
    st.divider()

    # Initialize Modules
    parser = ResumeParser()
    matcher = ResumeMatcher()
    evaluator = ResumeEvaluator()

    # Layout: Two Columns for Upload and JD Input
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1. Upload Candidate Resume (PDF)")
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    with col2:
        st.subheader("2. Target Job Description (JD)")
        job_description = st.text_area(
            "Paste Job Description text here...",
            height=180,
            placeholder="Paste technical requirements, qualifications, and key skills..."
        )

    st.divider()

    if uploaded_file is not None and job_description.strip() != "":
        if st.button("🚀 Analyze & Screen Candidate", type="primary"):
            with st.spinner("Extracting PDF text and running NLP pipeline..."):
                # 1. Extract and Clean Text
                raw_text = parser.extract_text_from_pdf(uploaded_file)
                cleaned_resume_text = parser.clean_text(raw_text)
                contact_info = parser.extract_contact_info(raw_text)

                # 2. Calculate Match Score
                cleaned_jd_text = parser.clean_text(job_description)
                match_score = matcher.calculate_match_score(cleaned_resume_text, cleaned_jd_text)

                # 3. Extract Keywords and Analyze Gap
                resume_keywords = matcher.extract_top_keywords(cleaned_resume_text, top_n=15)
                jd_keywords = matcher.extract_top_keywords(cleaned_jd_text, top_n=15)
                gap_analysis = evaluator.analyze_skills_gap(resume_keywords, jd_keywords)

            st.success("Analysis Complete!")

            # Display Key Metrics
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.metric("Overall Match Score", f"{match_score}%")
            with m_col2:
                st.metric("Candidate Email", contact_info["email"])
            with m_col3:
                st.metric("Candidate Phone", contact_info["phone"])

            st.divider()

            # Detailed Visual Breakdown
            b_col1, b_col2 = st.columns(2)

            with b_col1:
                st.subheader("✅ Matched Skills & Overlaps")
                if gap_analysis["matched_skills"]:
                    for skill in gap_analysis["matched_skills"]:
                        st.markdown(f"- **{skill.title()}**")
                else:
                    st.info("No direct keyword overlaps detected.")

            with b_col2:
                st.subheader("⚠️ Missing Skills / Keywords Gap")
                if gap_analysis["missing_skills"]:
                    for skill in gap_analysis["missing_skills"]:
                        st.markdown(f"- :red[{skill.title()}]")
                else:
                    st.success("Great match! No major skills missing.")

            # Raw Extracted Text Viewer
            with st.expander("🔍 View Raw Parsed Resume Text"):
                st.text(raw_text)

    elif uploaded_file is None or job_description.strip() == "":
        st.info("💡 Please upload a Resume PDF and paste a Job Description above to initiate screening.")

if __name__ == "__main__":
    main()