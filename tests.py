"""
file: tests.py
description: Verify the chained hash map class implementation
"""

__author__ = ["NAME", "NAME"]

from hashmap import HashMap


def print_map(a_map):
    for word, counter in a_map:  # uses the iter method
        print(word, counter, end=" ")
    print()


def test0():
    table = HashMap(initial_num_buckets=10)
    table.add("to", 1)
    table.add("do", 1)
    table.add("is", 1)
    table.add("to", 2)
    table.add("be", 1)

    print_map(table)

    print("'to' in table?", table.contains("to"))
    print("'to' appears", table.get("to"), "times")
    table.remove("to")
    print("'to' in table?", table.contains("to"))

    print_map(table)


if __name__ == '__main__':
    test0()
