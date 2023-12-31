# 3. Reasoning Layer
class InconsistencyCheck:
    def __init__(self):
        self.found_incons = {
            'marriage': set(),
            'health': set(),
            'food': set(),
            'location': set()
        }

    def get_found_incons(self):
        return self.found_incons
    
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
        if (len(wm['isMarriedTo']) and len(wm['hasAge'])) > 0:
            person1, person2 = wm['isMarriedTo'][0]
            consentAge = list(ontology.get_age_of_consent())[0][0]
            incon_set = (person1, person2) #unique identifier for set(), good for keeping track
            if (incon_set not in self.found_incons['marriage']):
                person1age = self.get_age(person1, wm)
                person2age = self.get_age(person2, wm)
                if (int(person1age) or int(person2age)) < consentAge:
                    self.found_incons['marriage'].add(incon_set)
                    inconsistencies.append(('Marriage', '{} and {} are married under the age of consent of {}'.format(person1, person2, consentAge)))

        # Health condition check
        if (len(wm['hasHealthCondition']) > 0 and (len(wm['consumes'])) > 0):
            for pair in wm['hasHealthCondition']:
                person, condition = pair
                foods = [item[1] for item in wm['consumes'] if item[0] == person]
                for food in foods:
                    incon_set = (person, food)
                    food = food.capitalize()
                    if len(condition.split(" ")) > 1:
                        condition = condition.split(" ")[0].capitalize() + " " + condition.split(" ")[1].capitalize()
                    if (incon_set not in self.found_incons['health']) and not list(ontology.get_person_with_condition_that_consumes(condition, food)) and (food != str(list(ontology.get_health_condition_food(condition))[0][0].label.first())):
                        self.found_incons['health'].add(incon_set)
                        inconsistencies.append(('Health Condition', '{} can not eat {} because they have {}'.format(person, food, condition)))

        # Cuisine check
        if (len(wm['isLocatedIn']) > 0 and (len(['consumes'])) > 0):
            for pair in wm['consumes']:
                person = pair[0]
                food = pair[1].capitalize()
                for locPair in wm['isLocatedIn']:
                    locPerson, location = locPair
                    incon_set = (locPerson, location)
                    if location != 'kitchen':
                        locationFoods = [str(i[0].label.first()) for i in list(ontology.get_dishes_from_cuisine_of_restaurant(location))]
                        cuisine = str(list(ontology.get_cuisine('La Trattoria'))[0][0].label.first())
                        if (incon_set not in self.found_incons['food']) and (person == locPerson) and (food not in locationFoods):
                            self.found_incons['food'].add(incon_set)
                            inconsistencies.append(('Cuisine mismatch', '{} does not serve {} as it serves {} cuisine'.format(location, food, cuisine)))
        
        # guest location check
        if (len(wm['isLocatedIn']) > 0) and (len(['hasOccupation']) > 0):
            for pair in wm['isLocatedIn']:
                person,location = pair
                if location not in ['Amsterdam', 'Trattoria”', 'La Trattoria']:
                    location = location.capitalize()
                    for occPair in wm['hasOccupation']:
                        occPerson, occupation = occPair
                        incon_set = (person, location)
                        if (incon_set not in self.found_incons['location']) and (person == occPerson) and not list(ontology.get_persons_with_place_and_occupation(location, occupation)):
                            self.found_incons['location'].add(incon_set)
                            inconsistencies.append(('Location mismatch', "{}'s location should not be {}".format(person, location)))
                            

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