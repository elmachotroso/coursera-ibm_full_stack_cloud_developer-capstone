from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
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
    return get_dealerships(request)

def logout_request(request):
    return get_dealerships(request)

def registration_request(request):
    return render(request, "djangoapp/registration.html")

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    return render(request, "djangoapp/dealer_details.html")

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    return render(request, "djangoapp/add_review.html")

