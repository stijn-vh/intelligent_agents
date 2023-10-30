# 4. Action Layer
class FeedbackGenerator:
    def __init__(self):
        self.script = 'Inconsistency found in in the following sentence:\n\n"{}"\n\nInconsistency: {}\nReason: {}\n'

    def generate_feedback(self, inconsistency, sentence):
        print('\033[031m'+'##############################################################\n'+'\033[0m')
        print(self.script.format(sentence, inconsistency[0], inconsistency[1]))
        pass