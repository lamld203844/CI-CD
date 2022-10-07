from ast import Pass
from urllib import response
from django.db.models import Max
from django.test import TestCase, Client
from .models import Airport, Flight, Passenger

# Create your tests here.
class FlightTestCase(TestCase):

    def setUp(self):

        # Create airports
        a1 = Airport.objects.create(code = 'AAA', city = 'city A')
        a2 = Airport.objects.create(code = 'BBB', city = 'city B')

        # Create flights
        Flight.objects.create(origin = a1, destination = a2, duration = 100)
        Flight.objects.create(origin = a1, destination = a1, duration = 200)
        Flight.objects.create(origin = a1, destination = a2, duration = -100)

    def test_departures_count(self):
        a = Airport.objects.get(code = 'AAA')
        self.assertEqual(a.departures.count(), 3)

    def test_arrivals_count(self):
        a = Airport.objects.get(code = 'AAA')
        self.assertEqual(a.arrivals.count(), 1)

    def test_valid_flight(self):
        a1 = Airport.objects.get(code = 'AAA')
        a2 = Airport.objects.get(code = 'BBB')
        f = Flight.objects.get(origin = a1, destination = a2, duration = 100)

        self.assertTrue(f.is_valid_flight())
    
    def test_invalid_flight_destination(self):
        a1 = Airport.objects.get(code = 'AAA')
        a2 = Airport.objects.get(code = 'BBB')
        f = Flight.objects.get(origin = a1, destination = a1, duration = 200)

        self.assertFalse(f.is_valid_flight())
    
    def test_invalid_flight_duration(self):
        a1 = Airport.objects.get(code = 'AAA')
        a2 = Airport.objects.get(code = 'BBB')
        f = Flight.objects.get(origin = a1, destination = a2, duration = -100)

        self.assertFalse(f.is_valid_flight())

    def test_index(self):

        # Set up client
        c = Client()

        # Send get request
        response = c.get('/flights/')

        # Make sure status code is 200
        self.assertEqual(response.status_code, 200)

        # Make sure 3 flights are returned in context
        self.assertEqual(response.context['flights'].count(), 3)

    def test_valid_flight_page(self):
        a1 = Airport.objects.get(code = 'AAA')
        f = Flight.objects.get(origin = a1, destination = a1)

        c = Client()
        response = c.get(f'/flights/{f.id}')
        self.assertEqual(response.status_code, 200)

    def test_invalid_flight_page(self):
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]

        c = Client()
        response = c.get(f"/flights/{max_id + 1}")
        self.assertEqual(response.status_code, 404)

    def test_flight_page_passengers(self):
        p = Passenger.objects.create(first = 'Alice', last = 'Adams')
        f = Flight.objects.get(pk=1)
        f.passengers.add(p)

        c = Client()
        response = c.get(f'/flights/{f.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['passengers'].count(), 1)

    def test_flight_non_passengers(self):
        p = Passenger.objects.create(first = 'Alice', last = 'Adams')
        f = Flight.objects.get(pk=1)

        c = Client()
        response = c.get(f'/flights/{f.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['non_passengers'].count(), 1)