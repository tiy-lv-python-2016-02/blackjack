import random

# One thing to a function

# Decorator should return a value, not an action

# Keep hand logic to player, or a hand object. Do not have values or amount
# checking in game function. It should ask the player and player will return
# what the game needs to know. Example: Player.has_blackjack()

class Hand:
    pass


class HumanPlayer:

    # Move Dealer/Player print words into player classes, access with format.

    # Just one hand object for now, change it to a list in harder modes.

    def __init__(self, player_number, money=100):
        self.money = money
        self.hand_value = 0
        self.hand = []
        self.player_number = player_number
        self.title = "Player"

    def select_action(self):
        print("Please pick an action", "Hit: H", "Stand: S", sep="\n")
        action = " "
        while action not in "HS":
            action = input(":: ").upper()
        return action

    def update_hand(self, card):
        self.hand.append(card)
        self.calculate_hand()

    def calculate_hand(self):
        amount = [card.value for card in self.hand]
        while sum(amount) > 21 and 11 in amount:
            first_ace = amount.index(11)
            amount[first_ace] = 1
        self.hand_value = sum(amount)

    def get_hand_value(self):
        return self.hand_value

    def bust(self):
        return self.hand_value > 21

    def has_blackjack(self):
        return self.hand_value == 21 and len(self.hand) == 2

    def update_money(self):
        pass


class ComputerPlayer(HumanPlayer):

    def __init__(self,player_number, money=100):
        super().__init__(player_number, money=100)
        self.money = money
        self.player_number = player_number
        self.title = "Dealer"

    def select_action(self):
        if self.get_hand_value() >= 17:
            return "S"
        elif self.get_hand_value() < 17:
            return "H"


class Card:

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
    ranks = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']

    def __init__(self):
        self.cards = []

        for suit in self.suits:
            for rank in self.ranks:
                card = Card(suit, rank)
                self.cards.append(card)

    def draw(self):
        card = self.cards.pop(0)
        return card

    def card_count(self):
        return len(self.cards)

    def shuffle(self):
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

        for _ in range(2):
            self.player1.update_hand(self.deck.cards.pop())
            self.player2.update_hand(self.deck.cards.pop())

    def print_cards(self, player):
        for card in player.hand:
            print(card)

    def display(self):
        print("", "Dealer hand:", "X", self.player2.hand[1],"", "", sep="\n")
        print("Player total: {}".format(self.player1.get_hand_value()))
        self.print_cards(self.player1)
        print("")

    def resolve_message(self):
        """
        Compares hand values and print winner. The winning player number
        is returned for testing purposes and later formatting options.
        :return: The player_number of the winning player.
        """
        print("Dealer total: {}".format(self.player2.get_hand_value()))
        self.print_cards(self.player2)
        first = self.player1.get_hand_value(), self.player1.player_number
        second = self.player2.get_hand_value(), self.player2.player_number
        if first[0] > second[0]:
            print("You win!")
            return first[1]
        elif first[0] < second[0]:
            print("The dealer wins")
            return second[1]
        else:
            print(self.player1.get_hand_value(), self.player2.get_hand_value())
            print("It is a draw")

    def run_game(self):
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
                return
        self.resolve_message()


if __name__ == '__main__':
    player1 = HumanPlayer(1)
    player2 = ComputerPlayer(2)
    deck = Deck()
    deck.shuffle()  # Put here for testing, debugging.
    #deck.cards.extend()
    game = Game(deck, player1, player2)
    game.run_game()

# Fix run_game() returns, pass around player objects









