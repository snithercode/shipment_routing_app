from loader import Loader

# Initializes the Loader with the provided CSV files and sets up 'loader' and 'trucks'
# as global variables for universal access across modules.

loader = Loader('csv/package_data.csv', 'csv/street_addresses.csv', 'csv/distance_table.csv')
trucks = []
