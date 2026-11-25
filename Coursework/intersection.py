class Route:
    def __init__(self, id, length, direction, dest, origin):
        self.id: int = id
        self.destination_id: int = dest
        self.origin_id: int = origin
        self.length: int = length
        self.vehicles = []
        self.direction: int = direction
        self.space_left = length

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
        self.space_left -= (vehicle.size + vehicle.padding)

    def remove_vehicle(self, vehicle):
        self.vehicles.remove(vehicle)
        self.space_left += (vehicle.size + vehicle.padding)

    
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

    def add_vehicle_to_route(self, route_id, vehicle):
        
        for route in self.routes:
            if route.destination_id == route_id:
                print(f"DEBUG: Added vehicle {vehicle.id} onto Node {self.id} Route {route.id} towards Node {route.destination_id}")
                route.add_vehicle(vehicle)
                return
        else:
            raise ValueError(f"ADD VEHICLE ERROR: Unable to find route {route_id} on node {self.id} for vehicle {vehicle.id}")

    def remove_vehicle_from_route(self, route_id, vehicle):
        for route in self.routes:
            if route.destination_id == route_id:
                print(f"DEBUG: Removed vehicle {vehicle.id} from Node {self.id} Route {route.id} towards Node {route.destination_id}")
                route.remove_vehicle(vehicle)
                return
        else:
            raise ValueError(f"REMOVE VEHICLE ERROR: Unable to find route {route_id} on node {self.id} for vehicle {vehicle.id}")


    def get_next_space_on_route(self, route_id) -> int:
        for route in self.routes:
            if route.destination_id == route_id:
                if len(route.vehicles) == 0:
                    return 0
                vehicle = route.vehicles[-1]
                return vehicle.distance_along_route + vehicle.size
        else:
            raise ValueError(f"GET ROUTE SPACE ERROR: : Unable to find route {route_id} on node {self.id}")