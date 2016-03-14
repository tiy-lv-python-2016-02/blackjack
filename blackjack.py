import random
from sys import exit


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return "{} of {}s".format(self.rank, self.suit)

    def value(self):
        if self.rank == 'A':
            return 11
        elif self.rank in ['K', 'J', 'Q']:
            return 10
        else:
            return int(self.rank)

    def __int__(self):
        return self.value()


class Deck:

    suits = ['Heart', 'Club', 'Spade', 'Diamond']
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
        self.blackjack = False
        self.bust = False

    def ace_change(self):
        if sum(self.hand_value) > 21:
            for index, ace in enumerate(self.hand_value):
                if ace == 11:
                    self.hand_value[index] = 1

    def __repr__(self):
        return str(self.name)


class Dealer(Player):

    def dealer_ai(self):
        if sum(self.hand_value) >= 17:
            pass
        while sum(self.hand_value) < 17:
            pass
# if sum of hand value is >= 17, stand
# else hit


class Game:

    def __init__(self, *args, deck=Deck()):
        self.players = list(args)
        self.current_player = self.players[0]
        self.deck = deck
        self.blackjack = False
        self.hit = False
        self.bust = False
        self.player_response = ' '
        self.other_player = self.players[0]

    def shuffle(self):
        self.deck.shuffle()

    def hand_reset(self):
        self.current_player = self.players[0]
        self.current_player.hand_value = []
        self.current_player.hand = []
        self.switch_player()
        self.current_player.hand_value = []
        self.current_player.hand = []
        self.bust = False
        self.blackjack = False

    def deal_hand(self):
            for _ in range(2):
                draw = self.deck.draw()
                self.current_player.hand.append(str(draw))
                self.current_player.hand_value.append(int(draw))

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

    def blackjack_check(self):
        if sum(self.current_player.hand_value) == 21:
            print("\t**BLACKJACK**\n")
            self.current_player.money += 20
            print("""{} GOT BLACKJACK. {}'s BANK NOW AT ${}.00
            """.format(self.current_player,self.current_player,
                       self.current_player.money))
            self.blackjack = True
            return self.blackjack

    def bust_check(self):
        if sum(self.current_player.hand_value) > 21:
            print("BUST!", "{} LOSES.".format(self.current_player), sep="\n")
            self.bust = True
            self.switch_player()
            self.winner_bank()

    def setup_players(self):

        print("\n\t\t  ------ NEW HANDS ------")

        self.current_player = self.players[0]

        for player in self.players:

            self.deal_hand()
            self.current_player.ace_change()
            self.current_player.money -= 10
            print("")
            print("\n{} : {}\n".format(player.name, player.hand))
            print("BANK :: ${}.00".format(player.money))
            print("""HAND VALUE :: {}
            """.format(sum(player.hand_value)))
            self.blackjack_check()
            self.switch_player()
        if not self.blackjack or not self.bust:
            self.current_player = self.players[1]
            self.player_prompt()
        elif self.blackjack:
            self.compare_hands()

    def player_prompt(self):
        while not self.blackjack:
            if not self.bust:
                print("\n{}.\t(H)IT ----- or ----- (S)TAND\n"
                      .format(self.current_player.name))
                self.player_response = " "
                while self.player_response not in "HS":
                    self.player_response = input(">>>").upper()
                if self.player_response == "H":
                    print("HIT\n")
                    self.player_draw()
                elif self.player_response == "S":
                    self.player_stand()
            self.player_response = " "
            break
            # self.show_hand()

    def show_hand(self):
        print("\n{} : {}\n".format(self.current_player.name,
                                   self.current_player.hand))
        print("""HAND VALUE :: {}
                """.format(sum(self.current_player.hand_value)))

    def show_hands(self):
        for _ in self.players:
            self.switch_player()
            self.show_hand()

    def player_draw(self):
        while self.player_response in "H":
            draw = self.deck.draw()
            self.current_player.hand.append(str(draw))
            self.current_player.hand_value.append(int(draw))
            self.current_player.ace_change()
            print("{} ADDED TO YOUR HAND.".format(draw))
            self.bust_check()
            self.player_response = " "
        if not self.bust:
            self.show_hands()
            self.player_prompt()

    def player_stand(self):
        while self.player_response in "S":
            print("\nPLAYER STANDS AT {}."
                  .format(sum(self.current_player.hand_value)))
            self.switch_player()
            self.player_response = " "
        self.dealer_turn()

    def dealer_draw(self):
        draw = self.deck.draw()
        self.current_player.hand.append(str(draw))
        self.current_player.hand_value.append(int(draw))
        self.current_player.ace_change()
        print("{} HITS\n".format(self.current_player.name))
        print("{} ADDED TO {}'s HAND.".format(draw, self.current_player.name))
        # self.show_hand()
        self.bust_check()

    def dealer_turn(self):
        while sum(self.other_player.hand_value) < 17:
            self.dealer_draw()
        self.bust_check()
        self.compare_hands()

    def compare_hands(self):
        print("\n\t\t------ FINAL HANDS ------")
        self.show_hands()
        self.current_player = self.players[1]
        player_total = sum(self.current_player.hand_value)
        dealer_total = sum(self.other_player.hand_value)
        print("TOTAL PLAYER HAND VALUE: {}".format(player_total))
        print("TOTAL DEALER HAND VALUE: {}".format(dealer_total))
        if player_total > dealer_total and not self.bust:
            self.winner_bank()
        elif dealer_total > player_total and not self.bust:
            self.current_player = self.players[0]
            self.winner_bank()
        elif dealer_total == player_total and player_total <= 21:
            self.current_player.money += 10
            self.current_player.money += 10
            print("DRAW.")


if __name__ == '__main__':
    print("""
    \n\tWELCOME TO THE BLACKJACK TRAINER.\n\n
    BANK STARTING AT $100 AND EACH BET IS $10.\n
            """)
    player_one = Player("PLAYER ONE")
    the_dealer = Dealer("DEALER")
    fresh_deck = Deck()
    while player_one.money != 0 and player_one.money != 200:

        fresh_deck = Deck()
        new_game = Game(the_dealer, player_one, deck=fresh_deck)
        new_game.deck.shuffle()
        new_game.setup_players()
        new_game.hand_reset()
        player_one.money = new_game.current_player.money
        print("UPDATED PLAYER BANK :: ${}.00".format(player_one.money))
    if player_one.money == 0:
        print("YOU RAN OUT OF MONEY. GOODBYE.")
        exit()
    else:
        print("YOU WON!")
        exit()

