
# 3. Reasoning Layer
class InconsistencyCheck:
    def __init__(self):
        self.found_incons = {
            'marriage': set(),
            'health': set(),
            'food': set()
        }

    def get_age(self, name, wm):
        """
        Name: get_age()
        Description:
            Helper function to retrieve the age of entities
        Args:
            (string) entity name
            (dict) working memory of agent
        """
        for entry in wm['hasAge']:
            if entry[0] == name:
                return entry[1]
        return None

    def check(self, wm):
        """
        Name: check()
        Description:
            checks for inconsistencies using working memory and ontology
        Args:
            (dict) working memory of agent
        """
        inconsistencies = []

        # Marriage age
        if (len(wm['isMarriedTo']) > 0) and (len(wm['hasAge']) > 0):
            person1 = wm['isMarriedTo'][0][0]
            person2 = wm['isMarriedTo'][0][1]

            consentAge = 18 #Maybe replace with a Ontology query

            incon_set = (person1, person2) #unique identifier for set(), good for keeping track
            if (incon_set not in self.found_incons['marriage']):
                person1age = self.get_age(person1, wm)
                person2age = self.get_age(person2, wm)

                if (int(person1age) or int(person2age)) < consentAge:
                    self.found_incons['marriage'].add(incon_set)
                    inconsistencies.append(('Marriage', '{} and {} are married under the age of consent of {}'.format(person1, person2, consentAge)))

        return inconsistencies


class QueryChecker:
    def __init__(self, wm, onto) -> None:
        self.wm = wm
        self.onto = onto

    def get_queries_to_perform(self):
        queries = []

        if any('Guest' in item for item in self.wm.retrieve()['hasOccupation']):
            queries.append(lambda: self.onto.get_persons_with_place_and_occupation('Guest', 'Kitchen'))

        for item in self.wm.retrieve()['serves']:
            for item_2 in self.wm.retrieve()['dishes']:
                if item[0] == item_2[0]:
                    queries.append(lambda: self.onto.get_dishes_from_cuisine_of_restaurant(item[1], item_2[1]))            
        

        for item in self.wm.retrieve()['hasHealthCondition']:
            for item_2 in self.wm.retrieve()['consumes']:
                if item[0] == item_2[0]:
                    queries.append(lambda: self.onto.get_person_with_condition_that_consumes(item[1], item_2[1]))

        return queries