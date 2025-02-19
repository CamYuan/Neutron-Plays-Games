class Hand:
    def __init__(self, name="Hand"):
        self.name = name

hands = [Hand("Hand 1"), Hand("Hand 2"), Hand("Hand 3"), Hand("Hand 4")]

while(i<len(hands)):
    print(f"Processing: {hand.name}")
    
    # Insert a new Hand after the current hand (at the next index)
    if hand.name == "Hand 2":
        hands.insert(index + 1, Hand("Hand 5")); 
        index -= 1
        print(f"REMOVED: {hand.name}")
    
    print(f"Current List: {[h.name for h in hands]}")
