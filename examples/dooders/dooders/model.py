"""
Wolf-Sheep Predation Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

import mesa

from dooders.scheduler import RandomActivationByTypeFiltered
from dooders.agents import Prey, Predator, Food


class DooderSim(mesa.Model):
    """
    Wolf-Sheep Predation Model
    """

    height = 20
    width = 20

    initial_prey = 100
    initial_predator = 50

    prey_reproduce = 0.04
    predator_reproduce = 0.05

    predator_gain_from_food = 20

    food = False
    food_regrowth_time = 30
    prey_gain_from_food = 4

    verbose = False  # Print-monitoring

    description = (
        "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
    )

    def __init__(
        self,
        width=20,
        height=20,
        initial_prey=100,
        initial_predator=50,
        prey_reproduce=0.04,
        predator_reproduce=0.05,
        predator_gain_from_food=20,
        food=False,
        food_regrowth_time=30,
        prey_gain_from_food=4,
    ):
        """
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_prey: Number of sheep to start with
            initial_predator: Number of wolves to start with
            sheep_reproduce: Probability of each sheep reproducing each step
            predator_reproduce: Probability of each wolf reproducing each step
            predator_gain_from_food: Energy a wolf gains from eating a sheep
            grass: Whether to have the sheep eat grass for energy
            food_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            prey_gain_from_food: Energy sheep gain from grass, if enabled.
        """
        super().__init__()
        # Set parameters
        self.width = width
        self.height = height
        self.initial_prey = initial_prey
        self.initial_predator = initial_predator
        self.prey_reproduce = prey_reproduce
        self.predator_reproduce = predator_reproduce
        self.predator_gain_from_food = predator_gain_from_food
        self.food = food
        self.food_regrowth_time = food_regrowth_time
        self.prey_gain_from_food = prey_gain_from_food

        self.schedule = RandomActivationByTypeFiltered(self)
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=True)
        self.datacollector = mesa.DataCollector(
            {
                "Predator": lambda m: m.schedule.get_type_count(Predator),
                "Prey": lambda m: m.schedule.get_type_count(Prey),
                "Food": lambda m: m.schedule.get_type_count(
                    Food, lambda x: x.fully_grown
                ),
            }
        )

        # Create prey:
        for i in range(self.initial_prey):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.prey_gain_from_food)
            prey = Prey(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(prey, (x, y))
            self.schedule.add(prey)

        # Create predators
        for i in range(self.initial_predator):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.predator_gain_from_food)
            predator = Predator(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(predator, (x, y))
            self.schedule.add(predator)

        # Create food
        if self.food:
            for agent, x, y in self.grid.coord_iter():

                fully_grown = self.random.choice([True, False])

                if fully_grown:
                    countdown = self.food_regrowth_time
                else:
                    countdown = self.random.randrange(self.food_regrowth_time)

                patch = Food(self.next_id(), (x, y), self, fully_grown, countdown)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print(
                [
                    self.schedule.time,
                    self.schedule.get_type_count(Predator),
                    self.schedule.get_type_count(Prey),
                    self.schedule.get_type_count(Food, lambda x: x.fully_grown),
                ]
            )

    def run_model(self, step_count=200):

        if self.verbose:
            print("Initial number predators: ", self.schedule.get_type_count(Predator))
            print("Initial number prey: ", self.schedule.get_type_count(Prey))
            print(
                "Initial number food: ",
                self.schedule.get_type_count(Food, lambda x: x.fully_grown),
            )

        for i in range(step_count):
            self.step()

        if self.verbose:
            print("")
            print("Final number predators: ", self.schedule.get_type_count(Predator))
            print("Final number prey: ", self.schedule.get_type_count(Prey))
            print(
                "Final number food: ",
                self.schedule.get_type_count(Food, lambda x: x.fully_grown),
            )
