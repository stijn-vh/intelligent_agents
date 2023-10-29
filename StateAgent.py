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
        self.query_checker = QueryChecker(self.wm, self.ontology)
        
        self.wm.set_relations_from_ontology(self.ontology.get_onto())

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
            self.relations = self.parser.parse(self.current_sentence)
            self.current_state = 'S3'
        else:
            self.current_state = 'END'

    def store_in_memory(self):
        """
        Name: store_in_memory()
        Description:
            Stores new entity relationship data into working memory
        """
        self.wm.store(self.relations)

        #self.wm.printwm() #Currently for Debug purposes
        #Below commented out is for debug running
        # if self.current_sentence_idx < 10:
        #     self.current_sentence_idx += 1
        #     self.current_state = 'S2'
        # else:
        #     self.current_state='END'

        if self.query_checker.get_queries_to_perform():
            self.current_state = 'S4'
        else:
            self.current_sentence_idx += 1
            self.current_state = 'S2'

    def query_ontology(self):
        queries = self.query_checker.get_queries_to_perform()
        self.query_results = []
        print(self.ontology.get_age_of_consent())
        for query in queries:
            self.query_results.append(list(query()))
        self.current_state = 'S5'

    def store_ontology_results(self):
        #Currently the agent gets to here
        ####Between these comments is for debug
        self.current_state = 'S6'
        # if self.current_sentence_idx < 10:
        #     self.current_sentence_idx += 1
        #     self.current_state = 'S2'
        # else:
        #     self.current_state='END'
        ###For debug above
        
        # self.wm.store(self.query_results)
        # self.current_state = 'S6'

    def reasoner(self):
        self.inconsistencies = self.incon_check.check(self.wm.retrieve())
        if self.inconsistencies:
            self.current_state = 'S7'
        else:
            self.current_sentence_idx += 1
            self.current_state = 'S2'

    def output_inconsistency(self):
        for inconsistency in self.inconsistencies:
            feedback = self.feedback_gen.generate_feedback(inconsistency, self.current_sentence)
        self.current_sentence_idx += 1
        self.current_state = 'S2'