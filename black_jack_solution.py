import random
suits = ('Hearts','Diamonds','Blades','Clubs')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')

values = {'Two': 2,'Three': 3,'Four': 4,'Five': 5,'Six': 6,'Seven': 7,'Eight': 8,'Nine': 9,'Ten': 10,'Jack': 10,'Queen': 10,'King': 10,'Ace': 11}

playing = True

class Card():
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
    
    def __str__(self):
        return self.rank + " of " + self.suit

class Deck():
    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit,rank))
    def shuffle(self):
        random.shuffle(self.all_cards)
    def deal_one(self):
        return self.all_cards.pop()
    def __str__(self):
        deck_comp = ''
        for card in self.all_cards:
            deck_comp += '\n' + card.__str__()
        return 'The deck has: '+deck_comp

class Hand():
    def __init__(self):
        self.cards=[]
        self.value= 0
        self.aces = 0

    def add_cards(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        #track aces
        if card.rank == 'Ace':
            self.aces += 1
    def adjust_for_ace(self):
        # If total value > 21 and I still have an ace
        # Than, change my ace to be a 1 instead of an 11
        while self.value >21 and self.aces:
            # self.aces is an integer used as truthiness -> convert the integer as a boolean. 
            # If 'any integer =/ 0 ' it returns 
            self.value -= 10
            self.aces -= 1

class Chips:
    def __init__(self):
        self.total = 100 #this can be default value or supplied by a user input
        self.bet = 0
    def win_bet(self):
        self.total += self.bet
    def lose_bet(self):
        self.total -= self.bet

##### Creating functions to use #####

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except:
            print('Sorry, please provide an integer')
        else:
            if chips.bet>chips.total:
                print('Sorry you do not have enough chips! You have: {}'.format(chips.total))
            else:
                break
def hit(deck,hand):
    single_card = deck.deal_one()
    hand.add_cards(single_card)
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing #to control an upcoming while loop

    while True:
        x=input('Hit or Stand? Enter H or S: ')
        if x[0].lower()== 'h':
            hit(deck,hand)
        elif x[0].lower() == 's':
            playing = False
        else:
            print('Sorry, I did not understand that. Please, enter H or S only: ')
            continue
        break

######### Display cards function #########
def show_some(player,dealer):
    # dealer.cards[0,1] -> he only has 2 cards and that is their place in coding
    # But only 1 of the dealer cards #
    print("\n Dealer's hand: ")
    print("First card hidden!")
    print(dealer.cards[1])

    # Show all (2 cards at the start) of the player cards #
    print("\n Player's hand: ")
    for card in player.cards:
        print(card)

def show_all (player, dealer):
    # Show ALL dealer cards #
    ## Calculate and display value ##
    print("\n Dealer's hand: ")
    for card in dealer.cards:
        print(card)
    
    #print("\n Dealer's hand: ", *dealer.cards,sep='\n') -> *dealer.cards going to loop through every item on that list - 
    # and the sep = separator , indicates how the list will separate. If we do not use it will be separate with an space

        ## Calculate and display value ##
    print(f"Value of Dealer's hand is: {dealer.value}")
    
    # Show ALL player cards #

    print("\n Player's hand: ")
    for card in player.cards:
        print(card)

        ## Calculate and display value ##
    print(f"Value of Dealer's hand is: {player.value}")

###### functions to hande end of game scenarios ######

def player_busts(player, dealer, chips):
    print('Bust Player!')
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print('Player WINS!')
    chips.win_bet()

def dealer_bust(player, dealer, chips):
    print('Player WINS! Dealer Busted!')
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print('Dealer Wins!')
    chips.lose_bet()

def push(player, dealer, chips):
    print('Dealer and player tie! PUSH')


################################### SETTING THE GAME ###################################

while True:
    #Print on open statetment:
    print('Welcome to BlackJack')
    
    # Creat and shuffle the deck
    deck = Deck()
    deck.shuffle

    #Setup Players - Deal 2 cards each
    player_hand = Hand()
    player_hand.add_cards(deck.deal_one())
    player_hand.add_cards(deck.deal_one())
    
    dealer_hand = Hand()
    dealer_hand.add_cards(deck.deal_one())
    dealer_hand.add_cards(deck.deal_one())

    #Setup Player's chips:
    player_chips = Chips()

    #Prompt the Player for their bet
    take_bet(player_chips)

    #Show cards - keeping 1 of dealer's hand hidden
    show_some(player_hand,dealer_hand)

    while playing: #recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)

        # Show cards(but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)
        # If player's hand exceed 21, run player_busts() and break the loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
        break
    # If Player hasn't busted, play Dealer's hand until Dealeer reached 17
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck,dealer_hand)

        #Show all cards
        show_all(player_hand,dealer_hand)
        
        #Run different winner scenarios
        if dealer_hand.value > 21:
            dealer_bust(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)
    
    # Inform Player of their chips total
    print(f'\n Player total chips are at: {player_chips.total}')

    # Ask to play again:
    new_game = input('Would you like to play another hand? Y/N ')
    if new_game[0].lower()== 'y':
        playing = True
        continue
    else:
        print('Thanks for playing')
        break