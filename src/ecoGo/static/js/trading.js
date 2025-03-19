var trade_offer

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

    console.log("connected")

    socket.send(JSON.stringify(message))
}

socket.onmessage = (event) =>{
    let data = JSON.parse(event.data)
    let state_flag = data["state_flag"]
    let data_body = data["body"]

    console.log("moving into state: " + state_flag)

    try{
        if(state_flag == "E"){
            reciveError()
            return; // Just in case reciveError() does not stop execution
        }

        if(user_type == "owner"){
            if(state_flag == "X"){
                state = "X"
                reset_to_w_disconnect();
            }
            else if(state_flag == "N" && state == "W"){
                state = "N"
                owner_joined_room(data_body);
            }
            else if(state_flag == "D"){
                if(state != "N")
                    throw "Invalid state transition" //pretty sure this is impossible

                state = "D"
                owner_trade_proposed()
            }
            else if(state_flag == "N" && state == "D"){
                state = "N"
                owner_trade_offer_rejected()
            }
            else if(state_flag == "A"){
                state = "A"

                owner_trade_complete()
            }
        }
        else if(user_type == "member"){
            if(state_flag == "X"){
                state = "X"
                kick_back_to_room_select()
            }
            else if(state_flag == "N" && state == "W"){
                state = "N"
                member_joined_room(data_body);
            }
            else if(state_flag == "D"){
                if(state != "N")
                    throw "Invalid state transition" //pretty sure this is impossible

                state = "D"
                trade_offer = data_body
                member_proposed_trade(data_body)
            }
            else if(state_flag == "N" && state == "D"){
                state = "N"
                member_trade_offer_rejected()
            }
            else if(state_flag == "A"){
                state = "A"

                member_trade_complete()
            }
        }
        else{
            throw "Invalid user type"
        }
    }
    catch(err){
        sendError(err.message)
    }
}

/*
   ------------------- BUTTON HANDLERS -------------------
*/

//Button handler to accept the trade (could prevent spamming in future)
function acceptTrade(){
    if(state != "D"){
        sendError("Cannot accept trade from this state")
        return;
    }

    if(user_type != "member"){
        sendError("Cannot accept trade as owner")
        return;
    }

    let message = {
        "state_flag": "A",
        "body": trade_offer
    }

    socket.send(JSON.stringify(message));
}

//Button hander to reject the trade
function rejectTrade(){
    if(state != "D"){
        sendError("Cannot reject trade from this state")
        return;
    }

    if(user_type != "member"){
        sendError("Cannot reject trade as owner")
        return;
    }

    let message = {
        "state_flag": "N",
        "body": {}
    }

    socket.send(JSON.stringify(message));
}

//Button handler for proposing a trade
function propse_trade_handler(){
    if(state != "N"){
        sendError("Cannot propose trade from this state")
        return;
    }

    if(user_type != "owner"){
        sendError("Cannot propose trade as member")
        return;
    }

    let owner_cards = null
    let member_cards = null

    /*
        POPULATE OWNER_CARDS AND MEMBER_CARDS HERE
    */

    propose_trade(owner_cards, member_cards)
}

function propose_trade_test(){
    let owner_cards = ["Hydronis"]
    let member_cards = ["Vortex-9"]

    propose_trade(owner_cards, member_cards)
}

function propose_trade(owner_cards, member_cards){
    let message = {
        "state_flag": "D",
        "body":{
            "member_cards": member_cards,
            "owner_cards":owner_cards
        }
    }

    socket.send(JSON.stringify(message))
}

function sendError(error_message){
    // This will result in an error being sent back
    let message = {
        "state_flag": "E",
        "body": {
            "msg": error_message
        }
    }

    socket.send(JSON.stringify(message))
}

/*
   ------------------- EVENT HANDLERS -------------------
*/

function reciveError(){
    // Exit out to landing page on error (for now)
    window.location.href = "/"
}

//Resets the page to the inital state for the room owner
function reset_to_w_disconnect(){

}

//Kicks the member back to the room selection if room closes (with error?)
function kick_back_to_room_select(){

}

//Called when the member joins the room, data_body contains their name/level
function owner_joined_room(data_body){

}

//Called when the member joins the room, data_body contains the owners name/level
function member_joined_room(data_body){

}

//Called when a trade is proposed (on owners client)
function owner_trade_proposed(){

}

//Called when a trade is proposed and gets passed cards for trading
function member_proposed_trade(data_body){

}

//Called when the member rejects a trade, resets back to N state (on owners client)
function owner_trade_offer_rejected(){

}

//Called when the member rejects a trade, resets back to N state (on members client)
function member_trade_offer_rejected(){

}

//Called by the owner when the trade has been accepted and processed
function owner_trade_complete(){

}

//Called by the member when the trade has be accepted and processed
function member_trade_complete(){

}