import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ResumeMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def calculate_match_score(self, resume_text: str, job_description_text: str) -> float:
        if not resume_text or not job_description_text:
            return 0.0

        documents = [resume_text, job_description_text]
        tfidf_matrix = self.vectorizer.fit_transform(documents)
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(float(similarity) * 100, 2)

    def extract_top_keywords(self, text: str, top_n: int = 15) -> list:
        if not text:
            return []
            
        custom_stop_words = {
            'end', 'responsible', 'skills', 'seeking', 'strong', 
            'expertise', 'candidate', 'requirements', 'required', 'working',
            'learning', 'model', 'deep'
        }
        
        try:
            tfidf = TfidfVectorizer(stop_words='english', ngram_range=(1, 1))
            matrix = tfidf.fit_transform([text])
            feature_names = np.array(tfidf.get_feature_names_out())
            sorted_indices = np.argsort(matrix.toarray()[0])[::-1]
            
            keywords = feature_names[sorted_indices].tolist()
            filtered_keywords = [kw for kw in keywords if kw not in custom_stop_words]
            return filtered_keywords[:top_n]
        except Exception as e:
            print(f"Keyword extraction failed: {e}")
            return []