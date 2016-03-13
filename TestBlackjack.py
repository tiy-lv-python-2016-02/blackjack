from Blackjack import HumanPlayer, ComputerPlayer, Game, Deck, Card
from unittest import TestCase, mock


class HumanPlayerTests(TestCase):
    def setUp(self):
        self.player = HumanPlayer()
        self.player.update_hand(Card("Clubs", "10"))
        self.player.update_hand(Card("Hearts", "6"))

    def test_calculate_hand(self):
        self.player.calculate_hand()
        self.assertEqual(self.player.hand_value, 16)

    def test_update_hand(self):
        self.player.update_hand(Card("Hearts", "A"))
        self.assertEqual(len(self.player.hand), 3)
        self.assertEqual(self.player.hand_value, 17)


class ComputerPlayerTests(TestCase):
    def test_select_action(self):

        self.player = ComputerPlayer()

        self.player.hand_value = 16
        action = self.player.select_action()
        self.assertEqual(action, "H")

        self.player.hand_value = 17
        second_action = self.player.select_action()
        self.assertEqual(second_action, "S")


class GameTest(TestCase):
    def setUp(self):
        self.player1 = HumanPlayer()
        self.player2 = ComputerPlayer()
        self.deck = Deck()

    def test_run_game_blackjack(self):
        """
        Tests that player2 is the winner when dealt a blackjack.
        """
        self.deck.cards.extend([Card("Test", "A"), Card("Test", "2"),
                                Card("Test", "K"), Card("Test", "2")])
        self.game = Game(self.deck, self.player1, self.player2)
        winner = self.game.run_game()
        self.assertEqual(winner, self.player2)

    def test_run_game_player1(self):
        """
        Tests that player1 wins when being dealt a 20 and standing against
        the dealers 19 and that player1 will lose when hitting in that
        same scenario and drawing a 5.
        """
        with mock.patch('builtins.input', side_effect=["S", "H"]):

            self.deck.cards.extend([Card("Test", "9"), Card("Test", "Q"),
                                    Card("Test", "K"), Card("Test", "10")])
            self.game = Game(self.deck, self.player1, self.player2)
            self.assertEqual(self.game.run_game(), self.player1)

            self.deck.cards.extend(
                [Card("Test", "5"), Card("Test", "9"), Card("Test", "Q"),
                 Card("Test", "K"), Card("Test", "10")]
            )
            self.game = Game(self.deck, self.player1, self.player2)
            self.assertEqual(self.game.run_game(), self.player2)
