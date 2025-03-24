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
    cards = []

    user_cards = request.user.user_data.get_all_cards()

    for card in user_cards:
        cards.append({
                "card_name": card.card_name,
                "value": card.value,
                "card_desc": card.card_desc,
                "image_path": card.image
            })

    return render(request, 'trading/trading_room.html', {'room_name': room_name, 'user': 'owner', 'cards':cards})

def join_trading_room(request, room_name):

    cards = []

    user_cards = request.user.user_data.get_all_cards()

    for card in user_cards:
        cards.append({
                "card_name": card.card_name,
                "value": card.value,
                "card_desc": card.card_desc,
                "image_path": card.image
            })
        
    return render(request, 'trading/trading_room.html', {'room_name': room_name, 'user': 'member', 'cards':cards})
