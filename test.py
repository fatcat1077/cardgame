import random

# Define card suits and values
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = list(range(2, 15))  # Use 2-14 to represent cards 2-10, J, Q, K, A (Ace)

# Create a deck of cards
deck = [(value, suit) for suit in suits for value in values]

def has_straight_flush(hand):
    # Group the cards by suits
    suit_groups = {}
    for value, suit in hand:
        if suit not in suit_groups:
            suit_groups[suit] = []
        suit_groups[suit].append(value)
    
    # Check for straight flush in each suit group
    for values in suit_groups.values():
        values.sort()
        # Check for straight flush: 5 consecutive values
        for i in range(len(values) - 4):
            if values[i + 4] - values[i] == 4:
                return True
    return False

attempts = 0
while True:
    attempts += 1
    # Shuffle the deck and draw 7 cards
    random.shuffle(deck)
    hand = deck[:7]
    
    if has_straight_flush(hand):
        break

print(f'Found a straight flush after {attempts} attempts.')