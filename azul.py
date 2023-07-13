from enum import Enum
import random


BLUE = 0
YELLOW = 1
RED = 2
BLACK = 3
WHITE = 4

TILES = [
    (0, 'BLUE'),
    (1, 'YELLOW'),
    (2, 'RED'),
    (3, 'BLACK'),
    (4, 'WHITE')
]


class TileArray:
    def __init__(self, starting=0):
        self.tiles = [
            starting for _ in range(5)
        ] 

    def update(self, tile: int):
        '''
        Used only on drawbag so far.
        '''
        if self.tiles[tile] > 0:
            self.tiles[tile] -= 1
            return True
        return False  

    def pop_tiles(self, tile: int):
        ''' 
        Use for factory and pool when player makes a selection.
        '''
        quantity = self.tiles[tile]
        self.tiles[tile] = 0
        return tile, quantity
    
    def select_tile(self):
        while True:
            print("Select Tile:")
            for i in range(5):
                print(f"[{i + 1}] - {TILES[i]}")
            tile = int(input()) - 1
            if self.tiles[tile] != 0:
                return self.pop_tiles(tile)
            print("Invalid selection!")

    def is_empty(self):
        for value in self.tiles:
            if value != 0:
                return False
        return True
    
    def print(self):
        for i in range(5):
            print(f"{TILES[i][1]}: {self.tiles[i]}")
        

class Factory(TileArray):
    def __init__(self):
        # Initialize factory tiles dictionary to zero.
        TileArray.__init__(self)
        self.tiles = self.tiles

    def populate(self, drawbag):
        # If drawbag is not empty, draw tiles from drawbag
        # and populate factory tiles dictionary.
        if drawbag.is_empty():
            # Empty lid and refill drawbag
            return False
            
        for i in range(4):
            while True:
                tile = random.randint(0, 4)
                if drawbag.update(tile):
                    self.tiles[tile] += 1
                    break 

class Playerboard:
    def __init__(self):
        self.points = 0
        self.grid = [
            {BLUE: 0, YELLOW: 0, RED: 0, BLACK: 0, WHITE: 0},
            {WHITE: 0, BLUE: 0, YELLOW: 0, RED: 0, BLACK: 0},
            {BLACK: 0, WHITE: 0, BLUE: 0, YELLOW: 0, RED: 0},
            {RED: 0, BLACK: 0, WHITE: 0, BLUE: 0, YELLOW: 0},
            {YELLOW: 0, RED: 0, BLACK: 0, WHITE: 0, BLUE: 0},
        ]

        self.stage = [
            list(),
            list(),
            list(),
            list(),
            list()
        ]

        self.penalties = [
            [-1, -1],
            [-1, -1],
            [-2, -1],
            [-2, -1],
            [-2, -1],
            [-3, -1],
            [-3, -1]
        ]

    def take_penalties(self, quantity):
        if quantity == 0:
            return quantity
        
        index = 0
        for i in range(len(self.penalties)):
            index += self.penalties[i][1]

        if index == 0:
            return quantity

        while quantity:
            self.penalties[index][1] = 0
            quantity -= 1
            index += 1
            if index == 0:
                return quantity
    
    def print_tableau(self):
        for i in range(5):
            row = list(self.grid[i].values())
            for j in range(5):
                if row[j] == 0:
                    print(" --- ", end='')
                    continue
                print(row[j], end='')
            print("  |  ", end='')
            if self.stage[i]:
                for value in self.stage[i]:
                    print(TILES[value][1], end=' ')
            print()

        print(self.penalties)

    def update_tableau(self, tile: int, quantity: int):
        while True:
            for i in range(5):
                print(f"[{i + 1}] - {self.stage[i]}")
            print(f"Select Stage Row to in which to place {quantity} {TILES[tile][1]} tiles:")
            row = int(input()) - 1
            if len(self.stage[row]) == 0:
                for _ in range(row + 1):
                    self.stage[row].append(tile)
                    quantity -= 1
                    if quantity == 0:
                        return 0
                to_lid = self.take_penalties(quantity)
                return to_lid
            elif tile in self.stage[row]:
                pass
            
            print("Row contains a different color. Try Again.")
            continue


class Azul:
    def __init__(self, num_players=2, starting=20):
        # Initialize players.
        self.num_players = num_players
        self.current_player = -1
        self.playerboards = [
            Playerboard() for _ in range(self.num_players)
        ]

        # Initialize factories.
        self.num_factories = (num_players * 2) + 1 # MAXIMUM 4; MINIMUM 2.
        self.factories = [
            Factory() for _ in range(self.num_factories)
        ]

        # Initialize remaining game components.
        self.drawbag = TileArray(starting)
        self.lid = TileArray()
        self.pool = TileArray()
        self.first_player_token = True

    def select_from_factory(self):
        while True:
            # Get factory selection from player.
            print(f"Select Factory <1 - {self.num_factories}>:")
            choice = int(input())
            factory = self.factories[choice - 1]

            # Verify that factory is not empty.
            if factory.is_empty():
                print("Factory is empty. Please select another.")
                continue

            # Given selected factory, get tile choice from player.
            # Move remainder from factory to pool.
            tile, quantity = factory.select_tile()
            for i in range(5):
                if factory.tiles[i] != 0:
                    self.pool.tiles[i] = factory.tiles[i]
                    factory.tiles[i] = 0

            return tile, quantity

    def select_from_pool(self):
        # Selecting from pool, get tile choice from player.
        return self.pool.select_tile()

    def actions(self):
        print("[1] - Factory\n[2] - Pool")
        choice = int(input())
        if choice == 1:
            tile, quantity = self.select_from_factory()
        elif choice == 2:
            tile, quantity = self.select_from_pool()
        return tile, quantity
        
    def play(self):
        # Add tiles to factories
        for factory in self.factories:
            factory.populate(self.drawbag)

        # GAME LOOP
        while True:
            # Establish player turn.
            self.current_player += 1
            self.current_player %= 2

            # Display factories
            for number, factory in enumerate(self.factories):
                print(f"\nFACTORY {number + 1}")
                if factory.is_empty():
                    print()
                else:
                    factory.print()
            
            # Display pool
            print("\nPOOL")
            print(f'First Player Token: {self.first_player_token}')
            self.pool.print()
            
            # Display playerboard
            print(f"\nPLAYER {self.current_player + 1} BOARD")
            self.playerboards[self.current_player].print_tableau()
            
            # Display Player Menu and take action.
            tile, quantity = self.actions()
            
            # Update playerboard
            to_lid = self.playerboards[self.current_player].update_tableau(tile, quantity)
            self.lid.tiles[tile] += to_lid
            print("\nLID")
            print(self.lid.tiles)
            print()
            self.playerboards[self.current_player].print_tableau()
            
            print("\nPress Enter to Continue to Next Player's Turn")
            do_nothing = input()

def main():
    game = Azul()
    game.play()


if __name__ == "__main__":
    main()