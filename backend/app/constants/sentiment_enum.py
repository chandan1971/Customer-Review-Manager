from enum import Enum
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