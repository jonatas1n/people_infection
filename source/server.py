from mesa.visualization.modules import (
    CanvasGrid,
    ChartModule,
    PieChartModule,
    BarChartModule,
)
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .model import PeopleCollision

COLORS = {
    "Healthy": "#00AA00",
    "Sick": "#880000",
}

def people_collision_portrayal(person):
    if person is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    (x, y) = person.pos
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = COLORS[person.condition]
    return portrayal

canvas_element = CanvasGrid(people_collision_portrayal, 100, 100, 500, 500)

infection_chart = ChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)

infection_pie = PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)

model_params = {
    "height": 100,
    "width": 100,
    "density": UserSettableParameter("slider", "Demographic density", 0.5, 0.01, 1.0, 0.01),
    "infection_rate": UserSettableParameter("slider", "Infected Rate", 0.5, 0.01, 0.99, 0.01),
    "infectivity_rate": UserSettableParameter("slider", "Infectivity Rate", 0.5, 0.01, 0.99, 0.01),
    "infection_duration": UserSettableParameter("slider", "Infection Duration", 5, 1, 10, 1),
}

server = ModularServer(
    PeopleCollision,
    [canvas_element, infection_chart, infection_pie],
    "Forest Fire",
    model_params,
)
