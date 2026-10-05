import numpy as np
import random


# ==========================================
# Environment
# ==========================================

class Garden:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        # 0 = empty
        # 1 = flower
        # 2 = bee
        # 3 = hive
        self.grid = np.zeros((height, width), dtype=int)

        # Store flowers separately so they can have
        # different pollen amounts
        self.flowers = {}

        # Hive position
        self.hive_position = (0, 0)
        self.grid[0][0] = 3

    def add_flowers(self, number):

        for _ in range(number):

            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            # Don't put flowers on the hive
            while self.grid[y][x] != 0:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)

            # Each flower starts with a random pollen amount
            pollen = random.randint(1, 5)

            self.grid[y][x] = 1
            self.flowers[(x, y)] = pollen

    def add_bee(self, bee):

        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)

        while self.grid[y][x] != 0:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

        bee.x = x
        bee.y = y

        self.grid[y][x] = 2

    def get_percept(self, bee):
        """
        Tell the bee what it can currently perceive.

        For this simple version the bee can see the
        square it is currently standing on.
        """

        position = (bee.x, bee.y)

        if position in self.flowers:
            return {
                "flower": True,
                "pollen": self.flowers[position]
            }

        return {
            "flower": False
        }

    def move_bee(self, bee, dx, dy):

        new_x = bee.x + dx
        new_y = bee.y + dy

        # Check boundaries
        if new_x < 0 or new_x >= self.width:
            return False

        if new_y < 0 or new_y >= self.height:
            return False

        # Don't move onto another bee
        if self.grid[new_y][new_x] == 2:
            return False

        # Remove bee from old position
        self.grid[bee.y][bee.x] = 0

        # Move bee
        bee.x = new_x
        bee.y = new_y

        # Place bee on new position
        self.grid[new_y][new_x] = 2

        return True

    def collect_pollen(self, bee):

        position = (bee.x, bee.y)

        if position in self.flowers:

            pollen = self.flowers[position]

            bee.pollen += pollen

            print(
                bee.name,
                "collected",
                pollen,
                "pollen at",
                position
            )

            # Remove flower from garden
            del self.flowers[position]

            # Make grid square empty
            self.grid[bee.y][bee.x] = 2

    def return_to_hive(self, bee):

        if (bee.x, bee.y) == self.hive_position:

            print(
                bee.name,
                "returned to the hive with",
                bee.pollen,
                "pollen"
            )

            bee.total_pollen += bee.pollen

            bee.pollen = 0

    def display(self):

        print()

        for row in self.grid:
            print(" ".join(str(cell) for cell in row))

        print()


# ==========================================
# Bee Agent
# ==========================================

class Bee:

    def __init__(self, name, hive_position):

        self.name = name

        # Current position
        self.x = 0
        self.y = 0

        # Internal knowledge
        self.known_flowers = set()
        self.explored = set()

        # Hive is known from the beginning
        self.hive_position = hive_position

        # Current pollen
        self.pollen = 0

        # Total pollen delivered to hive
        self.total_pollen = 0

        # Return to hive after collecting this much
        self.pollen_limit = 10

    # --------------------------------------
    # Perception
    # --------------------------------------

    def perceive(self, environment):

        percept = environment.get_percept(self)

        # Remember that this position has been explored
        self.explored.add((self.x, self.y))

        # If a flower is discovered, remember it
        if percept["flower"]:

            position = (self.x, self.y)

            self.known_flowers.add(position)

            print(
                self.name,
                "discovered flower at",
                position
            )

    # --------------------------------------
    # Decide what to do
    # --------------------------------------

    def choose_target(self):

        # If carrying too much pollen, go home
        if self.pollen >= self.pollen_limit:
            return self.hive_position

        # If we know about flowers, go to one
        if self.known_flowers:

            return random.choice(
                list(self.known_flowers)
            )

        # Otherwise explore randomly
        return None

    # --------------------------------------
    # Move towards target
    # --------------------------------------

    def move_towards(self, target, environment):

        if target is None:

            # Random exploration
            directions = [
                (0, -1),
                (0, 1),
                (-1, 0),
                (1, 0)
            ]

            dx, dy = random.choice(directions)

            environment.move_bee(
                self,
                dx,
                dy
            )

            return

        target_x, target_y = target

        dx = 0
        dy = 0

        # Move horizontally first
        if self.x < target_x:
            dx = 1

        elif self.x > target_x:
            dx = -1

        # Otherwise move vertically
        elif self.y < target_y:
            dy = 1

        elif self.y > target_y:
            dy = -1

        # Already at target
        else:
            return

        environment.move_bee(
            self,
            dx,
            dy
        )

    # --------------------------------------
    # Agent update
    # --------------------------------------

    def update(self, environment):

        # 1. Perceive environment
        self.perceive(environment)

        # 2. Collect pollen if standing on flower
        environment.collect_pollen(self)

        # 3. If at hive, unload pollen
        environment.return_to_hive(self)

        # 4. Choose what to do
        target = self.choose_target()

        # 5. Move towards target
        self.move_towards(
            target,
            environment
        )


# ==========================================
# Create Environment
# ==========================================

garden = Garden(10, 10)

garden.add_flowers(15)


# ==========================================
# Create Multiple Agents
# ==========================================

bees = [
    Bee("Bee 1", garden.hive_position),
    Bee("Bee 2", garden.hive_position),
    Bee("Bee 3", garden.hive_position)
]


# Add bees to garden
for bee in bees:
    garden.add_bee(bee)


# ==========================================
# Run Simulation
# ==========================================

for step in range(50):

    print("\n==============================")
    print("STEP", step)
    print("==============================")

    # Each bee gets a turn
    for bee in bees:

        bee.update(garden)

    # Display garden
    garden.display()


# ==========================================
# Display Bee Knowledge
# ==========================================

print("\nFINAL BEE KNOWLEDGE")
print("==============================")

for bee in bees:

    print("\n", bee.name)

    print(
        "Known flowers:",
        bee.known_flowers
    )

    print(
        "Explored locations:",
        len(bee.explored)
    )

    print(
        "Total pollen delivered:",
        bee.total_pollen
    )