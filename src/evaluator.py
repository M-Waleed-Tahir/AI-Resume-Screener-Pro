class ResumeEvaluator:
    """
    Evaluator module to compare extracted keywords between Resume and Job Description (JD).
    Identifies matched skills, missing critical keywords, and visual summary data.
    """

    def __init__(self):
        pass

    def analyze_skills_gap(self, resume_keywords: list, jd_keywords: list) -> dict:
        """
        Compares candidate keywords with JD keywords to find overlaps and missing skills.
        """
        resume_set = set([kw.lower() for kw in resume_keywords])
        jd_set = set([kw.lower() for kw in jd_keywords])

        matched_skills = list(resume_set.intersection(jd_set))
        missing_skills = list(jd_set - resume_set)

        total_jd_keywords = len(jd_set) if len(jd_set) > 0 else 1
        coverage_rate = round((len(matched_skills) / total_jd_keywords) * 100, 2)

        return {
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "coverage_rate": coverage_rate
        }