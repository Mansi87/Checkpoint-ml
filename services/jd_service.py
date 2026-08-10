from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return text


def analyze_jd(resume_text, jd_text):
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([resume_clean, jd_clean])

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    ats_score = round(similarity * 100, 2)

    jd_vector = vectorizer.transform([jd_clean])
    feature_names = vectorizer.get_feature_names_out()
    jd_scores = jd_vector.toarray()[0]

    top_indices = jd_scores.argsort()[::-1][:15]
    jd_keywords = [feature_names[i] for i in top_indices if jd_scores[i] > 0]

    resume_words = set(resume_clean.split())
    missing_keywords = [kw for kw in jd_keywords if kw not in resume_words]

    return {
        "ats_score": ats_score,
        "missing_keywords": missing_keywords[:10]
    }