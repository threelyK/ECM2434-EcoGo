# - Authentication models/functions - #

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.contrib.auth import get_user_model # not being used rn
from .forms import LoginForm, CreateUserForm
from .models import User, UserData

def landing(request):
    # renders the landing page where users can choose to log in or register
    return render(request, 'user/landingpage.html')


def register(request):
    form = CreateUserForm()

    # checks if the request method is POST, which means the user is submitting the registration form
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        # checks if the form data is valid (including password1 and password2 to match)
        if form.is_valid():
            form.save()
            # redirects the user to the login page after successful registration
            return redirect("login")
        
        else:
            print(form.errors)

    # passes the form to the template context to display it on the page
    context = {'registerform': form}

    # renders the registration page with the form
    return render(request, 'user/register.html', context=context)


def user_login(request):
    form = LoginForm()

    # checks if the request method is POST, indicating the user is trying to log in
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            # retrieves the username and password from the POST data
            username = request.POST.get('username')
            password = request.POST.get('password')

            # attempts to authenticate the user using the provided credentials
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # logs the user in
                auth.login(request, user)

                # redirects the user to the homepage after a successful login
                return redirect("homepage")
            else:
                # the authentication failed
                pass

    context = {'loginform': form}

    # renders the login page with the form
    return render(request, 'user/login.html', context=context)


@login_required(login_url='login') # Enforces the rule that users need to be logged in to access the home page
def homepage(request):
    # renders the homepage but only if the user is logged in
    return render(request, 'user/homepage.html')


def user_logout(request):

    auth.logout(request)

    # redirects the user to the home page if they log out
    return redirect("landing")

@login_required(login_url="login")
def inventory(request):
    """
    Endpoint for "user/inventory", serves inventory page throwing error if 
    user has invalid internal state
    """
    if request.method == "GET":
        user_data = request.user.user_data
        cards_quant = user_data.get_all_cards_quant()
        cards = []
        for card in cards_quant:
            cards.append({
                "card_name": card[0].card_name,
                "value": card[0].value,
                "quant": card[1],
                "card_desc": card[0].card_desc,
                "image_path": card[0].image
            })

            print(card[0].image)

        #data to send to template
        con = {
            "cards": cards,
            "points": user_data.points,
            "username": request.user.username,
            "level": user_data.level,
            "xp": user_data.xp
        }

        return render(request, "user/inventory.html", context=con)
    
@login_required(login_url="login")
def sell_card(request):
    """
    Endpoint for "user/inventory/sellCard": removes a card from a users inventory, adds the cards value to
    the users points and serves and updated template with the changes reflected.
    """

    if request.method == "POST":
        return HttpResponse("Hello World")
    else:
        return Http404()