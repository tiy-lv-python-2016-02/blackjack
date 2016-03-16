
import random
from sys import exit
from time import sleep


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)

    def value(self):
        """
        Ace value change in player class
        see: ace_change
        """
        if self.rank == 'A':
            return 11
        elif self.rank in ['K', 'J', 'Q']:
            return 10
        else:
            return int(self.rank)

    def __int__(self):
        return self.value()


class Deck:

    suits = ['Hearts', 'Clubs', 'Spades', 'Diamonds']
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self):
        self.cards = []

        for suit in self.suits:
            for rank in self.ranks:
                self.cards.append(Card(suit, rank))

    def card_count(self):
        return len(self.cards)

    def draw(self):
        card = self.cards.pop(0)
        return card

    def shuffle(self):
        random.shuffle(self.cards)

    def __str__(self):
        return str(self.cards)


class Player:

    def __init__(self, name, money=100):
        self.name = name
        self.money = money
        self.hand = []
        self.hand_value = []
        self.player_response = " "

    def hand_reset(self):
        self.hand = []
        self.hand_value = []

    def ace_change(self):
        """
        If hand value total is over 21
        and there is an ace present, it will
        change the value.
        Can be improved to only change first
        ace. Currently changes all aces.
        """
        if sum(self.hand_value) > 21:
            for index, ace in enumerate(self.hand_value):
                if ace == 11:
                    self.hand_value[index] = 1

    def __repr__(self):
        return str(self.name)


class Dealer(Player):

    def dealer_turn(self):
        """
        Dealer returns hit response if it has less than 17
        otherwise it will tell game it wants to stand.
        """
        while sum(self.hand_value) < 17:
            self.player_response = "H"
            print("DEALER HITS")
            return self.player_response
        self.player_response = "S"


class Game:

    def __init__(self, dealer, player, deck=Deck()):
        self.deck = deck
        self.player = player
        self.dealer = dealer
        self.players = [dealer, player]
        self.current_player = self.players[0]
        self.player_response = ' '
        self.winner = False

    def shuffle(self):
        self.deck.shuffle()

    def deal_hand(self):
        """
        gives every player their first two cards.
        range # can be changed later to use with
        more players
        """
        for _ in range(2):
            draw = self.deck.draw()
            self.current_player.hand.append(str(draw))
            self.current_player.hand_value.append(int(draw))

    def draw_card(self):
        draw = self.deck.draw()
        self.current_player.hand.append(str(draw))
        self.current_player.hand_value.append(int(draw))
        self.current_player.ace_change()

    def winner_bank(self):
        self.current_player.money += 20
        print("""{} WINS. {}'s BANK NOW AT ${}.00
            """.format(self.current_player, self.current_player,
                       self.current_player.money))

    def switch_player(self):

        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
        else:
            self.current_player = self.players[0]

    def prompt(self):
        self.current_player = self.player
        print("\n{}.\t(H)IT ----- or ----- (S)TAND\n"
              .format(self.current_player.name))
        self.player_response = " "
        while self.player_response not in "HS":
            self.player_response = input(">>>").upper()
        if self.player_response == "H":
            print("{} HIT.\n".format(self.current_player))
        elif self.player_response == "S":
            print("{} STANDS.\n".format(self.current_player))
        else:
            print("Please enter valid response.")
        return self.player_response

    def new_hands(self):

        print("\n\t\t  ------ NEW HANDS ------")

        self.current_player = self.players[0]

        for player in self.players:

            self.deal_hand()
            self.current_player.ace_change()
            self.current_player.money -= 10
            print("{} : {}".format(player.name, player.hand))
            print("BANK :: ${}.00".format(player.money))
            print("""HAND VALUE :: {}
            """.format(sum(player.hand_value)))
            self.blackjack_check()
            self.switch_player()

        if not self.winner:
            self.new_round()

    def new_round(self):

        self.current_player = self.player

        while self.current_player == self.players[1]:
            self.bust_check()
            if not self.winner:
                self.prompt()
                self.turn()

        while not self.winner:
            self.dealer.dealer_turn()
            if self.dealer.player_response == "H":
                self.draw_card()
                self.show_hand()
                self.bust_check()
                self.player_response = " "
            else:
                self.compare_hands()

    def turn(self):
        if self.player_response == "H":
            self.draw_card()
            self.show_hands()
            self.player_response = " "
        elif self.player_response == "S":
            self.bust_check()
            self.switch_player()
            self.player_response = " "

    def show_hand(self):
        print("{} : {}".format(self.current_player.name,
                                   self.current_player.hand))
        print("""HAND VALUE :: {}
                """.format(sum(self.current_player.hand_value)))

    def show_hands(self):
        for _ in self.players:
            self.switch_player()
            self.show_hand()

    def bust_check(self):
        if sum(self.current_player.hand_value) > 21:
            print("BUST!", "{} LOSES.".format(self.current_player), sep="\n")
            self.winner = True
            self.switch_player()
            self.winner_bank()
        return self.winner

    def blackjack_check(self):
        if sum(self.current_player.hand_value) == 21:
            print("\t**BLACKJACK**\n")
            self.current_player.money += 20
            print("""{} GOT BLACKJACK. {}'s BANK NOW AT ${}.00
            """.format(self.current_player.name, self.current_player.name,
                       self.current_player.money))
            self.winner = True
            sleep(2)

        return self.winner

    def compare_hands(self):
        print("\n\t\t------ FINAL HANDS ------")
        self.show_hands()
        self.current_player = self.players[1]
        player_total = sum(self.player.hand_value)
        dealer_total = sum(self.dealer.hand_value)
        print("TOTAL PLAYER HAND VALUE: {}".format(player_total))
        print("TOTAL DEALER HAND VALUE: {}".format(dealer_total))
        if player_total > dealer_total and not self.winner:
            self.winner_bank()
        elif dealer_total > player_total and not self.winner:
            self.current_player = self.players[0]
            self.winner_bank()
        elif dealer_total == player_total and player_total <= 21:
            self.current_player.money += 10
            self.current_player.money += 10
            print("DRAW.")
        self.winner = True


if __name__ == '__main__':

    print("""
    \n\tWELCOME TO THE BLACKJACK TRAINER.\n\n
    BANK STARTS AT $100 AND EACH BET IS $10.\n
            """)

    player_one = Player("PLAYER ONE")
    the_dealer = Dealer("DEALER")

    while player_one.money != 0 and player_one.money != 200:

        fresh_deck = Deck()
        new_game = Game(the_dealer, player_one, fresh_deck)
        new_game.deck.shuffle()
        player_one.hand_reset()
        the_dealer.hand_reset()
        new_game.new_hands()

    if player_one.money == 0:
        print("YOU RAN OUT OF MONEY. GOODBYE.")
        exit()
    else:
        print("\tYOU WON!")
        exit()

