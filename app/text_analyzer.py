import json
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions, SentimentOptions

class TextAnalyzer:
    def __init__(self, api_key='9a-GE9xAuObCOU7mc31DPCs9Qbh8iuRnT7FC38Y7aVmK', url= 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com', version='2021-08-01'):
        self.authenticator = IAMAuthenticator(api_key)
        self.nlu = NaturalLanguageUnderstandingV1(
            version=version,
            authenticator=self.authenticator
        )
        self.nlu.set_service_url(url)

    def analyze_text(self, text):
        try:
            response = self.nlu.analyze(
                text=text,
                features=Features(
                    emotion=EmotionOptions(),
                    sentiment=SentimentOptions()
                )
            )
            return self._process_response(response)
        except Exception as e:
            return {"error": str(e)}

    def _process_response(self, response):
        result = {}
        result['sentiment'] = {
            'label': response.result['sentiment']['document']['label'],
            'score': response.result['sentiment']['document']['score']
        }
        result['emotion'] = response.result['emotion']['document']['emotion']
        return result

if __name__ == "__main__":

    text_analyzer = TextAnalyzer()

    text_to_analyze = "I hate the weather today although it's sunny outside"

    analysis_result = text_analyzer.analyze_text(text_to_analyze)

    print("Sentiment Label:", analysis_result['sentiment']['label'])
    print("Sentiment Score:", analysis_result['sentiment']['score'])
    print("Emotion:", analysis_result['emotion'])