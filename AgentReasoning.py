
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

    def check(self, wm, ontology):
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

            consentAge = list(ontology.get_age_of_consent())[0][0]

            incon_set = (person1, person2) #unique identifier for set(), good for keeping track
            if (incon_set not in self.found_incons['marriage']):
                person1age = self.get_age(person1, wm)
                person2age = self.get_age(person2, wm)

                if (int(person1age) or int(person2age)) < consentAge:
                    self.found_incons['marriage'].add(incon_set)
                    inconsistencies.append(('Marriage', '{} and {} are married under the age of consent of {}'.format(person1, person2, consentAge)))

        # Rough health condition check
        if (len(wm['hasHealthCondition']) > 0 and (len(wm['consumes'])) > 0):
            for pair in wm['hasHealthCondition']:
                person = pair[0]
                condition = pair[1]
                foods = [item[1] for item in wm['consumes'] if item[0] == person]
                for food in foods:
                    incon_set = (person, food)
                    food = food.capitalize()
                    if len(condition.split(" ")) > 1:
                        condition = condition.split(" ")[0].capitalize() + " " + condition.split(" ")[1].capitalize()
                    if (incon_set not in self.found_incons['health']) and not list(ontology.get_person_with_condition_that_consumes(condition, food)) and (food != str(list(ontology.get_health_condition_food(condition))[0][0].label.first())):
                        self.found_incons['health'].add(incon_set)
                        inconsistencies.append(('Health Condition', '{} can not eat {} because they have {}'.format(person, food, condition)))

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
                    queries.append(lambda: self.onto.get_dishes_from_cuisine_of_restaurant(item[1].capitalize(), item_2[1].capitalize()))            
        

        for item in self.wm.retrieve()['hasHealthCondition']:
            for item_2 in self.wm.retrieve()['consumes']:
                if item[0] == item_2[0]:
                    queries.append(lambda: self.onto.get_person_with_condition_that_consumes(item[1].capitalize(), item_2[1].capitalize()))

        return queries