from owlready2 import *

# 2. Knowledge Representation Layer
class Ontology:
    def __init__(self, iri):
        self.ontology = get_ontology(iri + '.owl').load()
        self.iris = { 'None': [] }

        self.fill_iris_dict()

    def get_onto(self):
        return self.ontology

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
                <{self.retrieve_IRI(restaurant)}> <{self.retrieve_IRI('serves')}> ?cuisine .
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
    
    def get_health_condition_food(self, condition):
        return self.ontology.world.sparql(f"""
            SELECT ?dish
            WHERE {{
                <{self.retrieve_IRI(condition)}> <{self.retrieve_IRI('canEat')}> ?dish .
            }}
        """)
    
    def get_cuisine(self, restaurant):
        return self.ontology.world.sparql(f"""
            SELECT ?cuisine
            WHERE {{
                <{self.retrieve_IRI(restaurant)}> <{self.retrieve_IRI('serves')}> ?cuisine .
            }}
        """)
    
    def get_age_of_consent(self):
        return self.ontology.world.sparql(f"""
            SELECT ?age
            WHERE {{
                <{self.retrieve_IRI('AgeOfConsent')}> <{self.retrieve_IRI('hasAge')}> ?age .
            }}
        """)
    
    def retrieve_IRI(self, label):
        return self.iris[label]

class WorkingMemory:
    def __init__(self):
        self.memory = {}

    def store(self, data):
        """
        Name: store()
        Description:
            Merges new relationships into working memory
        Args:
            (dict) new relationship to store
        """
        for key, value in data.items():
            if key in self.memory:
                existing_value = self.memory[key]
                if existing_value and isinstance(existing_value, list) and all(isinstance(item, tuple) for item in existing_value):
                    self.memory[key].extend(item for item in value if item not in existing_value)
                else:
                    self.memory[key] = [existing_value, value] if existing_value and not isinstance(existing_value[0], tuple) else list(value)
            else:
                self.memory[key] = list(value)

    def set_relations_from_ontology(self, ontology):
        """
        Name: set_relations_from_ontology()
        Description:
            Fills the initial working memory with data and object properties from the ontology
        Args:
            (Ontology) owl ontology
        """
        for prop in ontology.data_properties():
            self.memory[str(prop.label[0])] = []
        for prop in ontology.object_properties():
            self.memory[str(prop.label[0])] = []

    #For debug only
    def printwm(self):
        print(self.memory)
        print('\n\n')

    def retrieve(self):
        return self.memory