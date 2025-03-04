# - Authentication models/functions - #

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from json import loads
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.contrib.auth import get_user_model # not being used rn
from .forms import LoginForm, CreateUserForm
from .models import User, UserData
from apps.cards.models import Card

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
    user_context = {
        "user": request.user
    }
    return render(request, 'user/homepage.html', context=user_context)


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
    
    else:
        return Http404()
    
@login_required(login_url="login")
def sell_card(request):
    """
    Endpoint for "user/inventory/sellCard": removes a card from a users inventory, adds the cards value to
    the users points and serves and updated template with the changes reflected.
    """

    if request.method == "POST":
        #Checks request body is correct json
        try:
            data = loads(request.body.decode("utf-8"))
        except:
            return HttpResponseBadRequest("INVALID REQUEST BODY FORMAT")

        #Checks request body includes a card name element
        if not "card_name" in data.keys():
            return HttpResponseBadRequest("INVALID REQUEST BODY FORMAT")

        #Checks that the card requested exists
        try:
            card = Card.objects.get(card_name=data["card_name"])
        except:
            return HttpResponseBadRequest("REQUESTED CARD DOES NOT EXIST")

        user_data = request.user.user_data

        try:
            user_data.remove_card(card)
        except:
            return HttpResponseBadRequest("USER DOES NOT HAVE THE REQUIRED CARD")
        
        user_data.add_points(card.value)

        #renders the template again using the inventory view
        request.method = 'GET'
        return inventory(request)

    else:
        return Http404()
    

def leaderboard(request):
    """
    This function will find and return the top 10 users based on their level. 
    The usernames as well as the level are then returned within the context to be used by the front-end template.
    """

    top_10_users = UserData.objects.select_related('owner').order_by('-level')[:10] # Gets the users ordered by the number of points. Limits the query to 10 users.

    con = {'top_10_users' : [{'username':user.owner.username, 'level':user.level} for user in top_10_users]}  # Includes username from the paernt table (User) and level from UserData table

    return render(request, 'user/leaderboard.html', context=con)
