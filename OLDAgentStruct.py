# 1. Perception Layer
class NLP:
    def __init__(self):
        pass

    def parse(self, text):
        pass

class Segmentation:
    def segment(self, text):
        return text.split('.')

# 2. Knowledge Representation Layer
class Ontology:
    def __init__(self):
        self.ontology = None

    #This might be useful, although Raoul mentioned that no edits would take place
    def add_entity(self, entity):
        pass

    #Same issue as above
    def update_entity(self, entity, property):
        pass

class WorkingMemory:
    def __init__(self):
        self.memory = []

    def store(self, data):
        self.memory.append(data)

    def retrieve(self):
        return self.memory

# 3. Reasoning Layer
class InconsistencyCheck:
    #Some kind of logic reasoner/checker
    def check(self, data):
        pass

# 4. Action Layer
class FeedbackGenerator:
    def generate_feedback(self, inconsistency):
        pass

# Main agent body
class Agent:
    def __init__(self):
        self.parser = NLP()
        self.segmenter = Segmentation()
        self.ontology_db = Ontology()
        self.working_memory = WorkingMemory()
        self.inconsistency_checker = InconsistencyCheck()
        self.feedback_generator = FeedbackGenerator()

    def process_story(self, story):
        segments = self.segmenter.segment(story)
        for segment in segments:
            entities = self.parser.parse(segment)
            self.working_memory.store(entities)
            
            for entity in entities:
                self.ontology_db.add_entity(entity)
            
            inconsistencies = self.inconsistency_checker.check(entities)
            for inconsistency in inconsistencies:
                feedback = self.feedback_generator.generate_feedback(inconsistency)
                print(feedback)