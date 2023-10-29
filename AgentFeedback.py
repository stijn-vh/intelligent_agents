# 4. Action Layer
class FeedbackGenerator:
    def __init__(self):
        self.script = '\nInconsistency found in in the following sentence:\n\n"{}"\n\nInconsistency: {}\nReason: {}\n'

    def generate_feedback(self, inconsistency, sentence):
        print(self.script.format(sentence, inconsistency[0], inconsistency[1]))
        pass