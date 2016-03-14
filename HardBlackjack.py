import random


class Hand:

    def __init__(self):
        self.cards = []
        self.hand_value = 0

    def calculate_hand(self):
        amount = [card.value for card in self.cards]
        while sum(amount) > 21 and 11 in amount:
            first_ace = amount.index(11)
            amount[first_ace] = 1
        self.hand_value = sum(amount)

    def update_hand(self, card):
        self.cards.append(card)
        self.calculate_hand()

    def get_hand_value(self):
        return self.hand_value

    def bust(self):
        return self.hand_value > 21

    def has_blackjack(self):
        return self.hand_value == 21 and len(self.cards) == 2

    def player_options(self):
        options = {"S": "Stand"}
        if self.hand_value < 21:
            options["H"] = "Hit"
        if len(self.cards) == 2:
            options["U"] = "Surrender"
        return options

    def clear_cards(self):
        self.cards = []


class HumanPlayer:

    def __init__(self, money=100, bet_amount=10):
        self.money = money
        self.hand_value = 0
        self.title = "Player"
        self.bet_amount = bet_amount

    def select_action(self, hand_value, options):

        print("Please choose an action")
        for key, val in options.items():
            print("{}: {}".format(val, key))
        action = " "
        while action not in list(options.keys()):
            action = input(":: ").upper()
        return action

    def winning_hand(self, win):
        if win:
            self.money += self.bet_amount
        else:
            self.money -= self.bet_amount

    def surrender(self):
        self.money -= self.bet_amount * 0.5

    def count_money(self):
        return self.money

    def win_three_two(self):
        # For blackjacks that pay 3-2
        self.money += self.bet_amount * 1.5


class ComputerPlayer(HumanPlayer):

    def __init__(self, money=100):
        super().__init__(money=100)
        self.money = money
        self.title = "Dealer"

    def select_action(self, hand_value, options):
        """
        :param options: Not used in this version of player
        :return:
        """

        if hand_value >= 17:
            return "S"
        elif hand_value < 17:
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
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self):
        self.cards = []
        self.used_cards = []

        for suit in self.suits:
            for rank in self.ranks:
                card = Card(suit, rank)
                self.cards.append(card)

    def draw(self):
        card = self.cards.pop(0)
        self.used_cards.append(card)
        return card

    def card_count(self):
        return len(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def reshuffle(self):
        self.cards.extend(self.used_cards)
        self.shuffle()

    def __str__(self):
        return str(self.cards)


class Shoe(Deck):

    single_deck = Deck()

    def __init__(self, num_decks):
        super().__init__()
        self.num_deck = num_decks
        self.cards = []

        for _ in range(num_decks):
            self.cards.extend(self.single_deck.cards)


class Turn:

    def __init__(self, player, hand, deck):
        self.player = player
        self.hand = hand
        self.deck = deck
        self.end = False

    def display_hand(self):
        print(
            "{} total: {}".format(self.player.title,
                                  self.hand.get_hand_value())
        )
        for card in self.hand.cards:
            print(card)
        print("")

    def single_hand_turn(self, hand):
        action = ""
        self.display_hand()
        while action != "S" and hand.get_hand_value() <= 21:

            # Get options for the player from the hand class
            options = hand.player_options()

            action = self.player.select_action(hand.get_hand_value(), options)

            if action == "U":
                self.player.surrender()
                print("You get back half of your money.")
                self.end = True
                return self.player, self.hand, deck, self.end

            elif action == "H":
                next_card = self.deck.draw()
                self.hand.update_hand(next_card)
                self.display_hand()

    def run_turn(self):

        hand = self.hand
        self.single_hand_turn(hand)

        return self.player, self.hand, deck, self.end


class Game:

    def __init__(self, deck, player1, player2):
        self.deck = deck
        self.player1 = player1
        self.player2 = player2
        self.hand1 = Hand()
        self.hand2 = Hand()
        self.players = [self.player1, self.player2]
        self.hands = [self.hand1, self.hand2]

    def initial_deal(self):

        self.hand1.clear_cards()
        self.hand2.clear_cards()

        for _ in range(2):  # Change to handle optional number of players.
            self.hand1.update_hand(self.deck.draw())
            self.hand2.update_hand(self.deck.draw())

    def display_board(self):
        print("", "Dealer hand:", "X", self.hand2.cards[1], "", "", sep="\n")

    def print_cards(self, hand):
        for card in hand.cards:
            print(card)

    def resolve_message(self):

        first = self.hand1.get_hand_value()
        second = self.hand2.get_hand_value()

        if first > second:
            print("You win!")
            self.player1.winning_hand(True)
        elif first < second:
            print("The dealer wins")
            self.player1.winning_hand(False)

        else:
            print(self.hand1.get_hand_value(), self.hand2.get_hand_value())
            print("It is a draw")

    def game_prompt(self):
        print("You currently have ${}".format(self.player1.money))
        prompt = input("Do you want to continue? [y/n]").lower()
        return prompt[0] != "n"

    def run_game(self):

        print("\nGreetings. You have ${} dollars.".format(self.player1.money))

        self.initial_deal()

        if self.hand1.has_blackjack():
            print("You were dealt a blackjack!")
            self.player1.win_three_two()
            return self.game_prompt()
        elif self.hand2.has_blackjack():
            print("Dealer was dealt a blackjack")
            self.player1.winning_hand(False)
            return self.game_prompt()

        for i in range(len(self.players)):
            self.display_board()
            print("**********" * 5)
            turn = Turn(self.players[i], self.hands[i], self.deck)
            self.players[i], self.hands[i], self.deck, end = turn.run_turn()

            # end is a boolean returned by Turn for whether or not to continue
            # with the following evaluation.
            if end:
                return self.game_prompt()

            if self.hand1.bust():
                print("Player busted")
                self.player1.winning_hand(False)
                return self.game_prompt()
            elif self.hand2.bust():
                print("The Dealer busted")
                self.player1.winning_hand(True)
                return self.game_prompt()

        self.resolve_message()
        return self.game_prompt()

    def run(self):
        another_game = True

        while another_game and self.player1.count_money() >= 10:

            if deck.card_count() < 26:  # Reshuffle at cut card.
                self.deck.reshuffle()

            another_game = self.run_game()

        print("You ended with ${}".format(self.player1.money))


if __name__ == '__main__':
    player1 = HumanPlayer()
    player2 = ComputerPlayer()

    deck = Shoe(6)
    deck.shuffle()

    game = Game(deck, player1, player2)
    game.run()
