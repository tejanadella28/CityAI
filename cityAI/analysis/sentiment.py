from textblob import TextBlob

def analyze_sentiment(text: str) -> str:
    """Analyze sentiment of the text."""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"
