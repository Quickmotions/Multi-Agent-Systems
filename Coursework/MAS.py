from intersection import Intersection
from traffic_light import TrafficLight, RoundRobinTrafficLight
from visualisation import NetworkVisualiser
from Agents.car import Car
from Agents.agent import Agent

class Enviroment:
    def __init__(self):
        self.nodes: list[Intersection] = []
        self.next_route_id = 0
        self.tick = 0

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

    def get_intersection(self, id) -> Intersection:
        for node in self.nodes:
            if node.id == id:
                return node
        raise ValueError(f"MAS Cannot find node id {id}")

    def add_traffic_light(self, node_id, green, red, delay):
        tl = TrafficLight()
        tl.set_green(green)
        tl.set_red(red)
        tl.set_delay(delay)
        self.nodes[node_id].add_traffic_light(tl)


    def visualise(self):
        NetworkVisualiser().visualise(self.nodes)


    def update(self, vehicles: list[Agent], log: bool):
        if log: print(f"updating TICK {self.tick}:")

        # update traffic lights
        for node in self.nodes:
            if node.traffic_light:
                node.update_traffic_light(self.tick)

        # update agents    
        for agent in vehicles:
            if log: next_destination = agent.get_next_action()
            if log: print(f"Agent {agent.id} @ pos {agent.position}- Next detination = {next_destination}")
            agent.update_movement(self)

                
        self.tick += 1

if __name__ == "__main__":
    mas = Enviroment()
    
    mas.add_node()

    mas.add_node()
    mas.add_node()

    mas.add_route(node_id=0, destination=1, length=100, direction=180)
    mas.add_route(node_id=1, destination=0, length=100, direction=180+180)
    mas.add_route(node_id=0, destination=2, length=140, direction=90)
    mas.add_route(node_id=2, destination=0, length=140, direction=90+180)

    mas.add_route(node_id=1, destination=2, length=270, direction=45)
    mas.add_route(node_id=2, destination=1, length=270, direction=45+180)

    mas.add_traffic_light(node_id=0, green=[1], red=[2], delay=20)

    mas.visualise()

    vehicles: list[Agent] = []

    car = Car(id=0, speed=40, velocity=3, size=2, starting_pos=1)
    car.set_destination(2, mas)
    # print(car.route)
    vehicles.append(car)

    while True:
        mas.update(vehicles, log=True)
        print(vehicles[0].info())
        input("")

        for agent in vehicles:
            if agent.has_reached_destination:
                vehicles.remove(agent)


