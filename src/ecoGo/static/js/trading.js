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


$(document).ready(function(){
    var trade_offer
    let member_card_array = []
    let owner_card_array = []

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

        let owner_cards = owner_card_array
        let member_cards = member_card_array

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

    function clearSelection(){
        member_card_array = []
        owner_card_array = []

        //Undo all selection effects
    }

    /*
    ------------------- EVENT HANDLERS -------------------
    */

    function reciveError(){
        // Exit out to landing page on error (for now)
    //  window.location.href = "/"
    }

    //Resets the page to the inital state for the room owner
    function reset_to_w_disconnect(){
        window.location.href = "/homepage"
    }

    //Kicks the member back to the room selection if room closes (with error?)
    function kick_back_to_room_select(){
        window.location.href = "/homepage"
    }

    //Called when the member joins the room, data_body contains their name/level
    function owner_joined_room(data_body){
        display_cards(data_body["cards"], "#member-container", false)
        //Adding submit button for the cards
        $("#member-container").append("<button type='button' id='propose' class='btn btn-success btn-lg propose' style='font-family: GameFont, Arial, Helvetica, sans-serif; margin-top: 20px;'>Propose Trade</button>")
        $('.card-container.member').on('click', function(){
            var cardName = $(this).find('.card-title').first().text();
            if(!$(this).hasClass("selected")){
                member_card_array.push(cardName);
                $(this).addClass("selected")
            }
            else{
                //remove the card from the list
                let index = member_card_array.indexOf(cardName)
                member_card_array.splice(index, 1)

                $(this).removeClass("selected")
            }

        })

        $(document).ready(function(){
            $('#propose').on('click', function(){
                propse_trade_handler();
            })
        })
    }

    //Called when the member joins the room, data_body contains the owners name/level
    function member_joined_room(data_body){
        
    }

    function display_cards(cardsList, container, isOwner){
        let o_or_m;
        if(isOwner){
            o_or_m = "owner";
        }
        else{
            o_or_m = "member"
        }
        cardsList.forEach((card) =>{
            var cardHTML = `
            <li>
                <div class="card-container ${o_or_m}">
                    <div class="card">
                        <div class="bar bar-top">
                            <div class="card-title">${ card.card_name }</div>
                            <div class="casting-cost">
                                <div class="card-value">
                                    ${ card.value }
                                </div> 
                                <div class="card-quantity">
                                    ${ card.quant }
                                </div>
                            </div>
                        </div>
                        <div class="card-image">
                            <img src="/static/${card.image_path}" alt="card image">
                        </div>
                        <div class="bar bar-mid">
                            <div class="card-title">Instant</div>
                        </div>
                        <div class="card-text">
                            <div class="card-ability">
                                ${ card.card_desc }
                            </div>
                        </div>
                        <div class="footer">
                            <div class="author">Created by Breadscrums.</div>
                        </div>
                    </div>
                </div>
            </li>
            `;

            $(container).append(cardHTML);

        })
    }

    //Called when a trade is proposed (on owners client)
    function owner_trade_proposed(){

    }

    //Called when a trade is proposed and gets passed cards for trading
    function member_proposed_trade(data_body){
        display_cards(data_body["owner_cards"], "#receive-container", true)
        display_cards(data_body["member_cards"], "#giving-container", false)
        $("#member-offer").append("<button type='button' id='reject' class='btn btn-success btn-lg' style='font-family: GameFont, Arial, Helvetica, sans-serif; margin-top: 20px;'>Reject Trade</button>")
        $("#member-offer").append("<button type='button' id='accept' class='btn btn-success btn-lg' style='font-family: GameFont, Arial, Helvetica, sans-serif; margin-top: 20px;'>Accept Trade</button>")
        $(document).ready(function(){
            $('#accept').on('click', function(){
                acceptTrade();
            })
        })
    
        $(document).ready(function(){
            $('#reject').on('click', function(){
                rejectTrade();
            })
        })

        trade_offer = {
            "member_cards":[],
            "owner_cards":[]
        }

        for(let i = 0; i < data_body["owner_cards"].length; i++){
            trade_offer["owner_cards"].push(data_body["owner_cards"][i].card_name)
        }

        for(let i = 0; i < data_body["member_cards"].length; i++){
            trade_offer["member_cards"].push(data_body["member_cards"][i].card_name)
        }
    }

    //Called when the member rejects a trade, resets back to N state (on owners client)
    function owner_trade_offer_rejected(){
        clearSelection()
    }

    //Called when the member rejects a trade, resets back to N state (on members client)
    function member_trade_offer_rejected(){

    }

    //Called by the owner when the trade has been accepted and processed
    function owner_trade_complete(){
        window.location.href = "/homepage"
    }

    //Called by the member when the trade has be accepted and processed
    function member_trade_complete(){
        window.location.href = "/homepage"
    }

    $(document).ready(function(){
        $('.card-container.member').on('click', function(){
            var cardName = $(this).find('.card-title').first().text();
            if(!$(this).hasClass("selected")){
                member_card_array.push(cardName);
                $(this).addClass("selected")
            }
            else{
                //remove the card from the list
                let index = member_card_array.indexOf(cardName)
                member_card_array.splice(index, 1)

                $(this).removeClass("selected")
            }

        })
    })

    $(document).ready(function(){
        $('.card-container.owner').on('click', function(){
            var cardName = $(this).find('.card-title').first().text();
            if(!$(this).hasClass("selected")){
                owner_card_array.push(cardName);
                $(this).addClass("selected")
            }
            else{
                //remove the card from the list
                let index = owner_card_array.indexOf(cardName)
                owner_card_array.splice(index, 1)

                $(this).removeClass("selected")
            }
        })
    })
})
