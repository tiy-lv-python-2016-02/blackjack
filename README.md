### Objectives

After completing this assignment, you should understand:

* how to track state by using objects
* how to design classes to collaborate and communicate
* build an interactive game
* fundamentals of Object Oriented Programing

### Normal Mode

Take your CRC cards and notes and code examples from the planning session and create a game of Blackjack that one person plays on the command line against a computer dealer, with the following rules:

* The only valid moves are hit and stand.
* Allow the player to play as many turns as they want.
* The dealer will stand at 17 (soft or hard)
* The dealer uses one deck and reshuffles after each round.
* [OPTIONAL] The game should start the player with $100 and bets are $10. A player's turn is over when they are out of money

### Hard Mode

In addition to the requirements from **Normal Mode**:

* The dealer uses a shoe of six decks. With a shoe, the dealer uses something called a _cut card_. A plastic card is inserted somewhere near the bottom of the shoe. Once it is hit, the shoe is reshuffled at the end of the round. You can simulate this by reshuffling after there are 26 or less cards left in the shoe.
* Add doubling-down.
* Add surrender (early surrender as opposed to late surrender.)
* Add [insurance](https://en.wikipedia.org/wiki/Blackjack#Insurance).
* Add splitting hands.
* [OPTIONAL] The player can choose how much they want to bet before each round.

### Nightmare Mode

In addition to the requirements from **Hard Mode**:

* Add the ability to choose rulesets, like:
  * No surrender/early surrender/late surrender.
  * Dealer hits soft 17 vs dealer stands of soft 17.
  * Number of decks used in the shoe.

Each choice should be able to be made separately.

### Notes

This is again an assignment with a text-based interface, which can be very hard to test. You will do best at this assignment by building all the logic for each piece and testing it well before then adding the interface on top of it.

### Additional Resources

* [Building Skills in Object-Oriented Design](http://www.itmaybeahack.com/book/oodesign-python-2.1/html/index.html)

