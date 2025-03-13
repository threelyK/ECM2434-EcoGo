from django.shortcuts import render, redirect
from django.http import JsonResponse

def waiting_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        return redirect('trading_room', room_name=room_name)
    return render(request, 'trading/waiting_room.html')

def join_room(request):
    return render(request, 'trading/join_room.html')

def available_rooms(request):
    # This should return a list of available rooms
    rooms = ['room1', 'room2', 'room3']  # Example room names
    return JsonResponse({'rooms': rooms})

def trading_room(request, room_name):
    return render(request, 'trading/trading_room.html', {'room_name': room_name})