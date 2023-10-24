import numpy as np
from StateAgent import *

if __name__ == "__main__":
    # Story loaded from txt file
    with open('AgentStory.txt', 'r', encoding='utf-8') as file:
        story = file.read()
    agent = Agent()
    agent.start(story)