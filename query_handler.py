from owlready2 import *

class QueryHandler:

    def __init__(self) -> None:
        self.iris = {
            'None': []
        }

        self.wm = {}

        self.onto_iri = 'urn_webprotege_ontology_5d0dac0d-8168-404e-b9c8-c3f420fec954'
        self.onto = get_ontology(self.onto_iri + '.owl').load()

        self.fill_iris_dict()

        print()

    def fill_iris_dict(self):
        list_of_entities = [self.onto.individuals(), self.onto.classes(), self.onto.object_properties(), self.onto.data_properties()]

        for entities in list_of_entities:
            for entity in entities:
                if hasattr(entity, "label") and len(entity.label) > 0:
                    self.iris[str(entity.label[0])] = entity.iri
                else:
                    self.iris['None'].append(entity.iri)

                if entity in self.onto.data_properties() or entity in self.onto.object_properties():
                    self.wm[str(entity.label[0])] = [] 

    def retrieve_IRI(self, label):
        return self.iris[label]
    
    def print_results(self, results):
        for result in results:
            print(result)

    def get_queries_to_perform(self):
        queries = []

        if any('Guest' in item for item in self.wm['hasOccupation']):
            queries.append(self.get_persons_with_place_and_occupation)
        
        for item in self.wm['serves']:
            if any(item[0] is item_2[0] for item_2 in self.wm['dishes']):
                queries.append(self.get_dishes_from_cuisine_of_restaurant)
        
        for item in self.wm['hasHealthCondition']:
            if any(item[0] is item_2[0] for item_2 in self.wm['consumes']):
                queries.append(self.get_dishes_from_cuisine_of_restaurant)
        
    
    ######################## Queries ########################

    def get_persons_with_place_and_occupation(self, place, occupation):
        return self.onto.world.sparql(f"""
                SELECT ?person
                WHERE {{
                    ?person <{self.retrieve_IRI('hasOccupation')}> <{self.retrieve_IRI(occupation)}> .
                    ?person <{self.retrieve_IRI('isLocatedIn')}> <{self.retrieve_IRI(place)}>
                }}
            """)
    
    def get_dishes_from_cuisine_of_restaurant(self):
        return self.onto.world.sparql(f"""
            SELECT ?dish
            WHERE {{
                ?restaurant <{self.retrieve_IRI('serves')}> ?cuisine .
                ?cuisine <{self.retrieve_IRI('dishes')}> ?dish
            }}
        """)
    
    def get_person_with_condition_that_consumes(self, condition, dish):
        return self.onto.world.sparql(f"""
            SELECT ?person
            WHERE {{
                ?person <{self.retrieve_IRI('hasHealthCondition')}> <{self.retrieve_IRI(condition)}> .
                ?person <{self.retrieve_IRI('canEat')}> <{self.retrieve_IRI(dish)}>
            }}
        """)