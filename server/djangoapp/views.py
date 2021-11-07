from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarModel, CarMake
from .restapis import get_dealers_from_cf, get_dealers_by_state_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, add_review_to_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def about(request):
    return render(request, "djangoapp/about.html")

def contact(request):
    return render(request, "djangoapp/contact.html")

def login_request(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = 'Wrong username or password combination.'
    return render(request, "djangoapp/user_login.html", context)

def logout_request(request):
    if request.user is not None and request.user.is_authenticated:
        print("Logging out user {}".format(request.user.username))
        logout(request)
    return redirect('djangoapp:index')

def registration_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        password2 = request.POST['psw2']
        if password == password2:
            email = request.POST['email']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            users = User.objects.filter(username=username)
            if users.count() == 0:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=firstname, last_name=lastname)
                login(request, user)
                return redirect('djangoapp:index')
            else:
                context['message'] = "User {} already exists! Please try another unique username.".format(username)
        else:
            context['message'] = "Entered passwords do not match. Please try again and make sure they are correct."
    return render(request, "djangoapp/registration.html", context)

def get_dealerships(request):
    context = {}
    if request.method == "GET":
        dealerships = get_dealers_from_cf()
        context["dealers"] = dealerships
    return render(request, 'djangoapp/index.html', context)

def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        dealers = get_dealer_by_id_from_cf(dealer_id)
        context["dealer"] = None
        if len(dealers) > 0:
            context["dealer"] = dealers[0]
        context["reviews"] = get_dealer_reviews_from_cf(dealer_id)
    return render(request, "djangoapp/dealer_details.html", context)

def get_all_cars_by_dealer(dealer_id):
    results = {}
    car_models = CarModel.objects.filter(dealerId=dealer_id)
    for car_model in car_models:
        results[str(car_model.id)] = car_model
    print(f"get_all_cars_by_dealer({dealer_id})={results}")
    return results

def get_all_cars_options_by_dealer(dealer_id):
    results = []
    cars = get_all_cars_by_dealer(dealer_id)
    for carId in cars:
        car = cars[carId]
        results.append({
            "id" : carId,
            "label" : f"{car.name}-{car.makeId.name}-{car.year.year}"
        })
    return results

def add_review(request, dealer_id):
    if request.method == "POST":
        if request.user is not None and request.user.is_authenticated:
            print("POST something.")
            POST = request.POST
            review = {
                "dealership" : dealer_id,
                "name" : f"{request.user.first_name} {request.user.last_name}",
                "purchase" : ("purchase" in POST and POST["purchase"] == "on"),
                "purchase_date" : POST["purchase_date"],
                "review" : POST["review"],
                }

            review["car_make"] = "undefined"
            review["car_model"] = "undefined"
            review["car_year"] = 1800
            post_carId = POST["car"]
            car_models = get_all_cars_by_dealer(dealer_id)
            if car_models and post_carId in car_models:
                car = car_models[post_carId]
                review["car_make"] = car.makeId.name
                review["car_model"] = car.name
                review["car_year"] = car.year.year
                
            json_payload = { "review" : review }
            print(f"json_payload={json_payload}")
            result = add_review_to_cf(json_payload)
            if result and len(result) > 0:
                print(f"POST add_review_to_cf SUCCESS! reviewId={result[0]['reviewId']}")
                return redirect('djangoapp:dealer', dealer_id=dealer_id)
    # GET part
    context = {}
    dealers = get_dealer_by_id_from_cf(dealer_id)
    context["dealer"] = None
    context["cars"] = get_all_cars_options_by_dealer(dealer_id)
    if len(dealers) > 0:
        context["dealer"] = dealers[0]
    return render(request, "djangoapp/add_review.html", context)

