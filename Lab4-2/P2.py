"""
Narudee Chakitdee
673040147-9
Lab4-2 P2
"""
from datetime import datetime

class Cat:
# 1. Class Attributes
    species = "Felis catus" # Scientific name for domestic cats 
    total_cats = 0 # Tracks total number of cats
    average_lifespan = 15 # Average cat lifespan 

# 2. Instance Attributes
def __init__(self, name, age, breed, color):
# Basic info
    self.name = name
    self.age = age
    self.breed = breed
    self.color = color
# State tracking
    self.hungry = False
    self.energy = 100
    self.happiness = 100

    Cat.total_cats += 1

# 3. Instance Methods
def meow(self):
    if self.hungry:
        print(f"{self.name}: Meow Meow Meow! (hungry)")
    elif self.energy < 30:
        print(f"{self.name}: Meowww... (sleepy)")
    elif self.happiness > 80:
        print(f"{self.name}: Meow ~ ~ (happiest)")
    else:
        print(f"{self.name}: Meow!")

def eat(self, food_amount):
    if food_amount < 0:
            return "No Food ? !"
        
    self.hungry = False
    self.energy = min(100, self.energy + food_amount * 2)
    self.happiness = min(100, self.happiness + food_amount)

    return f"{self.name} Meow ~"

def play(self, play_time):
    if play_time < 0:
            return "Meow ? ? (Not play with me ?)"
    
    self.energy = max(0, self.energy - play_time * 10)
    self.happiness = max(100, self.happiness + play_time * 5)

    if self.energy < 30:
        self.hungry = True

        return f"{self.name} have played for {play_time} hours."
    
    
def sleep(self, hours):
    if hours <= 0:
        return "No sleep hours"
        
    self.energy = min(100, self.energy + hours * 15)
    self.hungry = True

    return f"{self.name} have slept for {hours} hours."
    
def get_status(self):
        return {
            "name": self.name,
            "age": self.age,
            "breed": self.breed,
            "color": self.color,
            "hungry": self.hungry,
            "energy": self.energy,
            "happiness": self.happiness
        }
    
# 4. Class Methods 
@classmethod
def from_birth_year(cls, name, birth_year, breed, color):
    current_year = datetime.datetime.now().year
    age = current_year - birth_year
    return cls(name, age, breed, color)
    
@classmethod
def get_species_info(cls):
    return {
        "species": cls.species,
        "total_cats": cls.total_cats,
        "average_lifespan": cls.average_lifespan
    }
    
# 5. Static Methods   
@staticmethod
def is_senior(age):
    return age > 7
    
@staticmethod
def calculate_healthy_food_amount(weight):
    return weight * 20
