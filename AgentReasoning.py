
# 3. Reasoning Layer
class InconsistencyCheck:
    #Some kind of logic reasoner/checker
    def check(self, data):
        pass

class QueryChecker:
    def __init__(self, wm, onto) -> None:
        self.wm = wm
        self.onto = onto

    def get_queries_to_perform(self):
        queries = []

        if any('Guest' in item for item in self.wm['hasOccupation']):
            queries.append(lambda: self.onto.get_persons_with_place_and_occupation('Guest', 'Kitchen'))

        for item in self.wm['serves']:
            for item_2 in self.wm['dishes']:
                if item[0] == item_2[0]:
                    queries.append(lambda: self.onto.get_dishes_from_cuisine_of_restaurant(item[1], item_2[1]))            
        

        for item in self.wm['hasHealthCondition']:
            for item_2 in self.wm['consumes']:
                if item[0] == item_2[0]:
                    queries.append(lambda: self.onto.get_person_with_condition_that_consumes(item[1], item_2[1]))

        return queries