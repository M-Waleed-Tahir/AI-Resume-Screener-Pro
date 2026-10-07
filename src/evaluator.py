class SkillEvaluator:
    """
    Evaluates skill overlaps and missing keyword gaps between 
    Candidate Resume keywords and Target Job Description keywords.
    """

    def evaluate_skills_gap(self, resume_keywords: list, jd_keywords: list) -> dict:
        """
        Compares extracted keywords and categorizes them into matched vs missing skills.
        """
        resume_set = set(k.lower() for k in resume_keywords)
        jd_set = set(k.lower() for k in jd_keywords)

        matched_skills = list(resume_set.intersection(jd_set))
        missing_skills = list(jd_set - resume_set)

        return {
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        }