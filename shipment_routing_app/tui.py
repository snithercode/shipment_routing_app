import os
from datetime import timedelta
from globals import loader, trucks


# Function to clear the console view
# Time-Complexity: O(1) / Space-Complexity: O(1)
def clear_view():
    # Check if it's Windows or Linux/Mac and use the appropriate clear screen command
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


# For displaying the main menu
# Time-Complexity: O(1) / Space-Complexity: O(1)
# Just prints a static set of strings.
def main_menu():
    print('-' * 120)
    print('WGUPS Main Menu')
    print('1. View EOD report for all packages and truck mileage')
    print('2. View EOD report for a single package record with a package ID')
    print('3. View a report snapshot for all package records at a specific time')
    print('4. View a report snapshot for a single package record at a specific time')
    print('5. End Program')
    print('-' * 120)


# For printing the header in package record views. Formats column spacing
# Time-Complexity: O(1) / Space-Complexity: O(1)
def print_package_layout():
    print(
        '\n{:<3} {:<38} {:<16} {:<7} {:<5} {:<9} {:<5} {:<10} {:<12}'.format('PID', 'Address', 'City', 'Zipcode',
                                                                             'Kilos', 'Deadline', 'Truck',
                                                                             'Status', 'Delivery Completed'))
    print('-' * 120)


# For printing package record details with proper spacing
# Time-Complexity: O(1) / Space-Complexity: O(1)
# Simply formats and prints the attributes of a single package
def print_package_info(package):
    print('{:<3} {:<38} {:<16} {:<7} {:<5} {:<9} {:<5} {:<10} {:<12}'.format(package.id, package.address,
                                                                             package.city, package.zipcode,
                                                                             package.weight,
                                                                             package.delivery_commitment_time,
                                                                             package.assigned_truck if package.assigned_truck is not None else "",
                                                                             package.status,
                                                                             str(
                                                                                 package.delivery_time) if package.delivery_time is not None else ""))


# Function to display alternate menu options
# Time-Complexity: O(1) / Space-Complexity: O(1)
# Just prints a static set of strings and captures single user input
def alt_menu_options():
    print('-' * 120)
    print('1. Return to Main Menu')
    print('2. End Program')
    print('-' * 120)
    return int(input('\nEnter one of the options above to continue: '))


# Function to display current time
# Time-Complexity: O(1) / Space-Complexity: O(1)
def display_time(time):
    print('\nCurrent time: ', time.time(), '\n')


# Function to: View EOD report for all packages and truck mileage
# Time-Complexity: O(n) / Space-Complexity: O(1)
# Iterates through all packages in the hashtable once. Space used is constant.
def view_all_packages():
    clear_view()
    print_package_layout()

    for i in range(len(loader.hashtable.table)):
        package = loader.hashtable.lookup(i + 1)
        if package is not None:
            print_package_info(package)

    total_distance_traveled = 0

    for truck in trucks:
        total_distance_traveled += truck.distance_traveled
    print('\nTotal distance traveled by trucks: ', round(total_distance_traveled, 2), 'miles', '\n')

    return alt_menu_options()


# Function to: View a specific package record with a package ID
# Time-Complexity: O(n) worst-case, O(1) average-case / Space-Complexity: O(1)
# Performs a hashtable lookup which has O(1) average-case complexity. Space used is constant.
def view_package_by_id():
    # Ask user to enter a package id. If input is invalid (can't be converted to int), ask again.
    while True:
        clear_view()
        package_id_input = input('\nEnter a package ID: ')
        try:
            package_id = int(package_id_input)
            package = loader.hashtable.lookup(package_id)

            if package is not None:
                print_package_layout()
                print_package_info(package)
                return alt_menu_options()
            else:
                print('\nPackage ID not found. Please try again.')
                input('\nPress Enter to continue...')

        except ValueError:
            print('\nInvalid ID. Please enter a valid package ID.')
            input('\nPress Enter to continue...')


# Function to:  View a snapshot of package records at a specific time
# Time-Complexity: O(n) / Space-Complexity: O(1)
# Iterates through all packages in the hashtable once. Space used is constant.
def view_packages_by_time():
    # Ask user to enter a time for the snapshot. If input is invalid, ask again.
    while True:
        clear_view()
        time_snapshot_str = input('\nEnter a time in HH:MM:SS format: ')
        try:
            h, m, s = map(int, time_snapshot_str.split(':'))
            if 0 <= h < 24 and 0 <= m < 60 and 0 <= s < 60:
                time_snapshot = timedelta(hours=h, minutes=m, seconds=s)
                break
        except ValueError:
            print('\nInvalid time. Please enter a valid time in HH:MM:SS format.')
            input('\nPress Enter to continue...')

    print_package_layout()

    for i in range(len(loader.hashtable.table)):
        package = loader.hashtable.lookup(i + 1)
        if package is not None:
            assigned_truck = next((truck for truck in trucks if truck.id == package.assigned_truck), None)
            if assigned_truck is not None:
                if time_snapshot < assigned_truck.hub_departure_time:
                    if 'Delayed on flight---will not arrive to depot until 9:05 am' in package.notes:
                        package.status = 'Delayed'
                    else:
                        package.status = 'At Hub'
                elif package.delivery_time is not None and time_snapshot >= package.delivery_time:
                    package.status = 'Delivered'
                else:
                    package.status = 'En Route'

            print('{:<3} {:<38} {:<16} {:<7} {:<5} {:<9} {:<5} {:<10} {:<12}'.format(package.id, package.address,
                                                                                     package.city, package.zipcode,
                                                                                     package.weight,
                                                                                     package.delivery_commitment_time,
                                                                                     package.assigned_truck if package.assigned_truck is not None else "",
                                                                                     package.status,
                                                                                     str(
                                                                                         package.delivery_time) if package.delivery_time is not None and package.status == 'Delivered' else ""))
    return alt_menu_options()


# Function to:  View a snapshot of a single package record at a specific time
# Time-Complexity: O(n) / Space-Complexity: O(1)
# Performs hashtable lookup for the package and checks status at the specified time. Space used is constant.
def view_package_by_time_and_id():
    # Ask user to enter a time for the snapshot and a package ID. If input is invalid, ask again.
    while True:
        clear_view()
        time_snapshot_str = input('\nEnter a time in HH:MM:SS format: ')
        package_id_input = input('\nEnter a package ID: ')
        try:
            h, m, s = map(int, time_snapshot_str.split(':'))
            package_id = int(package_id_input)
            if 0 <= h < 24 and 0 <= m < 60 and 0 <= s < 60:
                time_snapshot = timedelta(hours=h, minutes=m, seconds=s)
                package = loader.hashtable.lookup(package_id)
                if package is not None:
                    break
        except ValueError:
            print('\nInvalid time or package ID. Please enter a valid time in HH:MM:SS format and a valid package ID.')
            input('\nPress Enter to continue...')

    print_package_layout()
    assigned_truck = next((truck for truck in trucks if truck.id == package.assigned_truck), None)
    if assigned_truck is not None:
        if time_snapshot < assigned_truck.hub_departure_time:
            if 'Delayed on flight---will not arrive to depot until 9:05 am' in package.notes:
                package.status = 'Delayed'
            else:
                package.status = 'At Hub'
        elif package.delivery_time is not None and time_snapshot >= package.delivery_time:
            package.status = 'Delivered'
        else:
            package.status = 'En Route'

    print('{:<3} {:<38} {:<16} {:<7} {:<5} {:<9} {:<5} {:<10} {:<12}'.format(package.id, package.address,
                                                                             package.city, package.zipcode,
                                                                             package.weight,
                                                                             package.delivery_commitment_time,
                                                                             package.assigned_truck if package.assigned_truck is not None else "",
                                                                             package.status,
                                                                             str(
                                                                                 package.delivery_time) if package.delivery_time is not None and package.status == 'Delivered' else ""))
    return alt_menu_options()


# Runs the text-based user interface
# Time-Complexity: O(n) for each option selection / Space-Complexity: O(1)
# Depending on the user's selection, different functions are called, but space used is constant.
def run_tui():
    # Loop running tui until user opts to exit
    while True:
        # Loop to handle input validation
        while True:
            clear_view()
            main_menu()
            try:
                option = int(input('\nEnter one of the options above to continue: '))
                if 1 <= option <= 5:
                    break  # If a valid integer is given, break the loop
                else:
                    print('\nInvalid option. Please try again.')
                    input('\nPress Enter to continue...')
            except ValueError:  # If the input couldn't be converted to an integer, ask again
                print('\nInvalid option. Please try again.')
                input('\nPress Enter to continue...')

        if option == 1:
            option = view_all_packages()
            if option == 1:
                continue
            elif option == 2:
                break
        elif option == 2:
            option = view_package_by_id()
            if option == 1:
                continue
            elif option == 2:
                break
        elif option == 3:
            option = view_packages_by_time()
            if option == 1:
                continue
            elif option == 2:
                break
        elif option == 4:
            option = view_package_by_time_and_id()
            if option == 1:
                continue
            elif option == 2:
                break
        elif option == 5:
            break
