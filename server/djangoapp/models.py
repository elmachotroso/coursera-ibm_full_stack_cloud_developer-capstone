from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512)

    def __str__(self):
        return f"CarMake name={self.name} description={self.description}"


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    TYPE_CHOICES = (
        ("Sedan", "Sedan"),
        ("SUV", "SUV"),
        ("WAGON", "WAGON"),
        ("Others", "Others"))
    modelId = models.ForeignKey(CarMake, on_delete=CASCADE)
    name = models.CharField(max_length=256)
    dealerId = models.IntegerField()
    type = models.CharField(max_length=128, choices=TYPE_CHOICES)
    year = models.DateField()
    def __str__(self):
        return f"modelId={modelId} name={name} dealerId={dealerId} type={type} year={year}"



# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer(models.Model):
    pass


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview(models.Model):
    pass