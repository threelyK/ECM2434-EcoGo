from django.test import TestCase
from django.contrib.auth import get_user_model

from .TradingRoom import TradingRoom

# Create your tests here.

class TradingRoomTest(TestCase):
    """
    The suite of tests for TradingRoom.py
    """

    def setUp(self):
        """
        Run before each test, sets up the users in the trading room
        """

        self.room_owner = get_user_model().objects.create_user(username='123', password='123456789')
        self.room_member = get_user_model().objects.create_user(username='321', password='987654321')

    def test_create_tradingRoom(self):
        """
        Tests that a trading room is properly created
        """

        # define basic mock response_func
        def mock_response_func(data, user):
            if not data == "5":
                self.fail()

        tr = TradingRoom(self.room_owner, mock_response_func)

        self.assertEqual(self.room_owner, tr.room_owner)

        tr.response_func("5", self.room_owner)

    def test_response_func_call_validation(self):
        """
        Tests that the validation funciton for the internal calling of the
        response_func works properly
        """

        # define basic mock response_func
        def mock_response_func(data, user):
            if not data == "5":
                self.fail()

        tr = TradingRoom(self.room_owner, mock_response_func)

        try:
            # 'name mangling' used to access private methods
            tr._TradingRoom__respond("5", None)
        except:
            try:
                tr._TradingRoom__respond("5", None)
                self.fail()
            except:
                return
            
            self.fail()
        
        self.fail()