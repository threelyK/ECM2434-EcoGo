# - Authentication models/functions - #

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from json import loads
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.contrib.auth import get_user_model # not being used rn
from .forms import LoginForm, CreateUserForm, BuyForm, SellForm
from .models import User, UserData
from apps.cards.models import Pack
from apps.cards.models import Card
from apps.cards.views import open_pack

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
        data_form = SellForm()
    elif request.method == "POST":
        data_form = SellForm(request.POST)

        if not data_form.is_valid():
            return HttpResponseBadRequest("INVALID FORM")

        card_name = data_form.cleaned_data["card_name"]

        #Checks that the card requested exists
        try:
            card = Card.objects.get(card_name=card_name)
        except:
            return HttpResponseBadRequest("REQUESTED CARD DOES NOT EXIST")

        user_data = request.user.user_data

        try:
            user_data.remove_card(card)
        except:
            return HttpResponseBadRequest("USER DOES NOT HAVE THE REQUIRED CARD")

        user_data.add_points(card.value)

    else:
        return Http404()
    
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

    #data to send to template
    con = {
        "cards": cards,
        "points": user_data.points,
        "username": request.user.username,
        "level": user_data.level,
        "xp": user_data.xp,
        "form" : data_form
    }

    return render(request, "user/inventory.html", context=con)

@login_required(login_url="login")
def shop(request):
    """
    Endpoint for "shop", serves the shop page
    """

    if request.method == "POST":
        data_form = BuyForm(request.POST)

        if data_form.is_valid():
            item_name = data_form.cleaned_data["item_name"]
            
            try:
                pack = Pack.objects.get(pack_name = item_name)
            except:
                return HttpResponseBadRequest("PACK REQUESTED DOES NOT EXIST")
                
            pack_cost = pack.cost
            user_points = request.user.user_data.points

            if user_points >= pack_cost:
                response = open_pack(request, item_name)
                request.user.user_data.remove_points(pack_cost)
                return response
            else:
                return HttpResponseBadRequest("NOT ENOUGH POINTS FOR TRANSACTION")
            
        else:
            return HttpResponseBadRequest("INVALID FORM")
    elif request.method == "GET":
        data_form = BuyForm()
    else:
        return Http404()
    
    user_data = request.user.user_data
    packs = Pack.objects.all()
    context = {
        "packs": packs,
        "points": user_data.points,
        "level": user_data.level,
        "form": data_form,
    }

    return render(request, "user/shop.html", context=context)
