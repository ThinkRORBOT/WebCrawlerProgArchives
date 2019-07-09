from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

def get_sentiment(comment):
    blob = TextBlob(comment, analyzer=NaiveBayesAnalyzer())
    # blob = TextBlob(comment)
    return blob.sentiment.p_pos
