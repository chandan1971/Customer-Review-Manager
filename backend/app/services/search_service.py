from app.utils.db_utils import get_all_reviews_texts
from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SearchService:
    def __init__(self, db: Session):
        self.db = db
        
    def search_reviews(self, query: str, top_k: int = 5):
        reviews = get_all_reviews_texts(self.db)
        if not reviews:
            return []

        review_texts = [r['review_text'] for r in reviews]
        review_ids = [r['id'] for r in reviews]

       
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(review_texts)
        query_vec = vectorizer.transform([query])

        similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
        top_indices = similarities.argsort()[::-1][:top_k]

        top_reviews = []
        for idx in top_indices:
            if(similarities[idx]>=0.1):
                top_reviews.append({
                    "id": review_ids[idx],
                    "review_text": review_texts[idx],
                    "similarity": float(similarities[idx])
                })

        return top_reviews
