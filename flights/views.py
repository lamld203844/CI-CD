from django.urls import reverse
from django.http import HttpResponseRedirect, Http404

from django.shortcuts import render
from flights.models import Flight, Airport, Passenger
# Create your views here.

def index(request):
    return render(request, "flights/index.html",{
        "flights": Flight.objects.all()
    })

def flight(request, flight_id):
    #Check existence of flight
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        flight = None

    # Case flight don't exist
    if flight == None:
        return render(request, "flights/not_found.html", status=404)

    #Get non passengers
    non_passengers = Passenger.objects.exclude(flights = flight).all()

    #Get all passengers in flight
    passengers = flight.passengers.all()
    return render(request, "flights/flight.html",{
        'flight': flight,
        'passengers': passengers,
        'non_passengers': non_passengers
    })

def book(request, flight_id):
    #For a POST request, add a new flight
    if request.method == "POST":

        #Access flight
        flight = Flight.objects.get(pk = flight_id)

        #Find passenger id from submitted form data
        passenger_id = int(request.POST["passenger"])

        #Find passenger based on id
        passenger = Passenger.objects.get(pk = passenger_id)

        #Add passenger to flight
        passenger.flights.add(flight)
        
        #Redirect 
        return HttpResponseRedirect(reverse("flight", args = (flight.id,)))


