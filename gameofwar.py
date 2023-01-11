import random
from time import sleep


SUPERIORITY = {
        "ace"  : 14,
        "king" : 13,
        "queen": 12,
        "jack" : 11,
    }

class Card():
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return f'{self.value} of {self.suit}'


class Deck():
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.build()

    def __repr__(self):
        return f'{self.name}, {self.cards}'

    def build(self):
        for s in ["spades", "clubs", "diamonds", "hearts"]:
            for v in range(2, 11):
                self.cards.append(Card(v, s))
            for f in ["ace", "queen", "king", "jack"]:
                self.cards.append(Card(f, s))

    def split(self):
        self.heap_one = self.cards[:len(self.cards) // 2]
        self.heap_two = self.cards[len(self.cards) // 2:]
        self.cards.clear()
        return self.heap_one, self.heap_two

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()


class Player():
    def __init__(self, name):
        self.hand = []
        self.name = name

    def __repr__(self):
        return f'Player {self.name}'

    def draw_one(self, deck):
        self.hand.append(deck.draw_card())

    def show_hand(self):
        return self.hand

    def count_hand(self):
        return len(self.hand)

    def take_heap(self, heap):
        for card in heap:
            self.hand.insert(0, card)

    def put_card(self):
        if len(self.hand)>0:
            return self.hand.pop()
        else:
            raise GameOverError

    def grab_one(self, card):
        self.hand.insert(0, card)

  
class GameOfWar():
    def __init__(self, player1, player2, deck, verbose=False):
        self.verbose = verbose
        self.player1 = Player(player1)
        self.player2 = Player(player2)
        self.deck = Deck(deck)
        self.deck.shuffle()
        heap1, heap2 = self.deck.split()
        self.player1.take_heap(heap1)
        self.player2.take_heap(heap2)
        self.war_heap = []

    def __repr__(self):
        return f'Game of war between {self.player1} and {self.player2} with {self.deck.name}'

    def get_player_names(self):
        return self.player1, self.player2

    def loot_war_heap(self):
        return self.war_heap

    def clear_war_zone(self):
        self.war_heap = []

    def check_superiority(self, val1, val2):
        if type(val1) != int:
            val1 = SUPERIORITY[val1]
        if type(val2) != int:       
            val2 = SUPERIORITY[val2]
        if val1 > val2:
            return 'player1'
        elif val1 < val2:
            return 'player2'
        else:
            return 'draw'

    def play(self):
        i = 0
        winner = None
        while (winner is None):
            try:
                card1 = self.player1.put_card()
                card2 = self.player2.put_card()
                if self.verbose:
                    print("============================")
                    print(f'{self.player1.name} put {card1}')
                    print(f'{self.player2.name} put {card2}')
                    print("============================")
            except GameOverError:
                if self.player1.hand > self.player2.hand:
                    winner = "player1"
                else:
                    winner = "player2"
                break

            val1 = card1.value
            val2 = card2.value
            tour_winner = self.check_superiority(val1, val2)
            if tour_winner == "player1":
                self.player1.grab_one(card2)
                self.player1.grab_one(card1)
                self.player1.take_heap(self.loot_war_heap())
                self.clear_war_zone()
                if self.verbose:
                    print(f'{self.player1.name} won this tour and has: {len(self.player1.hand)} cards')
            elif tour_winner == "player2":
                self.player2.grab_one(card1)
                self.player2.grab_one(card2)
                self.player2.take_heap(self.loot_war_heap())
                self.clear_war_zone()
                if self.verbose:
                    print(f'{self.player2.name} won this tour and has: {len(self.player2.hand)} cards')
            else:
                if self.verbose:
                    print('*************************')
                    print('WAR!')
                self.war_heap.append(card1)
                self.war_heap.append(card2)
            i += 1
        return i, winner


class GameOverError(IndexError):
    pass


# SIMULATION

def simulation(times):
    sum = 0
    p1_wins = 0
    p2_wins = 0
    for _ in range(0, times):
        game = GameOfWar(player1="Wacek", player2="Jacek", deck="default_deck")
        i, current_winner = game.play()
        sum += i
        if current_winner == "player1":
            p1_wins += 1
        else: 
            p2_wins += 1
    avg = int(sum/times)
    p1_name, p2_name= game.get_player_names()
    print(f'Games played: {times}.')
    print(f'Average length: {avg}.')
    print(f'{p1_name} won {p1_wins} times.')
    print(f'{p2_name} won {p2_wins} times.')


if __name__ == "__main__":
    simulation(1000)

