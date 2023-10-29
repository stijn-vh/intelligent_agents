import nltk
import spacy
from spacy.matcher import Matcher
import re

# Necessary for sentence segmentation
# nltk.download('punkt')

# 1. Perception Layer
class NLP:
    def __init__(self):
        self.model = spacy.load("en_core_web_sm")
        self.matcher = Matcher(self.model.vocab)

        # Matching Rules
        pattern_loc = [{"LOWER": "located"}, {"LOWER": "in"}, {"ENT_TYPE": "GPE"}]
        pattern_mar = [{"TEXT": "married"}, {"TEXT": "couple"}, {"TEXT": ","}, {"POS": "PROPN"}, {"TEXT": "and"}, {"POS": "PROPN"}]
        self.matcher.add("LOCATION", [pattern_loc])
        self.matcher.add("MARRIAGE", [pattern_mar])

        pass

    def parse(self, sent):
        doc = self.model(sent)
        matches = self.matcher(doc)
        relationships = {}

        for match_id, start, end in matches:
            match_id_str = self.model.vocab.strings[match_id]
            span = doc[start:end]
            
            #Location
            if match_id_str == "LOCATION":
                subject = doc[start-2:start].text
                location = span[-1].text
                relationships["isLocatedIn"] = [(subject, location)]

            #Marriage
            if match_id_str == "MARRIAGE":
                person1, person2 = span[3].text, span[5].text
                relationships["isMarriedTo"] = [(person1, person2)]
        
        #Ages
        for token in doc:
            if token.like_num:
                age = token.text
                for ancestor in token.ancestors:
                    if ancestor.dep_ in ["nsubj", "nsubjpass"]:
                        person = ancestor.text
                        relationships.setdefault("hasAge", []).append((person, age))

        if "hasAge" in relationships:
            relationships["hasAge"] = tuple(relationships["hasAge"])

        #Guest occupation
        dining_keywords = ["dinner", "restaurant", "dining", "meal"]
        added_entities = set()
        for token in doc:
            if token.lemma_.lower() in dining_keywords:
                left_span = doc[:token.i]
                named_entities = [ent for ent in left_span.ents if ent.label_ == "PERSON" and ent.text not in added_entities]
                for named_entity in named_entities:
                    person = named_entity.text
                    relationships.setdefault("hasOccupation", []).append((person, "Guest"))
                    added_entities.add(person)

        if "hasOccupation" in relationships:
            relationships["hasOccupation"] = tuple(relationships["hasOccupation"])
        
        #Person location
        location_keywords = ["restaurant", "dinner", "dining"]
        added_entities = set()
        location_name = "La Trattoria"
        location_relationships = []
        for token in doc:
            if token.lemma_.lower() in location_keywords:
                left_span = doc[:token.i]
                named_entities = [ent for ent in left_span.ents if ent.label_ == "PERSON" and ent.text not in added_entities]
                for named_entity in named_entities:
                    person = named_entity.text
                    location_relationships.append((person, location_name))
                    added_entities.add(person)

        if location_relationships:
            relationships["isLocatedIn"] += tuple(location_relationships)

        for token in doc:
            if token.dep_ in ("xcomp", "ccomp") and token.head.lemma_ in ("order", "decide"):
                subject = [ancestor for ancestor in token.ancestors if ancestor.dep_ in ("nsubj", "nsubjpass")]
                object = [descendant for descendant in token.subtree if descendant.dep_ in ("dobj", "attr")]
                if subject and object:
                    food_item = ' '.join([word.text for word in object[0].subtree])
                    relationships["consumes"].append((subject[0].text, food_item))

        return relationships

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