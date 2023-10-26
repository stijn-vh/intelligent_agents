from owlready2 import *

# 2. Knowledge Representation Layer
class Ontology:
    def __init__(self, iri):
        self.ontology = get_ontology(iri + '.owl').load()
        self.iris = { 'None': [] }

        self.fill_iris_dict()

        print()

    def fill_iris_dict(self):
        """
        Name: fill_iris_dict()
        Description:
            Fills a dictionary with labels and their corresponding IRI based 
            on the ontology (ex: 'Honest':'http://webprotege.stanford.edu/RCWDrAIFI4yFBz82HfKQBwg').
            IRI's of entities without a label are appended to string in key 'None'
        """
        list_of_entities = [self.ontology.individuals(), self.ontology.classes(), 
            self.ontology.object_properties(), self.ontology.data_properties()]

        for entities in list_of_entities:
            for entity in entities:
                
                if hasattr(entity, "label") and len(entity.label) > 0:
                    self.iris[str(entity.label[0])] = entity.iri
                else:
                    self.iris['None'].append(entity.iri)

    def get_persons_with_place_and_occupation(self, place, occupation):
        return self.ontology.world.sparql(f"""
                SELECT ?person
                WHERE {{
                    ?person <{self.retrieve_IRI('hasOccupation')}> <{self.retrieve_IRI(occupation)}> .
                    ?person <{self.retrieve_IRI('isLocatedIn')}> <{self.retrieve_IRI(place)}>
                }}
            """)
    
    def get_dishes_from_cuisine_of_restaurant(self, restaurant):
        return self.ontology.world.sparql(f"""
            SELECT ?dish
            WHERE {{
                <{restaurant}> <{self.retrieve_IRI('serves')}> ?cuisine .
                ?cuisine <{self.retrieve_IRI('dishes')}> ?dish
            }}
        """)
    
    def get_person_with_condition_that_consumes(self, condition, dish):
        return self.ontology.world.sparql(f"""
            SELECT ?person
            WHERE {{
                ?person <{self.retrieve_IRI('hasHealthCondition')}> <{self.retrieve_IRI(condition)}> .
                ?person <{self.retrieve_IRI('canEat')}> <{self.retrieve_IRI(dish)}>
            }}
        """)
    
    def retrieve_IRI(self, label):
        return self.iris[label]
    
    #This might be useful, although Raoul mentioned that no edits would take place
    def add_entity(self, entity):
        pass

    #Same issue as above
    def update_entity(self, entity, property):
        pass

class WorkingMemory:
    def __init__(self):
        self.memory = []

    def set_relations_from_ontology(self, ontology):
        for entity in [ontology.data_properties(), ontology.object_properties()]:
            if entity in ontology.data_properties() or entity in ontology.object_properties():
                self.memory[str(entity.label[0])] = [] 

    def store(self, data):
        self.memory.append(data)

    def retrieve(self):
        return self.memory