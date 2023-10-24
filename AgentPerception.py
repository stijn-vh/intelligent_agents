import nltk
import spacy
import re

# Necessary for sentence segmentation
# nltk.download('punkt')

# 1. Perception Layer
class NLP:
    def __init__(self):
        self.model = spacy.load("en_core_web_sm")
        pass

    def parse(self, text):
        sent = re.sub(r'[^\w\s]', '', text)
        doc = self.model(sent)
        for entity in doc.ents:
            print(entity.label_, ' | ', entity.text)
        pass

class Segmentation:
    def __init__(self):
        pass

    # Segment function which returns a list of individual sentences
    def segment(self, text):
        """
        Name: segment()
        Description:
            Segments text into sentences
        Args:
            (string) text to segment
        Returns:
            (list) individual sentences
        """
        sentences = nltk.sent_tokenize(text)
        return sentences