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