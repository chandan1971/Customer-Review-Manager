from transformers import pipeline
from app.constants.sentiment_constants import TOPIC_KEYWORDS
import re
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

def get_review_sentiment(review_text: str)-> str:
    sentiment_pipe = pipeline("sentiment-analysis")
    sentiment_label = sentiment_pipe(review_text)[0]["label"]
    return sentiment_label

def extract_topics(text: str) -> list[str]:
    tokens = re.findall(r"\w+", text.lower())
    stemmed_tokens = [stemmer.stem(tok) for tok in tokens]

    topics = set()
    for topic, keywords in TOPIC_KEYWORDS.items():
        for kw in keywords:
            if stemmer.stem(kw) in stemmed_tokens:
                topics.add(topic)
                break
            
    if not topics:
        topics.add("other")
    return list(topics)