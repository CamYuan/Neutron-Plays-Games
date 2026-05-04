

'''
    Players should only be making a bet on the initial hand.
    Splitting or doubling down will match the bet already placed.
    This implementation does not allow 'Up-to-current-bet'
    '''

'''
Runs through the hand:
1) Bet
2) Deal the hand
3) Check for blackjacks -> Not offering insurance
4) Payout Blackjacks and remove those hands from the table
5) Let each player make hit/stand/split/doubledown decisions
6) If a player busts, remove the hand from the table
7) Play out the dealer hand
8) Calculate scores
9) Payout
10) Clear the hands/table

If the dealer gets a blackjack, the whole table loses automatically UNLESS
the player also has blackjack, then they PUSH
If a player has blackjack, they win immediately 1.5x the amount they bet

Each player makes a series of decisions
Hitting gives the player a new card and they can then make a new decision
When they choose to stand, they will not get any more cards
If they BUST, they lose immediately
After the players make their choices, the dealer then hits based on
predetermined rules. In this case, they will stay on a Soft 17 or higher

After the dealer makes all their choices, score the table to determine winners
Discard all the cards and get ready for the next hand

'''


BLACKJACK
PreGame:
  - Set up a cardShoe with 6-8 decks.
  - Put a cutCard in the deck somewhere in the back of the shoe (last 30%)


1. Players place bets
    - [] Players can bet between the table min and max
    - [x] Players cannot bet more money than they have
    - [x] Immediately remove their bet from their bankroll
    - [] Players may place side bets
        - [] Bottom 3 bet
        - [] Top 3 bet cannot be placed if bottom 3 is not placed
2. Deal 2 cards to each player and the dealer.
    - [x] Deal 1 card to each person rotating clockwise.
    - [x] Deal the first dealer card face down.
    - [x] 2nd dealer card is face up
    - [x] All player cards are face up
    - [x] Each player and dealer should all have only 1 hand each
- [] Check Side Bets (Rules TBD)
3. Check the dealer's hand for blackjack
    - [x] If the dealer has blackjack, all players who do not also have blackjack lose and the dealer takes their bet
4. Check players hands for blackjack (2 cards with value 21. Only on initial hand)
    - [x] If the player has blackjack, they win immediately for 1.5x their bets
    - [x] Players cannot hit more cards if they have blackjack
5. Clockwise, each player makes some choices about their hand(s)
    - [x] A player may Stand (take no more cards and pass priority to the next player)
    - [x] A Player may hit (get an additional card)
        - [x] If the cutCard is drawn, this will be the last hand played and the shoe will be shuffled
        - [x] After taking a hit, check the value of the players hand
            - [x] If their hand value is over 21, they BUST
                - [x] player loses bet immediately (deducted when they make the bet. Loss is declared later)
            - [x] They may no longer split or double down
    - [x] A player may split (their hand becomes two hands)
        - [x] Their cards must be the same rank to split
        - [x] After splitting, they will be dealt 1 card on their first hand, play through that hand, then they will be dealt another card on their second hand
        - [x] Splitting Aces may only be done once (An AA hand that was created from an already split AA hand cannot be split again)
        - [x] Getting 21 on a split hand is not a natural blackjack, so it will only payout 1x their bet
        - [] Splitting Aces will only bet dealt 1 card on split aces (they cannot hit any more cards)
    - [x] A player may double down (Make an additional bet, take a single additional card, then stand)
        - [x] Players may only double down on their initial two cards
6. After all players have made decisions, show the dealer's hand and act accordingly
    - [x] Dealer must hit on anything under 17
    - [x] Dealer stays on a soft 17. (Some Casinos still hit)
    - [x] If the dealer BUSTS, all remaining players win
7. Calculate the values of all hands for everyone who has not BUST and not BLACKJACK
    - [x] If the player has more value than the dealer, they WIN and get 1x their bet
    - [x] If the player has the same value as the dealer, they PUSH and keep their bet
    - [x] If the player has less than the dealer, they LOSE and the dealer takes their bet
8. At this point, all players should have paid up or been paid out. Discard all hands and get ready for the next round



- TODO: Convert to Json? Don't think so anymore. Don't really need it
- TODO: write better unit tests
- TODO: Code Cleanup and optimization
- TODO: Verify multiple players can play
- TODO: Seperate the dealer into it's own class? would repeat a lot though...
- [x]: Generate Test data for basic Feed Forward Neural Net
    - Feed forward networks have no 'memory' so each hand state will act like an independent hand
- [x]: Train Neural Net on test data
- TODO: Train Neural Net based on Win/Loss to see if it comes up with the same basic strategy
- TODO: Re-do Neural Net with new information
- TODO: Implement Hi-Lo Card Count and other card counting systems
- TODO: Test Neural net efficiency with new information
- TODO: Implement RNN with all information.
- TODO: Test different training strategies and see what is best
- TODO: Throw it all together in a DQRNN maybe
