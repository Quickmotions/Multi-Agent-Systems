import asyncio
import numpy as np
import random


class Garden:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        # 0 = empty
        # 1 = flower
        # 2 = bee
        # 3 = hive
        self.grid = np.zeros((height, width), dtype=int)

        self.flowers = {}

        self.hive_position = (0, 0)
        self.grid[0][0] = 3

    def add_flowers(self, number):

        for _ in range(number):

            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            while self.grid[y][x] != 0:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)

            self.grid[y][x] = 1

            # Different flowers produce different pollen amounts
            self.flowers[(x, y)] = random.randint(1, 5)

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

        # Remove old position
        if (bee.x, bee.y) == self.hive_position:
            self.grid[bee.y][bee.x] = 3
        else:
            self.grid[bee.y][bee.x] = 0

        # Update position
        bee.x = new_x
        bee.y = new_y

        # Update grid
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
                "pollen"
            )

            # Remove flower from environment
            del self.flowers[position]

            # Remove from bee's memory
            bee.known_flowers.discard(position)

            self.grid[bee.y][bee.x] = 2

    def return_to_hive(self, bee):

        if (bee.x, bee.y) == self.hive_position:

            if bee.pollen > 0:

                print(
                    bee.name,
                    "returned to hive with",
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


class Bee:

    def __init__(self, name, hive_position):

        self.name = name

        self.x = 0
        self.y = 0

        # Agent's internal knowledge
        self.known_flowers = set()
        self.explored = set()

        self.hive_position = hive_position

        self.pollen = 0
        self.total_pollen = 0

        self.pollen_limit = 5

    async def perceive(self, environment):

        percept = environment.get_percept(self)

        # Remember explored position
        self.explored.add((self.x, self.y))

        # Remember discovered flowers
        if percept["flower"]:

            position = (self.x, self.y)

            if position not in self.known_flowers:

                self.known_flowers.add(position)

                print(
                    self.name,
                    "discovered flower at",
                    position
                )

    def choose_target(self, environment):

        # Remove flowers that have already been collected
        self.known_flowers = {
            flower for flower in self.known_flowers
            if flower in environment.flowers
        }

        # Return home if carrying enough pollen
        if self.pollen >= self.pollen_limit:
            return self.hive_position

        # Return home if carrying pollen but no flowers are known
        if self.pollen > 0 and not self.known_flowers:
            return self.hive_position

        # Visit known flower
        if self.known_flowers:
            return random.choice(list(self.known_flowers))

        # Explore
        return None

    async def move_towards(self, target, environment):

        if target is None:

            # Random exploration
            directions = [
                (0, -1),
                (0, 1),
                (-1, 0),
                (1, 0)
            ]

            dx, dy = random.choice(directions)

        else:

            target_x, target_y = target

            dx = 0
            dy = 0

            if self.x < target_x:
                dx = 1

            elif self.x > target_x:
                dx = -1

            elif self.y < target_y:
                dy = 1

            elif self.y > target_y:
                dy = -1

        moved = environment.move_bee(
            self,
            dx,
            dy
        )

        if moved:

            print(
                self.name,
                "moved to",
                (self.x, self.y)
            )

        # Give other agents a chance to run
        await asyncio.sleep(0.2)

    async def run(self, environment, steps):

        for _ in range(steps):

            # PERCEIVE
            await self.perceive(environment)

            # COLLECT
            environment.collect_pollen(self)

            # RETURN TO HIVE
            environment.return_to_hive(self)

            # DECIDE
            target = self.choose_target(environment)

            # ACT
            await self.move_towards(
                target,
                environment
            )


async def main():

    # Create environment
    garden = Garden(10, 10)

    # Add flowers
    garden.add_flowers(15)

    # Create agents
    bees = [
        Bee("Bee 1", garden.hive_position),
        Bee("Bee 2", garden.hive_position),
        Bee("Bee 3", garden.hive_position)
    ]

    # Place agents
    for bee in bees:
        garden.add_bee(bee)

    garden.display()

    # Run ALL agents concurrently
    await asyncio.gather(
        *(bee.run(garden, 50) for bee in bees)
    )

    # Results
    print("\nFINAL RESULTS")

    for bee in bees:

        print(
            bee.name,
            "collected",
            bee.total_pollen,
            "total pollen"
        )

        print(
            "Known flowers:",
            bee.known_flowers
        )

        print(
            "Explored:",
            len(bee.explored)
        )


asyncio.run(main())