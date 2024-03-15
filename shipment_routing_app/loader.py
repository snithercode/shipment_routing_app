import csv
from hash_table import HashTable
from package import Package

# Creating the hash table
# Time-Complexity: O(1) / Space-Complexity: O(n)
hashtable = HashTable()


class Loader:

    # Init the Loader with three files for packages, addresses and distances
    # Time-Complexity: O(n) / Space-Complexity: O(n)
    # Time and space complexity of this constructor depends on the three load methods called,
    # each of which scales linearly with the size of the input files.
    def __init__(self, packages_file, addresses_file, distances_file):
        self.hashtable = Loader.load_packages(packages_file)
        self.addresses = Loader.load_addresses(addresses_file)
        self.distances = Loader.load_distances(distances_file)

    # Reads package data from file and inserts package objects into a hash table.
    # Time-Complexity: O(n) / Space-Complexity: O(n)
    # Reads each package once from the file, creates a package object, and inserts it into the hash table.
    # Time complexity scales linearly with the number of packages. Stores all the package objects in a hash table,
    # resulting in space complexity that also scales linearly with the number of packages.
    @staticmethod
    def load_packages(file_path):
        # Open the file
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            # Read each row in the file
            for row in reader:
                # Get the package details from the row
                package_id = int(row[0])
                address = row[1]
                city = row[2]
                state = row[3]
                zipcode = row[4]
                delivery_commitment_time = row[5]
                weight = row[6]
                notes = row[7]
                assigned_truck = 0
                # Determine status based on notes
                if 'Delayed on flight---will not arrive to depot until 9:05 am' in notes:
                    status = 'Delayed'
                else:
                    status = 'At Hub'
                delivery_time = None
                # Create a new package object
                package = Package(package_id, address, city, state, zipcode, delivery_commitment_time, weight, notes,
                                  assigned_truck, status, delivery_time)
                # Insert the package into the hash table
                hashtable.insert(package)
        return hashtable

    # Reads address data from file and stores them in a list
    # Time-Complexity: O(n) / Space-Complexity: O(n)
    # Reads the file once, creating a dictionary for each address and adding it to the list.So, time complexity scales
    # linearly with num of addresses. Stores all the address dictionaries in a list, resulting in space complexity that
    # scales linearly with the number of addresses.
    @staticmethod
    def load_addresses(file_path):
        # Initialize empty list for addresses
        addresses = []
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            # For each row, get the address and its id
            for row in reader:
                address_id = row[0]
                address = row[2]
                # Add the address to the list
                addresses.append({'address': address, 'address_id': address_id})
        return addresses

    # Reads distance data from file and stores them in a 2D list (table)
    # Time-Complexity: O(n) / Space-Complexity: O(n)
    # Goes through each cell in the file once, scaling linearly with the total number of distance entries in the file.
    # Stores all the distances in a 2D list, so space complexity also scales linearly with the num of distance entries.
    @staticmethod
    def load_distances(file_path):
        # Initialize the table for distances
        distance_table = []
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            # For each row in the file, get the distance
            for row in reader:
                distance_row = []
                for val in row:
                    if val == '':
                        distance_row.append(None)
                    else:
                        # Convert the value to float before adding to distance_row
                        distance_row.append(float(val))
                # Add the row of distances to the table
                distance_table.append(distance_row)
        return distance_table

    # Returns id of the address that matches the given package's address
    # Time-Complexity: O(n) / Space-Complexity: O(1)
    # In worst-case scenario, iterates over all addresses to find match. Scales linearly with the num of addresses.
    # Does not use any additional space that grows with the input size, space complexity is constant.
    def get_address_id(self, package_id):
        # Lookup the package by id
        matching_package = self.hashtable.lookup(package_id)
        # For each address, if the address matches the package address, return the address id
        for address in self.addresses:
            if package_id == 0:
                return address['address_id']
            elif address['address'] == matching_package.address:
                return address['address_id']
