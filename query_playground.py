from owlready2 import *

onto_uri = 'urn_webprotege_ontology_5d0dac0d-8168-404e-b9c8-c3f420fec954'

onto = get_ontology(onto_uri + '.owl').load()

retrieve_guests_from_kitchen_query = """
    SELECT ?person
    WHERE {
        ?person <http://webprotege.stanford.edu/R87cwZuaE8be2SzYQtnrCWR> <http://webprotege.stanford.edu/R8s1aAoLumni3FEo5qSvwl7> .
        ?person <http://webprotege.stanford.edu/RCpk7ICP5OrVBr8HUVlF9lH> <http://webprotege.stanford.edu/RBGS2NqoXEtyR8XxshagIT7>
    }
"""

retrieve_underaged_married_persons = """
    SELECT ?person
    WHERE {
        
    }
"""

# Execute the query
results = onto.world.sparql(retrieve_guests_from_kitchen_query)

# Print the results
for result in results:
    print(result)