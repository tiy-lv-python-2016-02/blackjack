import random


class HumanPlayer:

    def __init__(self):
        self.hand_value = 0
        self.hand = []
        self.title = "Player"

    def select_action(self):
        """
        :return: Action from player input.
        """
        print("Please pick an action", "Hit: H", "Stand: S", sep="\n")
        action = " "
        while action not in "HS":
            action = input(":: ").upper()
        return action

    def update_hand(self, card):
        """
        Adds a card to hand and recalculates hand value.
        :param card: Accepts a card that has been popped off the deck.
        :return: Updated hand and hand value.
        """
        self.hand.append(card)
        self.calculate_hand()

    def calculate_hand(self):
        """
        Calculates the hand value, adjusts the value of an Ace when necessary.
        :return: Hand value.
        """
        amount = [card.value for card in self.hand]
        while sum(amount) > 21 and 11 in amount:
            first_ace = amount.index(11)
            amount[first_ace] = 1
        self.hand_value = sum(amount)

    def get_hand_value(self):
        """
        :return: The value of the players hand.
        """
        return self.hand_value

    def bust(self):
        """
        :return: Boolean whether a hand has busted.
        """
        return self.hand_value > 21

    def has_blackjack(self):
        """
        :return: Boolean value of whether or not a hand is a blackjack.
        """
        return self.hand_value == 21 and len(self.hand) == 2


class ComputerPlayer(HumanPlayer):

    def __init__(self):
        super().__init__()
        self.title = "Dealer"

    def select_action(self):
        """
        Simple computer player, always stands on 17.
        :return: Hit or stand.
        """
        if self.get_hand_value() >= 17:
            return "S"
        elif self.get_hand_value() < 17:
            return "H"


class Card:
    """
    The value for an ace is initially set to 11 and adjusted down when needed
    by the calculate_hand() method in Player class.
    """

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

        if self.rank in "JQK":
            self.value = 10
        elif self.rank == "A":
            self.value = 11
        else:
            self.value = int(self.rank)

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)


class Deck:

    suits = ['Hearts', 'Clubs', 'Spades', 'Diamonds']
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self):
        self.cards = []

        for suit in self.suits:
            for rank in self.ranks:
                card = Card(suit, rank)
                self.cards.append(card)

    def draw(self):
        """
        :return: Deals the next card off the deck.
        """
        card = self.cards.pop(0)
        return card

    def card_count(self):
        """
        :return: Number of cards remaining in deck.
        """
        return len(self.cards)

    def shuffle(self):
        """
        :return: Shuffles the un-dealt cards in the deck.
        """
        random.shuffle(self.cards)

    def __str__(self):
        return str(self.cards)


class Game:

    def __init__(self, deck, player1, player2):
        self.deck = deck
        self.player1 = player1
        self.player2 = player2
        self.players = [self.player1, self.player2]

    def initial_deal(self):
        """
        :return: Deals two cards to each player from the deck.
        """

        for _ in range(2):
            self.player1.update_hand(self.deck.cards.pop())
            self.player2.update_hand(self.deck.cards.pop())

    def print_cards(self, player):
        """
        :param player: Any player that is passed in.
        :return: Prints out player's cards one at a time.
        """
        for card in player.hand:
            print(card)

    def display(self):
        """
        A display method to show the board information to the user.
        :return: One dealer card and all player cards are printed.
        """
        print("", "Dealer hand:", "X", self.player2.hand[1], "", "", sep="\n")
        print("Player total: {}".format(self.player1.get_hand_value()))
        self.print_cards(self.player1)
        print("")

    def resolve_message(self):
        """
        Compares hand values and prints winner.
        :return: The winning player object.
        """
        print("Dealer total: {}".format(self.player2.get_hand_value()))
        self.print_cards(self.player2)
        if self.player1.get_hand_value() > self.player2.get_hand_value():
            print("You win!")
            return self.player1
        elif self.player1.get_hand_value() < self.player2.get_hand_value():
            print("The dealer wins")
            return self.player2
        else:
            print(self.player1.get_hand_value(), self.player2.get_hand_value())
            print("It is a draw")

    def run_game(self):
        """
        Runs the main game. Responsible for the deals, player action and
        discerning the winner.
        :return: Winning player.
        """
        self.initial_deal()
        for player in self.players:
            if player.has_blackjack():
                print("{} was dealt a blackjack!".format(player.title))
                return player

        for player in self.players:
            action = " "
            while action != "S" and player.get_hand_value() <= 21:
                self.display()
                action = player.select_action()
                if action == "H":
                    next_card = self.deck.cards.pop()
                    player.update_hand(next_card)

            if player.bust():
                print("{} has gone bust".format(player.title))
                self.print_cards(player)
                print("Game over")

                if self.player1.bust():
                    return self.player2
                else:
                    return self.player1

        return self.resolve_message()


if __name__ == '__main__':

    player1 = HumanPlayer()
    player2 = ComputerPlayer()

    # Deck is instantiated and shuffled outside of Game so that it can
    # more easily be changed and/or stacked for testing.
    deck = Deck()
    deck.shuffle()

    game = Game(deck, player1, player2)
    game.run_game()
