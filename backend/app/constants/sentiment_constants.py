from enum import Enum
from typing import  Optional
TOPIC_KEYWORDS = {
    "service": ["servic", "staff", "waiter", "support", "help", "ignor"],
    "wait_time": ["wait", "delay", "slow", "queue", "late", "deliveri"],
    "pricing": ["price", "cost", "expens", "cheap", "valu", "charg"],
    "product_quality": ["qualiti", "defect", "broken", "damag", "good", "bad", "miss", "crash"]
}

ALL_SENTIMENTS = ["POSITIVE", "NEGATIVE", "NEUTRAL"]
ALL_TOPICS = ["service","wait_time","pricing","product_quality"]

class Sentiment(Enum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"

    def format_topics(self,topics: list[str]) -> str:
        if not topics:
            return ""
        if len(topics) == 1:
            return topics[0].replace("_", " ")
        return ", ".join(t.replace("_", " ") for t in topics[:-1]) + " and " + topics[-1].replace("_", " ")


    def default_reply(self, topics: Optional[list[str]] = None) -> str:


        if topics:
            formatted_topics = self.format_topics(topics)
            if self == Sentiment.POSITIVE:
                topic_part = f" We’re thrilled you appreciated our {formatted_topics}!"
            elif self == Sentiment.NEGATIVE:
                topic_part = f" We’ll work on improving our {formatted_topics}."
            else:  
                topic_part = f" Your feedback on {formatted_topics} helps us improve."

        if self == Sentiment.POSITIVE:
            return "Thanks for your kind words! We're glad you enjoyed your experience."+topic_part
        elif self == Sentiment.NEGATIVE:
            return "Thanks for sharing your feedback.We’re sorry about your experience. We’ll look into this."+topic_part
        else:
            return "Thanks for sharing your feedback."+topic_part