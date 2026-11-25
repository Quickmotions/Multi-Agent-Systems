from Agents.agent import Agent

class Car(Agent):
    def __init__(self, id, speed, velocity, size, starting_pos):
        super().__init__(id, speed, velocity, size, starting_pos)