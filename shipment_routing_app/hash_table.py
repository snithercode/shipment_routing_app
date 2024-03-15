from typing import List
from package import Package


class HashTable:

    # Method for initializing an empty hash table which will store our packages
    # Time-Complexity: O(n) / Space-Complexity: O(n)
    # Time and space complexity is proportional to table size (creating n empty lists)
    def __init__(self, table_size=41):
        self.table = [[] for _ in range(table_size)]

    # Modulo Hash Method which uses the remainder from division of the key
    # Time-Complexity: O(1) / Space-Complexity: O(1)
    # Constant time and space complexity due to a single modulo operation
    def hash(self, key):
        return key % len(self.table)

    # Method for inserting package objects into the hash table
    # Time-Complexity: O(n) / Space-Complexity: O(n)
    # Worst case is linear time complexity due to key collisions, space complexity increases with added elements
    def insert(self, package: Package):
        hash_index = self.hash(package.id)
        bucket: List[Package] = self.table[hash_index]

        # Find if a package with the same id is already in the bucket
        for i, existing_package in enumerate(bucket):
            # If yes, we will overwrite it with the new package
            if package.id == existing_package.id:
                bucket[i] = package
                break
        else:
            # If not, append the new package to the bucket
            bucket.append(package)

    # Method to lookup a package object by its id
    # Time-Complexity: O(n) / Space-Complexity: O(1)
    # Worst case is linear time complexity due to key collisions, no additional space required for the lookup
    def lookup(self, package_id):
        hash_index = self.hash(package_id)
        bucket: List[Package] = self.table[hash_index]

        # Finding the package
        for existing_package in bucket:
            if package_id == existing_package.id:
                return existing_package
        return None
