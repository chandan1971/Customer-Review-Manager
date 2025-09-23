from sqlalchemy.orm import Session
from app.utils.db_utils import fetch_topic_sentiment_counts
from app.constants.sentiment_constants import ALL_SENTIMENTS, ALL_TOPICS

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_analytics(self):
        db_result= fetch_topic_sentiment_counts(self.db)
        analytics = {topic: {sent: 0 for sent in ALL_SENTIMENTS} for topic in ALL_TOPICS}

        for row in db_result:
            topic = row['topic']
            sentiment = row['sentiment']
            count = row['count']

            if topic not in analytics:
                analytics[topic] = {sent: 0 for sent in ALL_SENTIMENTS}  

            analytics[topic][sentiment] = count

        return analytics
