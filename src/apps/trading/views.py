from django.shortcuts import render, redirect
from django.http import JsonResponse
from .TradingRoom import rooms

available_rooms_list = []

def waiting_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        available_rooms_list.append(room_name)
        return redirect('trading_room', room_name=room_name)
    return render(request, 'trading/waiting_room.html')

def join_room(request):
    context = {"rooms":rooms}

    return render(request, 'trading/join_room.html', context)

def available_rooms(request):
    # This should return a list of available rooms
    return JsonResponse({'rooms': available_rooms_list})

def create_trading_room(request, room_name):
    return render(request, 'trading/trading_room.html', {'room_name': room_name, 'user': 'owner'})

def join_trading_room(request, room_name):
    return render(request, 'trading/trading_room.html', {'room_name': room_name, 'user': 'member'})

