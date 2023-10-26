from AgentPerception import *
from AgentKnowledge import *
from AgentReasoning import *
from AgentFeedback import *

class Agent:
    def __init__(self):
        self.parser = NLP()
        self.segmenter = Segmentation()
        self.ontology = Ontology('urn_webprotege_ontology_5d0dac0d-8168-404e-b9c8-c3f420fec954')
        self.wm = WorkingMemory()
        self.incon_check = InconsistencyCheck()
        self.feedback_gen = FeedbackGenerator()
        self.query_checker = QueryChecker()
        
        self.wm.set_relations_from_ontology(self.ontology)

        self.states = {
            'S1': self.start,
            'S2': self.read_and_nlp,
            'S3': self.store_in_memory,
            'S4': self.query_ontology,
            'S5': self.store_ontology_results,
            'S6': self.reasoner,
            'S7': self.output_inconsistency,
        }
        self.current_state = 'S1'

    def start(self, story):
        """
        Name: start()
        Description:
            Segments text and initialises sentence index used by agent
        Args:
            (string) Agent story
        """
        self.story = self.segmenter.segment(story)
        self.current_sentence_idx = 0
        self.current_state = 'S2'
        while self.current_state != 'END':
            self.states[self.current_state]()

    def read_and_nlp(self):
        """
        Name: read_and_nlp()
        Description:
            Applies NLP processes to the sentence the agent is currently at
        """
        if self.current_sentence_idx < len(self.story):
            self.current_sentence = self.story[self.current_sentence_idx]
            self.entities = self.parser.parse(self.current_sentence)
            self.current_state = 'S3'
        else:
            self.current_state = 'END'

    def store_in_memory(self):
        self.wm.store(self.entities)
        if self.can_execute_query():
            self.current_state = 'S4'
        else:
            self.current_sentence_idx += 1
            self.current_state = 'S2'

    def query_ontology(self):
        self.query_results = self.ontology.query(self.entities)
        self.current_state = 'S5'

    def store_ontology_results(self):
        self.wm.store(self.query_results)
        self.current_state = 'S6'

    def reasoner(self):
        self.inconsistencies = self.incon_check.check(self.wm.retrieve())
        if self.inconsistencies:
            self.current_state = 'S7'
        else:
            self.current_sentence_idx += 1
            self.current_state = 'S2'

    def output_inconsistency(self):
        for inconsistency in self.inconsistencies:
            feedback = self.feedback_gen.generate_feedback(inconsistency)
            print(feedback)
        self.current_sentence_idx += 1
        self.current_state = 'S2'

    def can_execute_query(self):
        """
        Name: can_execute_query()
        Description:
            Retrieves queries which could be performed based on current working memory
        """
        return self.query_checker.get_queries_to_perform()