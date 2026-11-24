from intersection import Intersection
from visualisation import NetworkVisualiser
from Agents.car import Car

class Enviroment:
    def __init__(self):
        self.nodes: list[Intersection] = []
        self.next_route_id = 0


    def add_node(self):
        self.nodes.append(Intersection(len(self.nodes)))

    def add_route(self, node_id, destination, length, direction):
        self.nodes[node_id].add_route(
            route_id=self.next_route_id,
            direction=direction,
            dest=destination,
            length=length,
        )
        self.next_route_id += 1

    def visualise(self):
        NetworkVisualiser().visualise(self.nodes)
        

if __name__ == "__main__":
    mas = Enviroment()
    mas.add_node()
    mas.add_node()
    mas.add_node()

    mas.add_route(node_id=0, destination=1, length=10, direction=180)
    mas.add_route(node_id=1, destination=0, length=10, direction=180+180)
    mas.add_route(node_id=0, destination=2, length=14, direction=90)
    mas.add_route(node_id=2, destination=0, length=14, direction=90+180)

    mas.add_route(node_id=1, destination=2, length=23, direction=45)
    mas.add_route(node_id=2, destination=1, length=23, direction=45+180)


    mas.visualise()

    car = Car(speed=4, size=2, starting_pos=1)
    car.set_destination(2, mas.nodes)

    print(car.route)