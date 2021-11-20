import random


class Card():
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def show(self):
        print(f'{self.value} of {self.suit}')

    def return_value(self):
        return self.value


class Deck():
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.build()

    def build(self):
        for s in ["spades", "clubs", "diamonds", "hearts"]:
            for v in range(2, 11):
                self.cards.append(Card(v, s))
            for f in ["ace", "queen", "king", "jack"]:
                self.cards.append(Card(f, s))
        random.shuffle(self.cards)

    def split(self):
        all_cards = self.cards
        first_heap = all_cards[:len(all_cards) // 2]
        second_heap = all_cards[len(all_cards) // 2:]
        return first_heap, second_heap

    def show(self):
        for card in self.cards:
            card.show()

    def shuffle(self):
        print("shuffling...")
        random.shuffle(self.cards)
        print(f'{self.name} is shuffled.'.capitalize())

    def draw_card(self):
        return self.cards.pop()


class Player():
    def __init__(self, name):
        self.hand = []
        self.name = name

    def draw(self, deck):
        self.hand.append(deck.draw_card())

    def show_hand(self):
        for card in self.hand:
            card.show()

    def count_hand(self):
        return len(self.hand);

    def take_heap(self, heap):
        for card in heap:
            self.hand.insert(0, card)

    def put_card(self):
        return self.hand.pop()

    def grab(self, card):
        self.hand.insert(0, card)


class GameOfWar():
    def __init__(self, player1, player2, deck):
        self.player1 = Player(player1)
        self.player2 = Player(player2)
        self.deck = Deck(deck)
        heap1, heap2 = self.deck.split()
        self.player1.take_heap(heap1)
        self.player2.take_heap(heap2)
        self.war_heap = []

    def war_zone(self, card1, card2):
        self.war_heap.append(card1)
        self.war_heap.append(card2)

    def war_prize(self):
        return self.war_heap

    def clear_war_zone(self):
        self.war_heap = []

    def check_superiority(self, val1, val2):
        if val1 == "king":
            val1 = 13
        if val1 == "queen":
            val1 = 12
        if val1 == "jack":
            val1 = 11
        if val1 == "ace":
            val1 = 14
        if val2 == "king":
            val2 = 13
        if val2 == "queen":
            val2 = 12
        if val2 == "jack":
            val2 = 11
        if val2 == "ace":
            val2 = 14
        if val1 > val2:
            return 'player1'
        elif val1 < val2:
            return 'player2'
        else:
            return 'draw'

    def play(self):
        i = 0
        winner = ''
        while (self.player1.hand != [] or self.player2.hand != []):
            try:
                card1 = self.player1.put_card()
                card2 = self.player2.put_card()
            except:
                if self.player1.hand > self.player2.hand:
                    winner = "player1"
                else:
                    winner = "player2"
                break

            val1 = card1.return_value()
            val2 = card2.return_value()
            tour_winner = self.check_superiority(val1, val2)
            if tour_winner == "player1":
                self.player1.grab(card2)
                self.player1.grab(card1)
                self.player1.take_heap(self.war_prize())
                self.clear_war_zone()
            elif tour_winner == "player2":
                self.player2.grab(card1)
                self.player2.grab(card2)
                self.player2.take_heap(self.war_prize())
                self.clear_war_zone()
            else:
                self.war_zone(card1, card2)
                self.check_superiority(val1, val2)
            i += 1
        return i, winner


# SIMULATION

def simulation(times):
    sum = 0
    p1_wins = 0
    p2_wins = 0
    for _ in range(0, times):
        gra = GameOfWar(player1="Pierwszy", player2="Drugi", deck="first_deck")
        i, current_winner = gra.play()
        sum += i
        if current_winner == "player1":
            p1_wins += 1
        else: 
            p2_wins += 1
    avg = int(sum/times)
    print(f'Games played: {times}.')
    print(f'Average length: {avg}.')
    print(f'Player1 won {p1_wins} times.')
    print(f'Player2 won {p2_wins} times.')


simulation(1000)

