"""Module responsable for the state logic of the trading room"""

from apps.user.models import User
from apps.cards.models import Card
from collections.abc import Callable
from functools import wraps
import logging
from json import dumps

rooms = []

class TradingRoom():
    """
    A trading room that generates responses to socket messages and 
    updates the state of the room
    """

    # -------------- Class atributes --------------

    #The state of the TradingRoom, can be:
    # 'W' - waiting, inital state where only 1 player has joined
    # 'N' - neutral, two players have joined but no trade has been proposed
    # 'D' - decision, a trade has been proposed and the memeber is deciding
    # 'A' - accepted, the final state, where a trade has been accepted
    # 'E' - error, some unhandled error has occoured and it needs to shut down
    # 'X' - disconnect, one side has disconnected unexpectedly
    state = 'W'

    #The room owner who created the room and proposes the trades
    room_owner = None

    #The room member who joins the room and accepts/rejects the trades
    room_member = None

    #The output function used to send messages back to the users
    response_func = None

    #A hash used to ensure that an accepted trade is the same as a proposed trade
    trade_hash = None

    #A flag to check if the room should be closed
    end_room = False

    #The logger responsable for recording unhandled errors triggerd by server logic
    logging.basicConfig(filename='ecoGo.log', filemode='a',encoding='utf-8')
    error_logger = logging.getLogger(__name__)

    # -------------- External interface --------------

    def __init__(self, room_owner : User):
        """
        Constructor for a trading room, sets up the trading room into
        the 'W' or waiting state with only a room_owner
        """

        self.room_owner = room_owner

    def error_handler(func):
        """
        Decorates a function to call the error service routine when it throws an exception
        """
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                self.__error_service_routine(e)

        return wrapper

    @error_handler
    def handle(self, message_data : dict, message_source : User):
        """
        Handles any message sent by either user, using the data and sender
        to send a proper response through the socket_output function
        """

        #Handle a user submitted error
        if message_data["state_flag"] == "E":
            raise Exception("Client error: " + message_data["body"]["msg"])

        if message_source == self.room_owner:
            if self.state == 'N' and message_data["state_flag"] == 'D':
                #move from N to D (trade proposed)
                self.__N_to_D(message_data)
        elif message_source == self.room_member:
            if self.state == 'D' and message_data["state_flag"] == 'N':
                #move from D to N (trade rejected)
                self.__D_to_N(message_data)
            elif self.state == 'D' and message_data["state_flag"] == 'A':
                #move from d to A (trade accepted)
                self.__D_to_A(message_data)
        else:
            raise Exception("Invalid message source")

    @error_handler
    def join_room(self, room_member : User, response_func : Callable[[dict, User], None]):
        """
        Allows a second user to join the room and establishes the response_func used
        to communicate with the users, can only be called in the 'W' state
        """

        #Check that the state is valid
        self.__validate_state("W")

        #Init room_member and response function
        self.room_member = room_member
        self.response_func = response_func

        #Update state to neutral
        self.__update_state("N")

        #Form messages to send back to the users
        message_owner = {
            "state_flag": 'N',
            "body": {
                "username": self.room_member.username,
                "level": self.room_member.user_data.level,
                "cards": []
            }
        }

        member_cards = self.room_member.user_data.get_all_cards()
        for card in member_cards:
            message_owner["body"]["cards"].append({
                "card_name": card.card_name,
                "value": card.value,
                "card_desc": card.card_desc,
                "image_path": card.image
            })

        message_member = {
            "state_flag": 'N',
            "body": {
                "username": self.room_owner.username,
                "level": self.room_owner.user_data.level,
                "cards": []
            }
        }

        owner_cards = self.room_owner.user_data.get_all_cards()
        for card in owner_cards:
            message_member["body"]["cards"].append({
                "card_name": card.card_name,
                "value": card.value,
                "card_desc": card.card_desc,
                "image_path": card.image
            })

        #Send a message to the users informing them of the change in state
        self.__send_message(message_owner, self.room_owner)
        self.__send_message(message_member, self.room_member)

    def disconnect(self, disconnected_user : User):
        """
        Method to be called when a user unexpectedly disconnects
        """
        if not self.state == "E":
            self.__update_state("X")

            if disconnected_user == self.room_member:
                #Informs room owner client of disconnect
                message = {
                    "state_flag": "X",
                    "body":{}
                }

                self.__send_message(message, self.room_owner)

                #Returns the room to the W state
                self.response_func = None
                self.room_member = None
                self.trade_hash = None

                self.__update_state('W')
            else:
                #Informs the room member that the room is gone
                message = {
                    "state_flag": "X",
                    "body":{}
                }

                self.__send_message(message, self.room_member)

                #Sets the flag to end the room
                self.end_room = True

    # -------------- Internal methods --------------

    def __send_message(self, message_data : dict, message_dest : User):
        """
        Validates a response to ensure that its valid, then calls the response_func
        """

        if not (message_dest == self.room_owner or message_dest == self.room_member):
            raise Exception("This room cannot respond to user: " + message_dest.username)
        elif message_dest == None:
            raise Exception("Cannot respond to 'None' user")
        
        self.response_func(message_data, message_dest)

    def __error_service_routine(self, e : Exception):
        """
        Called when there is an unhandled internal server error, properly ends the room as to
        keep the server running and informs users
        """

        if self.state == 'W':
            raise Exception("Cannot handle errors in W state")

        self.error_logger.error(e)
        self.error_logger.error("------------------------------------------------------")

        self.__update_state("E")

        error_message = {
            "state_flag" : "E",
            "body":""
        }

        #Inform the users clients of the error
        self.__send_message(error_message, self.room_owner)

        self.__send_message(error_message, self.room_member)

    def __validate_state(self, state : str):
        """
        Checks that the object is in some state and throws an error if not
        """
    
        if not self.state == state:
            raise Exception(
                "Unexpected state, required state is: " + self.state
                + " acctual state is: " + state
            )
        
    def __update_state(self, new_state: str):
        """
        Enforces validation on state transitions
        """

        valid_states = ["W", "N", "D", "A", "E", "X"]

        if not new_state in valid_states:
            raise Exception("Attempting to move to non-existent state")
        
        if self.state == 'W':
            if not new_state in ['N', 'E', 'X']:
                raise Exception("Invalid state transition")
            else:
                self.state = new_state
        elif self.state == 'N':
            if not new_state in ['D', 'E', 'X']:
                raise Exception("Invalid state transition")
            else:
                self.state = new_state
        elif self.state == 'D':
            if not new_state in ['A', 'N', 'E', 'X']:
                raise Exception("Invalid state transition")
            else:
                self.state = new_state
        elif self.state == 'X':
            if not new_state in ['E', 'W']:
                raise Exception("Invalid state transition")
            else:
                self.state=new_state
        else:
            if not new_state == "E":
                raise Exception("Invalid state transition")
            else:
                self.state = 'E'

    def __N_to_D(self, message_data: dict):
        """
        Handles a proposed N to D state transition
        """

        self.__validate_state("N")

        #Checking that the other user has the cards that are needed to trade
        proposed_member_cards = message_data["body"]["member_cards"]
        owned_member_cards = self.room_member.user_data.get_all_cards()
        owned_member_card_names = []

        for card in owned_member_cards:
            owned_member_card_names.append(card.card_name)

        valid = True
        not_owned_cards = []
        for card in proposed_member_cards:
            if not card in owned_member_card_names:
                valid = False
                not_owned_cards.append(card)

        #Either accept the transition or reject it
        if valid:
            
            proposed_owner_cards = message_data["body"]["member_cards"]
            message = {
                "state_flag": 'D',
                "body": {
                    "owner_cards": [],
                    "member_cards": []
                }
            }

            for card in proposed_member_cards:
                card_data = Card.objects.get(card_name = card)
                message["body"]["member_cards"].append({
                    "card_name": card_data.card_name,
                    "value": card_data.value,
                    "card_desc": card_data.card_desc,
                    "image_path": card_data.image
                })

            for card in proposed_owner_cards:
                card_data = Card.objects.get(card_name = card)
                message["body"]["owner_cards"].append({
                    "card_name": card_data.card_name,
                    "value": card_data.value,
                    "card_desc": card_data.card_desc,
                    "image_path": card_data.image
                })

            self.__update_state("D")
            #Save the hash for later validation
            self.trade_hash = hash(str(message_data["body"]))
            self.__send_message(message, self.room_owner)
            self.__send_message(message, self.room_member)
        else:
            message = {
                "state_flag" : 'N',
                "body": not_owned_cards
            }

            self.__send_message(message, self.room_owner)

    def __D_to_N(self, message_data: dict):
        """
        Handles a proposed D to N state transition
        """

        #Moving back to N state
        self.__validate_state("D")
        self.__update_state("N")

        message = {
            "state_flag": "N",
            "body": {}
        }

        #Informing the users of the change in state
        self.__send_message(message, self.room_owner)
        self.__send_message(message, self.room_member)

    def __D_to_A(self, message_data: dict):
        """
        Handles a proposed transtion from D to A
        """

        self.__validate_state("D")
        self.__update_state("A")

        #Check that the hash is the same as the proposed trade
        if not self.trade_hash == hash(str(message_data["body"])):
            raise Exception(
                "Hash mismach - trade accepted is different to trade proposed"
            )

        #Getting the cards
        member_cards = []
        for card in message_data["body"]["member_cards"]:
            member_cards.append(Card.objects.get(card_name = card))

        owner_cards = []
        for card in message_data["body"]["owner_cards"]:
            owner_cards.append(Card.objects.get(card_name = card))

        for card in member_cards:
            self.room_member.user_data.remove_card(card)
            self.room_owner.user_data.add_card(card)

        for card in owner_cards:
            self.room_owner.user_data.remove_card(card)
            self.room_member.user_data.add_card(card)

        message = {
            "state_flag": "A",
            "body":{}
        }

        self.__send_message(message, self.room_owner)
        self.__send_message(message, self.room_member)

        #Sets the flag to end the room
        self.end_room = True

def get_room(rooms : list[(str, TradingRoom, Callable)], room_name : str) -> tuple[TradingRoom, Callable]:
    """
    Gets the room with a specific name out of a list of rooms
    """

    for room in rooms:
        if room[0] == room_name:
            return (room[1], room[2])

    raise Exception("non-existent room requested")

def get_response_func(
        owner_user : User, 
        owner_respond : Callable, 
        member_user : User, 
        member_respond : Callable) -> callable:
    """
    Uses currying to provide a response func with all the necsissary data to properly respond
    """
    def respond(message_data : dict, message_dest : User):
        if message_dest == owner_user:
            data = dumps(message_data)
            owner_respond(data)
        elif message_dest == member_user:
            data = dumps(message_data)
            member_respond(data)
        else:
            raise Exception("Invalid response destination")
        
    return respond