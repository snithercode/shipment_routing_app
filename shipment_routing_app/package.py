class Package:
    # Method for initializing instances of the Package class
    # Time-Complexity: O(1) / Space-Complexity: O(1)
    def __init__(self, id, address, city, state, zipcode, delivery_commitment_time, weight, notes, assigned_truck,
                 status, delivery_time):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.delivery_commitment_time = delivery_commitment_time
        self.weight = weight
        self.notes = notes
        self.assigned_truck = assigned_truck
        self.status = status
        self.delivery_time = delivery_time

    # Time-Complexity: O(1) / Space-Complexity: O(1)
    def __str__(self):
        return f'Package({self.id}, {self.address}, {self.city}, {self.state}, {self.zipcode},' \
               f' {self.delivery_commitment_time}, {self.weight}, {self.notes}, {self.assigned_truck},' \
               f' {self.status}, {self.delivery_time}) '

    # Method to generate an unambiguous string representation of the Package object that can be used for debugging
    # Time-Complexity: O(1) / Space-Complexity: O(1)
    def __repr__(self):
        return self.__str__()
