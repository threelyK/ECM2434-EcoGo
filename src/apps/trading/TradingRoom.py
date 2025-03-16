"""Module responsable for the state logic of the trading room"""

from apps.user.models import User
from collections.abc import Callable

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

    # -------------- External interface --------------

    def __init__(self, room_owner : User):
        """
        Constructor for a trading room, sets up the trading room into
        the 'W' or waiting state with only a room_owner
        """

        self.room_owner = room_owner

    def handle(self, message_data : dict, message_source : User):
        """
        Handles any message sent by either user, using the data and sender
        to send a proper response through the socket_output function
        """

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
                "level": self.room_member.user_data.level
            }
        }

        message_member = {
            "state_flag": 'N',
            "body": {
                "username": self.room_owner.username,
                "level": self.room_owner.user_data.level
            }
        }

        #Send a message to the users informing them of the change in state
        self.__send_message(message_owner, self.room_owner)
        self.__send_message(message_member, self.room_member)

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
            raise Exception("Invalid state transition")
