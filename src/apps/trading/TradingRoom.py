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

    def __init__(self, room_owner : User, response_func : Callable[[dict, User], None]):
        """
        Constructor for a trading room, sets up the trading room into
        the 'W' or waiting state with only a room_owner
        """

        self.room_owner = room_owner
        self.response_func = response_func

    def handle(self, message_data : dict, message_source : User):
        """
        Handles any message sent by either user, using the data and sender
        to send a proper response through the socket_output function
        """

    # -------------- Internal methods --------------

    def __respond(self, message_data : dict, message_dest : User):
        """
        Validates a response to ensure that its valid, then calls the response_func
        """

        if not (message_dest == self.room_owner or message_dest == self.room_member):
            raise Exception("This room cannot respond to user: " + message_dest.username)
        elif message_dest == None:
            raise Exception("Cannot respond to 'None' user")
        
        self.response_func(message_data, message_dest)
