from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import RandomActivation

from .agent import Person


class PeopleCollision(Model):
    """
    Simple Forest Fire model.
    """

    def __init__(self, width=100, height=100, density=0.5, infection_rate=0.5, infectivity_rate=0.5, infection_duration=3):
        """
        Create a new forest fire model.

        Args:
            width, height: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """
        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = Grid(width, height, torus=False)
        self.density = density
        self.infection_rate = infection_rate
        self.infectivity_rate = infectivity_rate
        self.infection_duration = infection_duration

        self.datacollector = DataCollector(
            {
                "Healthy": lambda m: self.count_type(m, "Healthy"),
                "Sick": lambda m: self.count_type(m, "Sick"),
            }
        )

        # Place a tree in each cell with Prob = density
        for (_, x, y) in self.grid.coord_iter():
            if self.random.random() < density / 5:
                # Create a tree
                condition = 'Healthy'
                if self.random.random() < infection_rate:
                    condition = 'Sick'
                new_person = Person(self, (x, y), condition)
                self.grid._place_agent(new_person, (x, y))
                self.schedule.add(new_person)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # Halt if no more fire
        if self.count_type(self, 'Healthy') == 0 or self.count_type(self, 'Sick') == 0:
            self.running = False
            self.datacollector.collect(self)

    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        agents = model.schedule.agents
        return len([tree for tree in agents if tree.condition == tree_condition])
