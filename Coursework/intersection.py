class Route:
    def __init__(self, id, length, direction, dest, origin):
        self.id: int = id
        self.destination_id: int = dest
        self.origin_id: int = origin
        self.length: int = length
        self.vehicles: list[int] = []
        self.direction: int = direction
        
class Intersection:
    def __init__(self, number):
        self.id: int = number
        self.routes: list[Route] = []

    def has_route(self, destination):
        for route in self.routes:
            if route.destination_id == destination:
                return True

    def add_route(self, route_id, direction, dest, length):
        new_route = Route(route_id, length, direction, dest, origin=self.id)
        self.routes.append(new_route)
