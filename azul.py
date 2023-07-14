import random
from enum import Enum


class Color(Enum):
    BLUE = 0
    YELLOW = 1
    RED = 2
    BLACK = 3
    WHITE = 4


class Tile:
    def __init__(self, color: Color):
        self.name = color.name
        self.index = color.value
        self.color = color

    def __repr__(self):
        return str(self.name)


class TileMatrix:
    def __init__(self, num_tiles=0):
        self.tiles = [
            list(Tile(Color.BLUE) for _ in range(num_tiles)),
            list(Tile(Color.YELLOW) for _ in range(num_tiles)),
            list(Tile(Color.RED) for _ in range(num_tiles)),
            list(Tile(Color.BLACK) for _ in range(num_tiles)),
            list(Tile(Color.WHITE) for _ in range(num_tiles))
        ]

    def get_tiles_of_color(self, color: Color):
        '''
        Get tiles of only specified color. Useful as when player
        is selecting tiles from a factory or the pool on their turn.
        '''
        tile_set = None
        if self.tiles[color.value]:
            tile_set = self.tiles[color.value]
            self.tiles[color.value].clear()
        return tile_set

    def get_all_tiles(self):
        '''
        Empty all tiles from TileMatrix object
        and return them in tile set.
        '''
        tile_set = []
        for tiles in self.tiles:
            if tiles:
                tile_set.extend(tiles)
                tiles.clear()
        return tile_set

    def is_empty(self):
        '''
        Check if TileMatrix is empty. Called from is_empty 
        method in FactorySet class.
        '''
        for tile_set in self.tiles:
            if tile_set:
                return False
        return True
    
    def print(self):
        '''
        Print all tiles in TileMatrix.
        '''
        for tile_set in self.tiles:
            print(tile_set)


class DrawBag(TileMatrix):
    def draw(self):
        '''
        Draws a single random tile from drawbag if available.
        Used to add tiles to a factory. called from add_tiles
        method in Factory class.
        '''
        while True:
            select = random.randint(0, 4)
            if not self.tiles[select]:
                continue

            tile = self.tiles[select].pop()
            return tile


class Factory(TileMatrix): 
    def add_tiles(self, drawbag: DrawBag, lid: TileMatrix):
        '''
        Get tiles from drawbag, and if drawbag is depleted,
        refill drawbag from lid. Called from add_tiles method
        in FactorySet class.
        '''
        for _ in range(4):
                if drawbag.is_empty():
                    tile_set = lid.get_all_tiles()
                    for tile in tile_set:
                        drawbag.tiles[tile.index].append(tile)
                tile = drawbag.draw()
                self.tiles[tile.index].append(tile)

    def print(self):
        '''
        Print a single given factory. Called from print
        method in FactorySet class.
        '''
        number = 1
        for row in self.tiles:
            if row:
                print(f"[{number}] - {row}")
                number += 1


class FactorySet:
    def __init__(self, num_factories):
        self.factories = [
            Factory() for _ in range(num_factories)
        ]

    def add_tiles(self, drawbag: DrawBag, lid: TileMatrix):
        '''
        Draw tiles from drawbag to populate each factory.
        If drawbag is depleted, refill drawbag from lid and continue.
        '''
        for factory in self.factories:
            factory.add_tiles(drawbag, lid)
    
    def choose_tiles(self):
        '''
        Select tile of one color from a single factory.
        Useful as when player is selecting tiles from a
        factory or the pool on their turn. 
        '''
        pass

    def is_empty(self):
        '''
        Iterate through FactorySet using TileMatrix.is_empty() for each factory.
        '''
        for factory in self.factories:
            if not factory.is_empty():
                return False
        return True

    def print(self):
        '''
        Display each factory and the tiles they hold.
        Useful as when player is taking their turn.
        '''
        factory_num = 1
        for factory in self.factories:
            print(f'FACTORY {factory_num}')
            number = 1
            for row in factory.tiles:
                if not row:
                    continue
                print(f"[{number}] - {row}")
                number += 1
            print()
            factory_num += 1


class Playerboard:
    def __init__(self):
        self.points = 0
        self.first_player_token = False
        self.stage = TileMatrix()
        self.mosaic = [
            {Color.BLUE.name: None, Color.YELLOW.name: None, Color.RED.name: None, Color.Black.name: None, Color.WHITE.name: None},
            {Color.YELLOW.name: None, Color.RED.name: None, Color.Black.name: None, Color.WHITE.name: None, Color.BLUE.name: None},
            {Color.RED.name: None, Color.Black.name: None, Color.WHITE.name: None, Color.BLUE.name: None, Color.YELLOW.name: None},
            {Color.Black.name: None, Color.WHITE.name: None, Color.BLUE.name: None, Color.YELLOW.name: None, Color.RED.name: None},
            {Color.WHITE.name: None, Color.BLUE.name: None, Color.YELLOW.name: None, Color.RED.name: None, Color.Black.name: None},
        ]
        self.penalties = [
            [-1, None],
            [-1, None],
            [-2, None],
            [-2, None],
            [-2, None],
            [-3, None],
            [-3, None]
        ]

    def tessellate(self, lid: TileMatrix):
        '''
        For any full stage row, place one of its tiles in the mosaic
        and the remainder, if there are any, in the lid.
        '''
        for number, row in enumerate(self.stage):
            if number + 1 == len(row):
                tile = row.pop()
                self.mosaic[number][tile.name] = tile
                while row:
                    tile = row.pop()
                    lid.tiles[tile.index].append(tile)

    def take_penalties(self, lid: TileMatrix):
        '''
        Check population of penalty row, update player score,
        and discard tiles into the lid.
        '''
        penalty = 0
        for row in self.penalties:
            if row[1] is not None:
                penalty += row[0]
                tile = row.pop()
                lid.tiles[tile.index].append(tile)

        self.points += penalty
        if self.points < 0:
            self.points = 0
    
    # def print_tableau(self):
    #     for i in range(5):
    #         row = list(self.grid[i].values())
    #         for j in range(5):
    #             if row[j] == 0:
    #                 print(" --- ", end='')
    #                 continue
    #             print(row[j], end='')
    #         print("  |  ", end='')
    #         if self.stage[i]:
    #             for value in self.stage[i]:
    #                 print(TILES[value][1], end=' ')
    #         print()

    #     print(self.penalties)

    # def update_tableau(self, tile: int, quantity: int):
    #     while True:
    #         for i in range(5):
    #             print(f"[{i + 1}] - {self.stage[i]}")
    #         print(f"Select Stage Row to in which to place {quantity} {TILES[tile][1]} tiles:")
    #         row = int(input()) - 1
    #         if len(self.stage[row]) == 0:
    #             for _ in range(row + 1):
    #                 self.stage[row].append(tile)
    #                 quantity -= 1
    #                 if quantity == 0:
    #                     return 0
    #             to_lid = self.take_penalties(quantity)
    #             return to_lid
    #         elif tile in self.stage[row]:
    #             pass
            
    #         print("Row contains a different color. Try Again.")
    #         continue


# def select_from_factory(self):
#     while True:
#         # Get factory selection from player.
#         print(f"Select Factory <1 - {self.num_factories}>:")
#         choice = int(input())
#         factory = self.factories[choice - 1]

#         # Verify that factory is not empty.
#         if factory.is_empty():
#             print("Factory is empty. Please select another.")
#             continue

#         # Given selected factory, get tile choice from player.
#         # Move remainder from factory to pool.
#         tile, quantity = factory.select_tile()
#         for i in range(5):
#             if factory.tiles[i] != 0:
#                 self.pool.tiles[i] = factory.tiles[i]
#                 factory.tiles[i] = 0

#         return tile, quantity

# def select_from_pool(self):
#     # Selecting from pool, get tile choice from player.
#     return self.pool.select_tile()

# def actions(self):
#     print("[1] - Factory\n[2] - Pool")
#     choice = int(input())
#     if choice == 1:
#         tile, quantity = self.select_from_factory()
#     elif choice == 2:
#         tile, quantity = self.select_from_pool()
#     return tile, quantity
    
# def play(self):
#     # Initialize game components
#     playerboards = self.playerboards
#     factories = self.factories
#     drawbag = self.drawbag
#     lid = self.lid
#     pool = self.pool

#     # Add tiles to factories
#     for factory in factories:
#         factory.add_tiles(drawbag)

#     first_player_token = True
#     current_player = -1

#     # GAME LOOP
#     while True:
#         # Establish player turn.
#         current_player += 1
#         current_player %= 2

#         # Display factories
#         for number, factory in enumerate(factories):
#             print(f"\nFACTORY {number + 1}")
#             if factory.is_empty():
#                 print()
#             else:
#                 factory.print()
        
#         # Display pool
#         print("\nPOOL")
#         print(f'First Player Token: {first_player_token}')
#         pool.print()
        
#         # Display playerboard
#         print(f"\nPLAYER {current_player + 1} BOARD")
#         playerboards[current_player].print_tableau()
        
#         # Display Player Menu and take action.
#         tile, quantity = self.actions()
        
#         # Update playerboard
#         to_lid = playerboards[self.current_player].update_tableau(tile, quantity)
#         lid.tiles[tile] += to_lid
#         print("\nLID")
#         print(lid.tiles)
#         print()
#         playerboards[current_player].print_tableau()
        
#         print("\nPress Enter to Continue to Next Player's Turn")
#         do_nothing = input()