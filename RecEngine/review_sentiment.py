from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class Sentiment_Analyzer:
    def __init__(self,text):
        self.analyzer=SentimentIntensityAnalyzer()
        self.text=text

    def getSentiment(self):
        sentiment_dict = self.analyzer.polarity_scores(self.text)
        
        if sentiment_dict['compound'] >= 0.05 :
            overall_sentiment = "Positive"

        elif sentiment_dict['compound'] <= - 0.05 :
            overall_sentiment = "Negative"

        else :
            overall_sentiment = "Neutral"
        return  overall_sentiment
        
