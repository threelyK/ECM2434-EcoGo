socket.onopen = () => {
    let message;

    if(user_type == "owner"){
        message = {
            "state_flag": 'S',
            "body":{},
            "room_name": room_name
        }
    } else{
        message = {
            "state_flag": 'J',
            "body":{},
            "room_name": room_name
        }
    }

    socket.send(JSON.stringify(message))
}

socket.onmessage = (event) =>{
    console.log(event.data)
}