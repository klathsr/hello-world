"""
Chawanagorn Thiangsiri
673040660-7
Lab4-4 P1
"""

from room import Bedroom, Kitchen
    
if __name__ == "__main__":
    bedroom1 = Bedroom(12, 10, "kingSize")
    print(bedroom1.get_purpose())
    print(bedroom1.describe_room())
    print(bedroom1.calculate_area())
    print(bedroom1.get_recommended_lighting())
    print()
    kitchen1 = Kitchen(15, 12, has_island=True)
    print(kitchen1.get_purpose())
    print(kitchen1.describe_room())
    print(kitchen1.calculate_area())
    print(kitchen1.calculate_counter_space())
    print(kitchen1.get_recommended_lighting())

    print(kitchen1.calculate_counter_space.__doc__)