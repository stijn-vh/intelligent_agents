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