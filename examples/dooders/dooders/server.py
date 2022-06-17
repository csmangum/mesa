import mesa

from dooders.agents import Predator, Prey, Food
from dooders.model import DooderSim


def predator_prey_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Prey:
        portrayal["Shape"] = "dooders/resources/Prey.png"
        # https://icons8.com/web-app/433/sheep
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Predator:
        portrayal["Shape"] = "dooders/resources/Killer.png"
        # https://icons8.com/web-app/36821/German-Shepherd
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = round(agent.energy, 1)
        portrayal["text_color"] = "White"

    elif type(agent) is Food:
        if agent.fully_grown:
           portrayal["Shape"] = "dooders/resources/Food.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 0

    return portrayal


canvas_element = mesa.visualization.CanvasGrid(predator_prey_portrayal, 20, 20, 500, 500)
chart_element = mesa.visualization.ChartModule(
    [
        {"Label": "Predators", "Color": "#AA0000"},
        {"Label": "Prey", "Color": "#666666"},
        {"Label": "Food", "Color": "#00AA00"},
    ]
)

model_params = {
    # The following line is an example to showcase StaticText.
    "title": mesa.visualization.StaticText("Parameters:"),
    "food": mesa.visualization.Checkbox("Food Enabled", True),
    "food_regrowth_time": mesa.visualization.Slider("Food Regrowth Time", 20, 1, 50),
    "initial_prey": mesa.visualization.Slider(
        "Initial Prey Population", 100, 10, 300
    ),
    "prey_reproduce": mesa.visualization.Slider(
        "Prey Reproduction Rate", 0.04, 0.01, 1.0, 0.01
    ),
    "initial_predator": mesa.visualization.Slider("Initial Predator Population", 50, 10, 300),
    "predator_reproduce": mesa.visualization.Slider(
        "Predator Reproduction Rate",
        0.05,
        0.01,
        1.0,
        0.01,
        description="The rate at which predator agents reproduce.",
    ),
    "predator_gain_from_food": mesa.visualization.Slider(
        "Predator Gain From Food Rate", 20, 1, 50
    ),
    "prey_gain_from_food": mesa.visualization.Slider("Prey Gain From Food", 4, 1, 10),
}

server = mesa.visualization.ModularServer(
    DooderSim, [canvas_element, chart_element], "Dooder Simulation", model_params
)
server.port = 8521
