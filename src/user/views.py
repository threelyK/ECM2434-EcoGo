from django.shortcuts import render, redirect

from .forms import CreateUserForm, LoginForm

from django.contrib.auth.decorators import login_required


# - Authentication models/functions - #

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

def landing(request):

    return render(request, 'user/landingpage.html')

def register(request):

    form = CreateUserForm()

    if request.method == 'POST':

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("login")
        
    context = {'registerform': form}

    return render(request, 'user/register.html', context=context)


def login(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("home")
            
        
    context = {'loginform': form}

    return render(request, 'user/login.html', context=context)
    
            

    return render(request, 'user/login.html')

@login_required(login_url='login') # Forces people to login
def homepage(request):

    return render(request, 'user/homepage.html')

def user_logout(request):

    auth.logout(request)

    return redirect("")
