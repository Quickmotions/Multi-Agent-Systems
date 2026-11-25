class Route:
    def __init__(self, id, length, direction, dest, origin):
        self.id: int = id
        self.destination_id: int = dest
        self.origin_id: int = origin
        self.length: int = length
        self.vehicles: list[int] = []
        self.direction: int = direction
        self.space_left = length

    def add_vehicle(self, vehicle):
        self.vehicles.append(self.vehicles)
        self.space_left -= vehicle.size

    def remove_vehicle(self, vehicle):
        self.vehicles.remove(vehicle)
        self.space_left += vehicle.size

class TrafficLight:
    def __init__(self):
        # lists include list of the origin nodes (not dest)
        self.green_nodes = []
        self.red_nodes = []
        self.delay = 10

    def set_green(self, routes):
        self.green_nodes = routes

    def set_red(self, routes):
        self.red_nodes = routes

    def set_delay(self, time):
        self.delay = time
    
    def change_state(self, tick):
        if (tick % self.delay == 0):
            new_red = self.green_nodes
            self.green_nodes = self.red_nodes
            self.red_nodes = new_red

class RoundRobinTrafficLight(TrafficLight):
    def __init__(self):
        super().__init__()

    def change_state(self):
        new_green = self.red_nodes[0]
        self.red_nodes = self.red_nodes.pop(0) + self.green_nodes
        self.green_nodes = [new_green]
    
class Intersection:
    def __init__(self, number):
        self.id: int = number
        self.routes: list[Route] = []
        self.traffic_light = None

    def has_route(self, destination):
        for route in self.routes:
            if route.destination_id == destination:
                return True

    def add_route(self, route_id, direction, dest, length):
        new_route = Route(route_id, length, direction, dest, origin=self.id)
        self.routes.append(new_route)

    def add_traffic_light(self, traffic_light):
        self.traffic_light = traffic_light

    def update_traffic_light(self, tick):
        self.traffic_light.change_state(tick)