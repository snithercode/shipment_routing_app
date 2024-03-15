class Truck:
    # Method for initializing instances of the Truck class
    # Time-Complexity: O(1) / Space-Complexity: O(1)
    def __init__(self, id, loaded_packages, hub_departure_time):
        self.id = id
        self.loaded_packages = loaded_packages  # Loaded packages (yet to be delivered)
        self.current_location = 0  # Assuming truck starts at hub
        self.travel_speed = 18
        self.hub_departure_time = hub_departure_time
        self.distance_traveled = 0
