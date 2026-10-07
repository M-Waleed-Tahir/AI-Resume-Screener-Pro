import streamlit as st
import pandas as pd
from src.parser import ResumeParser
from src.matcher import ResumeMatcher
from src.evaluator import SkillEvaluator

# Initialize Modules
parser = ResumeParser()
matcher = ResumeMatcher()
evaluator = SkillEvaluator()

st.set_page_config(
    page_title="AI Resume Screener Pro",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Screener Pro & Batch Leaderboard")
st.markdown("Upload single or **multiple candidate resumes** to screen, score, and rank them against the Target Job Description.")

# Sidebar Controls
st.sidebar.header("⚙️ Screening Settings")
min_score_filter = st.sidebar.slider("Filter Candidates by Min Match Score (%)", 0, 100, 0)

# Layout Setup
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Upload Candidate Resumes (PDF)")
    uploaded_files = st.file_uploader("Choose PDF files", type=["pdf"], accept_multiple_files=True)

with col2:
    st.subheader("2. Target Job Description (JD)")
    job_description = st.text_area("Paste Job Description text here...", height=200)

st.markdown("---")

if st.button("🚀 Run Batch Screening & Leaderboard", type="primary"):
    if not uploaded_files:
        st.error("Please upload at least one Candidate Resume (PDF).")
    elif not job_description.strip():
        st.error("Please provide a Target Job Description.")
    else:
        with st.spinner("Processing Resumes, Extracting Contact Info & Calculating Scores..."):
            cleaned_jd = parser.clean_text(job_description)
            jd_keywords = matcher.extract_top_keywords(cleaned_jd, top_n=20)
            
            results = []

            for pdf_file in uploaded_files:
                raw_text = parser.extract_text_from_pdf(pdf_file)
                contact_info = parser.extract_contact_info(raw_text)
                cleaned_resume_text = parser.clean_text(raw_text)

                match_score = matcher.calculate_match_score(cleaned_resume_text, cleaned_jd)
                resume_keywords = matcher.extract_top_keywords(cleaned_resume_text, top_n=20)
                
                analysis = evaluator.evaluate_skills_gap(resume_keywords, jd_keywords)

                results.append({
                    "Candidate Name / File": pdf_file.name,
                    "Match Score (%)": match_score,
                    "Email": contact_info["email"],
                    "Phone": contact_info["phone"],
                    "Matched Skills": ", ".join(analysis["matched_skills"][:5]) if analysis["matched_skills"] else "None",
                    "Missing Skills Gap": ", ".join(analysis["missing_skills"][:5]) if analysis["missing_skills"] else "None",
                    "Raw Object": {
                        "analysis": analysis,
                        "raw_text": raw_text
                    }
                })

            # Create DataFrame
            df = pd.DataFrame(results)
            df = df.sort_values(by="Match Score (%)", ascending=False).reset_index(drop=True)
            df.index += 1  # 1-based Rank index

            # Store in session state for dynamic display
            st.session_state["screening_results"] = df

st.markdown("---")

# Display Results & Leaderboard
if "screening_results" in st.session_state:
    df = st.session_state["screening_results"]
    filtered_df = df[df["Match Score (%)"] >= min_score_filter]

    st.subheader("🏆 Candidate Leaderboard & Screening Summary")
    
    # Key Metrics Overview
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Screened", len(df))
    m2.metric("Shortlisted Candidates", len(filtered_df))
    m3.metric("Top Candidate Score", f"{df['Match Score (%)'].max()}%" if not df.empty else "N/A")

    # Display Ranked Table
    st.dataframe(
        filtered_df[["Candidate Name / File", "Match Score (%)", "Email", "Phone", "Matched Skills", "Missing Skills Gap"]],
        use_container_width=True
    )

    # Download CSV Button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Shortlisted Candidates (CSV)",
        data=csv,
        file_name="Shortlisted_Candidates_Report.csv",
        mime="text/csv"
    )

    st.markdown("---")
    st.subheader("🔍 Deep-Dive Candidate Inspector")
    selected_candidate = st.selectbox("Select Candidate for Detailed Analysis:", df["Candidate Name / File"].tolist())

    if selected_candidate:
        cand_data = df[df["Candidate Name / File"] == selected_candidate].iloc[0]
        
        c_col1, c_col2 = st.columns(2)
        with c_col1:
            st.success("✅ Matched Skills & Overlaps")
            st.write(cand_data["Matched Skills"])
        with c_col2:
            st.error("⚠️ Missing Critical Keywords")
            st.write(cand_data["Missing Skills Gap"])