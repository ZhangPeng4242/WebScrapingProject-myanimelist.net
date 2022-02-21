class Animal:
    num_animal = 0

    def __init__(self, weight_kg, num_legs):
        self._weight_kg = weight_kg
        self.num_legs = num_legs
        Animal.num_animal += 1

    def get_weight(self):
        return self._weight_kg

    def _get_weight_per_leg(self):
        return self._weight_kg / self.num_legs

    def set_weight_kg(self, weight_kg):
        self._weight_kg = weight_kg

    def gram_per_leg(self):
        return self._get_weight_per_leg()*1000

    def __eq__(self, other):
        if self.num_legs == other.num_legs and self._weight_kg == other._weight_kg:
            return True
        return False


dog_ceaser = Animal(10, 4)
dog_moshe = Animal(10, 4)
parrot_barney = Animal(1, 2)
print(dog_ceaser.gram_per_leg())
print(parrot_barney.gram_per_leg())
print(Animal.num_animal, dog_ceaser.num_animal, parrot_barney.num_animal)
print(dog_ceaser == dog_moshe)
print(dog_ceaser == parrot_barney)