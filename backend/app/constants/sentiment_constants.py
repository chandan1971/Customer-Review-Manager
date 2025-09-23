from enum import Enum

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

    def default_reply(self) -> str:
        if self == Sentiment.POSITIVE:
            return "Thanks for your kind words! We're glad you enjoyed your experience."
        elif self == Sentiment.NEGATIVE:
            return "We’re sorry about your experience. We’ll look into this."
        else:
            return "Thanks for sharing your feedback."