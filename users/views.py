from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    #if no user is signed in, return to login page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "users/user.html")

def login_view(request):
    if request.method == "POST":
        #get username and password from form data
        username = request.POST["username"]
        password = request.POST["password"]

        #authenticating
        user = authenticate(request, username= username, password=password)

        #If user object is returned, login and route to index page
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        #Otherwise, re-render page
        else:
            return render(request, "users/login.html",{
                "message": "Invalid credentials!!!!"
                })
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        "message": "Logged out."
    })