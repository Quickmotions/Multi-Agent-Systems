import heapq


class Agent:

    def __init__(self, id, speed, velocity, size, starting_pos):
        self.id = id
        self.max_speed: float = speed
        self.destination_node_id: int = 0
        self.size: int = size
        self.velocity: float = velocity
        self.current_speed: float = 0
        self.break_power: float = 20
        self.route: list[int] = []
        self.position = starting_pos # last interacted Node
        self.padding: float = 2
        self.distance_along_route: int = 0
        self.has_reached_destination = False

    def info(self) -> str:
        return f"{self.id} - pos {self.position} @ {self.distance_along_route}m, travelling at {self.current_speed}m/t"
    
    def calculate_route(self, current_node_id, nodes):
        # Dijkstra's Algorithm pathfinding
        self.route = []
        node_by_id = {node.id: node for node in nodes}
        if current_node_id not in node_by_id:
            raise ValueError(f"Unknown starting node: {current_node_id}")
        if self.destination_node_id not in node_by_id:
            raise ValueError(f"Unknown destination node: {self.destination_node_id}")

        distances = {current_node_id: 0}
        previous = {}
        pending = [(0, current_node_id)]
        while pending:
            distance, node_id = heapq.heappop(pending)
            if distance != distances[node_id]:
                continue
            if node_id == self.destination_node_id:
                break

            for route in node_by_id[node_id].routes:
                if route.destination_id not in node_by_id:
                    raise ValueError(f"Unknown node on route: {route.destination_id}")
                new_distance = distance + route.length
                if new_distance < distances.get(route.destination_id, float("inf")):
                    distances[route.destination_id] = new_distance
                    previous[route.destination_id] = node_id
                    heapq.heappush(pending, (new_distance, route.destination_id))

        if self.destination_node_id not in distances:
            return

        node_id = self.destination_node_id
        while node_id != current_node_id:
            self.route.append(node_id)
            node_id = previous[node_id]
        self.route.reverse()

    def set_destination(self, destination_id, mas):
        self.destination_node_id = destination_id
        self.calculate_route(self.position, mas.nodes)
        mas.get_intersection(self.position).add_vehicle_to_route(self.route[0], self)

    def get_next_action(self) -> int:
        if len(self.route) < 1:
            return None
        return self.route[0]

    def node_reached(self, origin_node, destination_node):
        self.distance_along_route = 0
        origin_node.remove_vehicle_from_route(self.route[0], self)
        if len(self.route) > 1: 
            destination_node.add_vehicle_to_route(self.route[1], self)
        else:
            print(ValueError("no new destination route"))
        self.position = self.route[0]
        self.route.pop(0)


    def increase_speed(self):
            self.current_speed += self.velocity
            if self.current_speed > self.max_speed:
                self.current_speed = self.max_speed

    def stop_speed(self):
        self.current_speed -= self.break_power
        if self.current_speed < 0:
            self.current_speed = 0

    def move_along_route(self, distance):
        self.distance_along_route += distance

    def update_movement(self, mas):

        # 1. Check Destination
        next_node = mas.get_intersection(id=self.get_next_action())
        if next_node is None: # Reached destination
            self.has_reached_destination = True
            self.stop_speed()
            return 0

        # 2. Check Route
        for route in mas.nodes[self.position].routes:
            if route.destination_id == next_node.id:
                current_route = route
                break
        else:
            raise ValueError(f"Vehicle {self.id} cannot find route on node {self.position} based on next route {next_node}")
        
        last_node = mas.get_intersection(id=self.position)

        # 3. End of Current Route -> check for space and green light
        if self.distance_along_route >= current_route.length:
            # No space
            if self.size + self.padding > current_route.space_left:
                self.stop_speed()
                self.distance_along_route = route.length
                print(f"Agent {self.id} has no space to join intersection")
                return 
            # Red Light
            traffic_light = next_node.traffic_light
            if traffic_light and last_node.id in traffic_light.red_nodes:
                self.stop_speed()
                self.distance_along_route = current_route.length
                print(f"Agent {self.id} has reached a red light")
                return 

            self.node_reached(last_node, next_node)

        # 4. On Route -> check space ahead, accellerate

        next_space_on_route = last_node.get_next_space_on_route(current_route.destination_id)
        print(f"DEBUG: next space avliable on route @ {next_space_on_route}m")

        self.increase_speed()
        self.move_along_route(self.current_speed)

    