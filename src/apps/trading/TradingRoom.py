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
        the 'w' or waiting state with only a room_owner
        """

    def handle(self, message_data : dict, message_source : User):
        """
        Handles any message sent by either user, using the data and sender
        to send a proper response through the socket_output function
        """

    
