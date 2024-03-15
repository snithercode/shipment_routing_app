import datetime
from globals import loader, trucks
from truck import Truck
from nearest_neighbor import calculate_shortest_route, get_distance_between_nodes
from tui import run_tui


# Time-Complexity: O(n) / Space-Complexity: O(1)
# The time complexity is generally linear with the number of packages to be delivered (n), and the space complexity is
# constant since it only creates a few variables and does not depend on the input size.

# *Note: A poor hash function or a highly skewed dataset that leads to a high collision rate could theoretically cause
# the time complexity to degrade to O(n^2). However, this scenario is unlikely with a well thought out hash function and
# a balanced dataset.
def deliver_packages(truck, route):
    current_time = truck.hub_departure_time

    # Set status of all packages in the truck to "En Route"
    for package_id in truck.loaded_packages:
        package = loader.hashtable.lookup(package_id)
        package.status = 'En Route'

    for i in range(len(route) - 1):
        distance = get_distance_between_nodes(loader.get_address_id(route[i]), loader.get_address_id(route[i + 1]),
                                              loader.distances)
        travel_time = datetime.timedelta(hours=distance / truck.travel_speed)
        current_time += travel_time

        # Get the package from the hash table and update its delivery time and status
        delivered_package = loader.hashtable.lookup(route[i + 1])
        delivered_package.delivery_time = current_time
        delivered_package.status = 'Delivered'


# Time-Complexity: O(n^2) / Space-Complexity: O(n)
# Time complexity is mainly dictated by calculate_shortest_route function which uses a nearest neighbor approach.
# This approach has a quadratic time complexity because it iterates over the list of packages for every package (n^2).
# Space complexity is linear because it depends on the num of packages and the num of trucks.
def main():
    # Create trucks and manually load packages
    truck1 = Truck(1, [1, 7, 13, 14, 15, 16, 19, 20, 21, 29, 30, 34, 37, 39, 40], datetime.timedelta(hours=8))
    truck2 = Truck(2, [3, 5, 6, 18, 25, 26, 28, 31, 32, 36, 38],
                   datetime.timedelta(hours=9, minutes=5))
    truck3 = Truck(3, [2, 4, 8, 9, 10, 11, 12, 17, 22, 23, 24, 27, 33, 35], datetime.timedelta(hours=10, minutes=20))

    trucks.append(truck1)
    trucks.append(truck2)
    trucks.append(truck3)

    # Assign truck number to each package
    for truck in trucks:
        for loaded_package in truck.loaded_packages:
            package = loader.hashtable.lookup(loaded_package)
            package.assigned_truck = truck.id

    # Calculate shortest route for Truck 1 and Truck 2 and keep track of combined distance traveled

    route1, total_distance = calculate_shortest_route(truck1.current_location, truck1.loaded_packages)
    truck1.distance_traveled = round(total_distance, 2)

    route2, total_distance = calculate_shortest_route(truck2.current_location, truck2.loaded_packages)
    truck2.distance_traveled = round(total_distance, 2)

    # Truck 1 and Truck 2 deliver their loaded packages
    deliver_packages(truck1, route1)
    deliver_packages(truck2, route2)

    # Truck 1's driver finishes delivering loaded packages and will return to the hub to begin delivering
    # Truck 3's loaded packages at 10:20:00.

    # Package 9's address is updated
    package_to_update = loader.hashtable.lookup(9)
    package_to_update.address = '410 S State St'
    package_to_update.zipcode = '84111'

    # Calculate shortest route for Truck 3
    route3, total_distance = calculate_shortest_route(truck3.current_location, truck3.loaded_packages)
    truck3.distance_traveled = round(total_distance, 2)

    # Truck 3 delivers its loaded packages
    deliver_packages(truck3, route3)

    # Just some print statements for checking address routes and distances traveled for each individual truck
    # print(route1, 'Truck 1 Distance: ', truck1.distance_traveled)
    # print(route2, 'Truck 2 Distance: ', truck2.distance_traveled)
    # print(route3, 'Truck 3 Distance: ', truck3.distance_traveled)

    run_tui()


if __name__ == '__main__':
    main()
