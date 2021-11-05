from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.timezone import now

class CarMake(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512)

    def __str__(self):
        return f"CarMake name={self.name} description={self.description}"

class CarModel(models.Model):
    TYPE_SEDAN = "Sedan"
    TYPE_SUV = "SUV"
    TYPE_WAGON = "WAGON"
    TYPE_ETC = "Others"
    TYPE_CHOICES = (
        (TYPE_SEDAN, "Sedan"),
        (TYPE_SUV, "SUV"),
        (TYPE_WAGON, "WAGON"),
        (TYPE_ETC, "Others"))
    makeId = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    dealerId = models.IntegerField(null=False)
    type = models.CharField(max_length=128, choices=TYPE_CHOICES, default=TYPE_SEDAN)
    year = models.DateField()
    def __str__(self):
        return f"makeId={self.makeId} name={self.name} dealerId={self.dealerId} type={self.type} year={self.year}"



# <HINT> Create a plain Python class `CarDealer` to hold dealer data
# class CarDealer(models.Model):
#     pass


# <HINT> Create a plain Python class `DealerReview` to hold review data
# class DealerReview(models.Model):
#     pass