from mesa import Agent
from random import randint
from math import sin, cos, radians

class Person(Agent):
    infection_days_remaining = 0

    def __init__(self, model, pos, condition='Healthy'):
        super().__init__(pos, model)
        self.pos = pos
        self.condition = condition
        if condition != 'Healthy':
            self.infection_days_remaining = self.model.infection_duration


    def step(self):
        new_direction = randint(0, 359)
        
        x, y = self.pos
        x += round(sin(radians(new_direction)))
        y += round(cos(radians(new_direction)))

        if x < 0:
            x = 0
        
        if x >= self.model.grid.width:
            x = self.model.grid.width - 1

        if y < 0:
            y = 0

        if y >= self.model.grid.height:
            y = self.model.grid.height - 1

        if (x, y) == self.pos:
            return
        
        self.model.grid.move_agent(self, (x, y))

        if self.condition == 'Sick':
            for neighbor in self.model.grid.neighbor_iter(self.pos):
                if neighbor.condition == 'Healthy':
                    continue
                if self.model.random.random() <= self.model.infectivity_rate:
                    neighbor.condition = 'Sick'
                    neighbor.infection_days_remaining = self.model.infection_duration

        if self.infection_days_remaining > 0:
            self.infection_days_remaining -= 1
        else:
            self.condition = 'Healthy'
