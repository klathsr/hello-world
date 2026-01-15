from abc import ABC, abstractmethod

class Room(ABC):
    def __init__(self, length, width):
        self.length = length
        self.width = width
    
    @abstractmethod
    def get_purpose(self):
        """Returns a string describing purposes of the room"""
        pass

    @abstractmethod
    def get_recommended_lighting(self):
        """Returns recommended lighting in lumens per square foot"""
        pass

    def calculate_area(self):
         return self.length * self.width
    
    def describe_room(self):
        area = self.calculate_area()
        return f"A {self.__class__.__name__} of {area} sq ft used for {self.get_purpose()}"

class Bedroom(Room):
    def __init__(self, length, width, bed_size):
        super().__init__(length, width)
        self.bed_size = bed_size

    
    def get_purpose(self):
        return f"For Sleeping"

   
    def get_recommended_lighting(self):
       return f"10-20 lumens per sq ft"

class Kitchen(Room):
    def __init__(self, length, width,has_island = True):
        super().__init__(length, width)
        self.has_island = has_island

    
    def get_purpose(self):
        return f"For Cooking"

    
    def get_recommended_lighting(self):
       return f"70-80 lumens per sq ft"


    def calculate_counter_space(self):
        """
        Calculates the available counter space in the kitchen.

        The counter space is divided into island counter space and wall counter space
        based on whether the kitchen has an island.

        Returns:
        tuple[float, float]: A tuple containing:
        - island_area: Counter space provided by the island (in square feet)
        - wall_area: Counter space along the walls (in square feet)
        """
        total_area = self.calculate_area()

        if self.has_island:
            island_area = total_area / 5
            wall_area = total_area / 4
        else:
            island_area = 0
            wall_area = total_area / 2

        return island_area, wall_area