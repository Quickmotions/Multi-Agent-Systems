import numpy as np
import random


class GridEnvironment:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Create an empty 2D grid
        # 0 = empty
        # 1 = food
        # 2 = agent
        self.grid = np.zeros((height, width), dtype=int)

    def add_food(self, number):
        """Randomly place food in the environment."""

        for _ in range(number):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            # Only place food on an empty square
            while self.grid[y][x] != 0:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)

            self.grid[y][x] = 1

    def add_agent(self, agent):
        """Add an agent to the environment."""

        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)

        # Find an empty position
        while self.grid[y][x] != 0:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

        agent.x = x
        agent.y = y

        self.grid[y][x] = 2

    def move_agent(self, agent, dx, dy):
        """Move an agent if the new position is inside the grid."""

        new_x = agent.x + dx
        new_y = agent.y + dy

        # Check that the new position is inside the grid
        if new_x < 0 or new_x >= self.width:
            return False

        if new_y < 0 or new_y >= self.height:
            return False

        # Don't move onto another agent
        if self.grid[new_y][new_x] == 2:
            return False

        # Check whether the agent has found food
        if self.grid[new_y][new_x] == 1:
            agent.food_collected += 1

        # Clear old position
        self.grid[agent.y][agent.x] = 0

        # Update agent position
        agent.x = new_x
        agent.y = new_y

        # Put agent into new position
        self.grid[new_y][new_x] = 2

        return True

    def display(self):
        """Print the current environment."""

        for row in self.grid:
            print(" ".join(str(cell) for cell in row))

        print()


class Agent:

    def __init__(self, name):
        self.name = name
        self.x = 0
        self.y = 0
        self.food_collected = 0

    def move_randomly(self, environment):
        """Move randomly in one of four directions."""

        directions = [
            (0, -1),  # up
            (0, 1),   # down
            (-1, 0),  # left
            (1, 0)    # right
        ]

        dx, dy = random.choice(directions)

        environment.move_agent(self, dx, dy)


# -----------------------------------
# Create the environment
# -----------------------------------

environment = GridEnvironment(10, 10)

# Add some food
environment.add_food(15)

# -----------------------------------
# Create multiple agents
# -----------------------------------

agents = [
    Agent("Bee 1"),
    Agent("Bee 2"),
    Agent("Bee 3")
]

# Add agents to environment
for agent in agents:
    environment.add_agent(agent)


# -----------------------------------
# Run the simulation
# -----------------------------------

for step in range(20):

    print("Step:", step)

    # Move every agent
    for agent in agents:
        agent.move_randomly(environment)

    # Display environment
    environment.display()


# -----------------------------------
# Print results
# -----------------------------------

for agent in agents:
    print(
        agent.name,
        "collected",
        agent.food_collected,
        "food"
    )