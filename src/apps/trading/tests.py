from django.test import TestCase
from django.contrib.auth import get_user_model

from .TradingRoom import TradingRoom
from apps.cards.views import get_cards_instance
from apps.cards.models import Card

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

        tr = TradingRoom(self.room_owner)

        self.assertEqual(self.room_owner, tr.room_owner)

    def test_response_func_call_validation(self):
        """
        Tests that the validation funciton for the internal calling of the
        response_func works properly
        """

        # define basic mock response_func
        def mock_response_func(data, user):
            if not data == "5":
                self.fail()

        tr = TradingRoom(self.room_owner)

        tr.response_func = mock_response_func

        tr._TradingRoom__send_message("5", self.room_owner)

        self.assertRaises(Exception, tr._TradingRoom__send_message, "5", None)
        self.assertRaises(Exception, tr._TradingRoom__send_message, "5", self.room_member)

    def test_validate_state(self):
        """
        Tests that the private validate state method works properly
        """

        tr = TradingRoom(self.room_owner)

        try:
            tr._TradingRoom__validate_state("W")
        except:
            self.fail()

        self.assertRaises(Exception, tr._TradingRoom__validate_state, "T")
     
        self.assertRaises(Exception, tr._TradingRoom__validate_state, "N")

            
    def test_update_state(self):
        """
        Tests that the private update_state method works properly
        """

        tr = TradingRoom(self.room_owner)

        #Tests going from 'W' to 'N'
        for state in ['D', 'A', 'W']:
            self.assertRaises(Exception, tr._TradingRoom__update_state, state)

        try:
            tr._TradingRoom__update_state("N")
        except:
            self.fail()
        
        self.assertEqual(tr.state, "N")

        #Tests going from 'N' to 'D'
        for state in ['A', 'W', 'N']:
            self.assertRaises(Exception, tr._TradingRoom__update_state, state)

        try:
            tr._TradingRoom__update_state("D")
        except:
            self.fail()
        
        self.assertEqual(tr.state, "D")

        #Tests going from 'W' to 'A'
        for state in ['W', 'D']:
            self.assertRaises(Exception, tr._TradingRoom__update_state, state)

        try:
            tr._TradingRoom__update_state("A")
        except:
            self.fail()
        
        self.assertEqual(tr.state, "A")

    def test_join_room(self):
        """
        Tests that the join_room method works properly
        """

        #Create a callable class that acts like a function as a mock response_func
        class mock_response_class():
            def __init__(self, outer):
                self.testClass = outer
                self.counter = 0
            
            def __call__(self, data, user):
                #first call
                if self.counter == 0:
                    self.testClass.assertEqual(user, self.testClass.room_owner)
                    self.testClass.assertEqual(data, {
                        "state_flag": 'N',
                        "body": {
                            "username": "321",
                            "level": 0
                        }
                    })
                    self.counter += 1
                #second call
                elif self.counter == 1:
                    self.testClass.assertEqual(user, self.testClass.room_member)
                    self.testClass.assertEqual(data, {
                        "state_flag": 'N',
                        "body": {
                            "username": "123",
                            "level": 0
                        }
                    })
                    self.counter += 1
                #there should not be a third call
                else:
                    self.testClass.fail()

        tr = TradingRoom(self.room_owner)

        rc = mock_response_class(self)

        tr.join_room.__wrapped__(tr, self.room_member, rc)

        self.assertEqual(tr.room_member, self.room_member)
        self.assertEqual(tr.response_func, rc)

    def test_N_to_D_transition_sucess(self):
        """
        Tests the transition from the nutral to the decison state functions properly
        """

        class mock_response_class():
            def __init__(self, outer):
                self.testClass = outer
                self.counter = 0
            
            def __call__(self, data, user):
                #first two calls
                if self.counter == 0 or self.counter == 1:
                    self.counter += 1
                #third call
                elif self.counter == 2:
                    self.testClass.assertEqual(user, self.testClass.room_owner)
                    self.testClass.assertEqual(data["state_flag"], "D")
                    self.counter += 1
                elif self.counter == 3:
                    #ensure the thrid message goes to the room_memeber
                    self.testClass.assertEqual(user, self.testClass.room_member)
                    self.testClass.assertEqual(data["state_flag"], "D")
                    self.counter += 1
                #there should not be a fith call
                else:
                    self.testClass.fail()

        #Init our cards
        get_cards_instance()

        vortex_card = Card.objects.get(card_name = "Vortex-9")
        self.room_member.user_data.add_card(vortex_card)

        tr = TradingRoom(self.room_owner)
        tr.join_room(self.room_member, mock_response_class(self))

        tr.handle({
            "state_flag": "D",
            "body": {
                "member_cards":["Vortex-9"]
            }
        }, self.room_owner)

    def test_N_to_D_transaction_fail(self):
        """
        Tests that the transition from N to D cannot be done if the 
        room member does not have the requested cards
        """

        class mock_response_class():
            def __init__(self, outer):
                self.testClass = outer
                self.counter = 0
            
            def __call__(self, data, user):
                #first two calls
                if self.counter == 0 or self.counter == 1:
                    self.counter += 1
                #third call
                elif self.counter == 2:
                   self.testClass.assertEqual(user, self.testClass.room_owner)
                   self.testClass.assertEqual(data["state_flag"], "N")
                   self.counter += 1
                #there should not be a fourth call
                else:
                    self.testClass.fail()

        tr = TradingRoom(self.room_owner)
        tr.join_room(self.room_member, mock_response_class(self))

        tr.handle({
            "state_flag": "D",
            "body": {
                "member_cards":["Vortex-9"]
            }
        }, self.room_owner)

    def test_error_service_routine(self):
        """
        Test that the error service routine propelry handles errors
        """

        class mock_error_logger():
            def __init__(self, outer):
                self.testClass = outer

            def error(self, msg):
                if not str(msg) == "Something wrong":
                    self.testClass.fail()

        class mock_response_class():
            def __init__(self, outer):
                self.testClass = outer
                self.counter = 0
            
            def __call__(self, data, user):
                #first two calls
                if self.counter == 0 or self.counter == 1:
                    self.counter += 1
                #third call
                elif self.counter == 2:
                    self.testClass.assertEqual(user, self.testClass.room_owner)
                    self.testClass.assertEqual(data["state_flag"], "E")
                    self.counter += 1
                #Fourth call
                elif self.counter == 3:
                    self.testClass.assertEqual(user, self.testClass.room_member)
                    self.testClass.assertEqual(data["state_flag"], "E")
                    self.counter += 1
                #there should not be a fith call
                else:
                    self.testClass.fail()

        tr = TradingRoom(self.room_owner)
        tr.error_logger = mock_error_logger(self)
        tr.join_room(self.room_member, mock_response_class(self))

        e = Exception("Something wrong")
        tr._TradingRoom__error_service_routine(e)

        self.assertEqual(tr.state, 'E')

    def test_user_error_handling(self):
        """
        Tests that an error is properly raised when the user sends an 
        error through the socket
        """

        class mock_error_logger():
            def __init__(self, outer):
                self.testClass = outer

            def error(self, msg):
                if not str(msg) == "Client error: Something wrong":
                    self.testClass.fail()

        class mock_response_class():
            def __init__(self, outer):
                self.testClass = outer
                self.counter = 0
            
            def __call__(self, data, user):
                #first two calls
                if self.counter == 0 or self.counter == 1:
                    self.counter += 1
                #third call
                elif self.counter == 2:
                    self.testClass.assertEqual(user, self.testClass.room_owner)
                    self.testClass.assertEqual(data["state_flag"], "E")
                    self.counter += 1
                #Fourth call
                elif self.counter == 3:
                    self.testClass.assertEqual(user, self.testClass.room_member)
                    self.testClass.assertEqual(data["state_flag"], "E")
                    self.counter += 1
                #there should not be a fith call
                else:
                    self.testClass.fail()

        tr = TradingRoom(self.room_owner)
        tr.error_logger = mock_error_logger(self)
        tr.join_room(self.room_member, mock_response_class(self))

        tr.handle({
            "state_flag" : "E",
            "body":{
                "msg": "Something wrong"
            }
        }, self.room_owner)