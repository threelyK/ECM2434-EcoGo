from django.shortcuts import render, redirect
from django.http import JsonResponse

available_rooms_list = []

def waiting_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        available_rooms_list.append(room_name)
        return redirect('trading_room', room_name=room_name)
    return render(request, 'trading/waiting_room.html')

def join_room(request):
    
    return render(request, 'trading/join_room.html')

def available_rooms(request):
    # This should return a list of available rooms
    return JsonResponse({'rooms': available_rooms_list})

def trading_room(request, room_name):
    return render(request, 'trading/trading_room.html', {'room_name': room_name})

