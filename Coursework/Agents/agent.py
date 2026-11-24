import heapq


class Agent:

    def __init__(self, speed, size, starting_pos):
        self.movement_speed: float = speed
        self.destination_node_id: int = 0
        self.size: int = size
        self.velocity = 0
        self.current_speed = 0
        self.route: list[int] = []
        self.position = starting_pos

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
                if route.length < 0:
                    raise ValueError("Dijkstra requires non-negative route lengths")
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
        self.route.append(current_node_id)
        self.route.reverse()

    def set_destination(self, destination_id, nodes):
        self.destination_node_id = destination_id
        self.calculate_route(self.position, nodes)

    