/*
let socketcontrol = false;

function create_Room() {
    console.log('Create room function called');
    const roomName = $('#roomName').val();
    socketcontrol = true;
    if (socketcontrol) {
        const socket = new WebSocket('ws://localhost:8000/ws/trading/');

        socket.onopen = function() {
            socket.send(JSON.stringify({
                'action': 'create_room',
                'room_name': roomName
            }));
        };

        socket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            $('#messages').append('<p>' + data.message + '</p>');
            if (data.message.includes('Room')) {
                //Redirect to trading room
                setTimeout(function() {
                window.location.href = '/trading/trading_room/' + roomName + '/';
                }, 1000);
            }
        };

        socket.onclose = function(event) {
            console.log("Websocket connection closed");
        };

        socket.onerror = function(error) {
            console.log("Websocket error: " + error,message);
        };
    }
}
*/

/*
function join_Room(roomName) {
    socketcontrol = true;
    if (socketcontrol) {
        const socket = new WebSocket('ws://localhost:8000/ws/trading/');

        socket.onopen = function() {
            socket.send(JSON.stringify({
                'action': 'join_room',
                'room_name': roomName
            }));
        };

        socket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            $('#messages').append('<p>' + data.message + '</p>');
            if (data.message.includes('Joined room')) {
                // Redirect to the trading room
                setTimeout(function() {
                window.location.href = '/trading/trading_room/' + roomName + '/';
                }, 1000);
            }
        };

        socket.onclose = function(event) {
            console.log("Websocket connection closed");
        };

        socket.onerror = function(error) {
            console.log("Websocket error: " + error.message);
        };
    }
}
    */

function redirectToTradingRoom() {
    const roomName = $('#roomName').val();
    if (!roomName) {
        alert("Please enter a room name.");
        return;
    }
    window.location.href = '/trading/trading_room/' + roomName + '/';
}