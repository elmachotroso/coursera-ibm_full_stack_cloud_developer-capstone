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

class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return f"Dealer name: {self.full_name}"

    @staticmethod
    def create(dealer_json):
        return CarDealer(address=dealer_json["address"]
                , city=dealer_json["city"]
                , full_name=dealer_json["full_name"]
                , id=dealer_json["id"]
                , lat=dealer_json["lat"]
                , long=dealer_json["long"]
                , short_name=dealer_json["short_name"]
                , st=dealer_json["st"]
                , zip=dealer_json["zip"])


class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return f"Name = {self.name}"

    @staticmethod
    def create( dealer_review_json ):
        return DealerReview(dealership=dealer_review_json['dealership']
            , name=dealer_review_json['name']
            , purchase=dealer_review_json['purchase']
            , review=dealer_review_json['review']
            , purchase_date=dealer_review_json['purchase_date']
            , car_make=dealer_review_json['car_make']
            , car_model=dealer_review_json['car_model']
            , car_year=dealer_review_json['car_year']
            , sentiment=dealer_review_json['sentiment']
            , id=dealer_review_json['id'])