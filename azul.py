import random
from enum import Enum


def take_input(prompt: str, a: int, b: int):
    err_msg = "Input must be an integer between {} and {}".format(a, b)
    while True:
        print(f'{prompt}\n', "Choice: ", sep='', end='')
        choice = input()

        try:
            choice = int(choice)
        except ValueError:
            print(err_msg)
            continue

        if choice < a or choice > b:
            print(err_msg)
            continue

        return choice

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

    def get_tiles_of_color(self):
        '''
        Get tiles of only specified color. Useful as when player
        is selecting tiles from a factory or the pool on their turn.
        '''
        tile_set = []
        num_options = 0
        for row in self.tiles:
            if row:
                num_options += 1

        choice = take_input(prompt="Select Tiles", a=1, b = num_options)
        
        count = 0
        for row in self.tiles:
            count += 1 if row else 0
            if count == choice:
                tile_set.extend(row)
                row.clear()
                break
        
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
        Print a single given factory. Called from print
        method in FactorySet class.
        '''
        number = 1
        for row in self.tiles:
            if row:
                print(f"[{number}] - {row}")
                number += 1


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
        self.num_factories = num_factories
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

    def select(self, pool: TileMatrix):
        '''
        Select tile of one color from a single factory.
        Useful as when player is selecting tiles from a
        factory or the pool on their turn. 
        '''
        while True:
            # Get factory selection from player.
            choice = take_input(f"Select Factory", a=1, b=self.num_factories)
            factory = self.factories[choice - 1]

            # Verify that factory is not empty.
            if factory.is_empty():
                print("Factory is empty. Please select another.")
                continue

            # Given selected factory, get tile choice from player.
            # Move remainder from factory to pool.
            tile_set = factory.get_tiles_of_color()
            remainder = factory.get_all_tiles()
            
            for tile in remainder:
                pool.tiles[tile.index].append(tile)

            return tile_set

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
            if factory.tiles:
                print(f'FACTORY {factory_num}')
                number = 1
                for row in factory.tiles:
                    if not row:
                        continue
                    print(f"[{number}] - {row}")
                    number += 1
                print()
                factory_num += 1


class PlayerBoard:
    def __init__(self):
        self.points = 0
        self.first_player_token = False
        self.stage = TileMatrix()
        self.mosaic = [
            [None, None, None, None, None]
            for _ in range(5)
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

    def staging_error(self, row: int, tile_set: list[Tile]):
        if len(self.stage.tiles[row - 1]) == 0:
            return False
            
        if self.stage.tiles[row - 1][0].index == tile_set[0].index:
            return False
        
        print("That row already has tiles of a different color. Pick another row.")
        return True
    
    def stage_tiles(self, tile_set: list[Tile], lid: TileMatrix):
        for i in range(5):
            print(f"[{i + 1}] - {self.stage.tiles[i]}")
        
        while True:
            row = take_input(f"Select Stage Row to in which to place {len(tile_set)} {tile_set[0].name} tiles", 1, 5)
            if not self.staging_error(row, tile_set):
                break

        # Add tiles to staging and if list is too long,
        # transfer the extra tiles to penalties row.
        penalty_tiles = []
        self.stage.tiles[row - 1].extend(tile_set)
        if len(self.stage.tiles[row - 1]) > row:
            penalty_tiles = self.stage.tiles[row - 1][row:]
            for _ in penalty_tiles:
                self.stage.tiles[row - 1].pop()
        
            for i in range(7):
                if self.penalties[i][1] is None:
                    if penalty_tiles:
                        tile = penalty_tiles.pop()
                        self.penalties[i][1] = tile
                    else:
                        break
        
        # If penalty row is full, discard extra tiles in lid.
        if penalty_tiles:
            lid.tiles.extend(penalty_tiles)

    def take_turn(self, first_player_token: bool, factory_set: FactorySet, pool: TileMatrix, lid: TileMatrix):
        '''
        Select from factory_set or pool.
        '''
        choice = take_input("[1] - Factories\n[2] - Pool", 1, 2)

        if choice == 1:
            tile_set = factory_set.select(pool)
        else:
            if first_player_token:
                self.first_player_token = True
                first_player_token = False
            tile_set = pool.get_tiles_of_color()
        
        self.stage_tiles(tile_set, lid)

        return first_player_token

    def index(self, number: int, tile_index: int):
        '''
        Calculate mosaic index for tile using row number.
        Used in the tessellate method.
        '''
        index = tile_index + number
        index %= 5
        return index

    def score(self, row_num: int, index: int):
        '''
        Calculate score for adjacent tiles after placing new tile.
        If complete row is found, return 2.
        Used in the tessellate method.
        '''
        game_end = -1
        self.points += 1

        # Check left
        ptr = index - 1
        while ptr >= 0:
            if self.mosaic[row_num][ptr] is not None:
                self.points +=1
            else:
                break
            ptr -= 1
        
        # Check if left side is full for game end condition.
        game_end -= 1 if ptr < 0 else 0

        # Check right
        ptr = index + 1
        while ptr <= 4:
            if self.mosaic[row_num][ptr] is not None:
                self.points += 1
            else:
                break
            ptr += 1

        # Check if right side is full for game end condition.
        game_end -= 1 if ptr > 4 else 0
        
        # Check up
        ptr = row_num - 1
        while ptr >= 0:
            if self.mosaic[ptr][index] is not None:
                self.points += 1
            else:
                break
            ptr -= 1

        # Check down
        ptr = row_num + 1
        while ptr <= 4:
            if self.mosaic[ptr][index] is not None:
                self.points += 1
            else:
                break
            ptr += 1

        return game_end

    def tessellate(self, lid: TileMatrix):
        '''
        For any full stage row, place one of its tiles in the mosaic
        and the remainder, if there are any, in the lid.

        Calculate points and update player score.
        '''
        game_end = 0
        for row_num, row in enumerate(self.stage.tiles):
            if row_num + 1 == len(row):
                tile = row.pop()
                index = self.index(row_num, tile.index)
                self.mosaic[row_num][index] = tile
                game_end = self.score(row_num, index)
                while row:
                    tile = row.pop()
                    lid.tiles[tile.index].append(tile)
        return game_end

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
                row.append(None)
                lid.tiles[tile.index].append(tile)

        self.points += penalty
        if self.points < 0:
            self.points = 0

    def print(self):
        '''
        Print out the whole playerboard spread.
        '''
        for i in range(5):
            print(self.mosaic[i], end=' | ')
            print(self.stage.tiles[i])
        
        print()
        print(self.penalties)


class PlayerBoardSet:
    def __init__(self, num_players=2):
        self.player_boards = [
            PlayerBoard() for _ in range(num_players)
        ]
    
    def resolve(self, lid: TileMatrix) -> int:
        '''
        Iterate through playerboards:
            Move tiles from stage to mosaic and calculate score,
            checking for game end condition.

            Calculate penalty for player and discard penalty tiles to lid.

            Determine first player.

            If game end condition is triggered, return game end.
            Else return current_player
        '''
        current_player = 0
        for player_num, board in enumerate(self.player_boards):
            game_end = board.tessellate(lid)
            board.take_penalties(lid)
            if board.first_player_token:
                board.first_player_token = False
                current_player = player_num
        
        if game_end == -3:
            return game_end
        return current_player
