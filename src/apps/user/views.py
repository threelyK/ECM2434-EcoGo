# - Authentication models/functions - #

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model # not being used rn
from django.contrib.auth import authenticate, login, logout


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
                login(request, user)

                # redirects the user to the homepage after a successful login
                return redirect("home")
            else:
                # the authentication failed
                pass

    context = {'loginform': form}

    # renders the login page with the form
    return render(request, 'user/login.html', context=context)


@login_required(login_url='login') # Enforces the rule that users need to be logged in to access the home page
def homepage(request):
    # redners the homepage but only if the user is logged in
    return render(request, 'user/homepage.html')

def user_logout(request):

    logout(request)

    # redirects the user to the home page if they log out
    return redirect("home")
