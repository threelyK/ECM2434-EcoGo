const socket = new WebSocket('ws://localhost:8000/ws/trading/');

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    $('#messages').append('<p>' + data.message + '</p>');
};

function create_Room() {
    const roomName = $('#roomName').val();
    socket.send(JSON.stringify({
        'action': 'create_room',
        'room_name': roomName
    }));
    // Redirect to the trading room
    window.location.href = '/trading/trading_room/' + roomName + '/';
}