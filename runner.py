import azul
import os

# Initialize game components.
num_players = 2
num_factories = (num_players * 2) + 1
drawbag = azul.DrawBag(num_tiles=20)
factory_set = azul.FactorySet(num_factories=num_factories)
playerboard_set = azul.PlayerBoardSet(num_players=num_players)
lid = azul.TileMatrix()
pool = azul.TileMatrix()
current_player = 0
first_player_token = True
round = 0


# GAME LOOP
while True:
    os.system('clear')
    if factory_set.is_empty() and pool.is_empty():
        '''
        Wrap up current round and prepare for next.
        Resolve playerboard for each player:
            Move staged tiles to mosaic,
            Calculate score.
            Take penalties.
        Restock factories.
        '''
        round += 1
        current_player = playerboard_set.resolve(lid)
        if current_player < 0:
            player, score = playerboard_set.find_winner()
            print(f"Congrats Player {player}, you won with {score} points!")
            exit()

        factory_set.add_tiles(drawbag, lid)
        first_player_token = True
    else:
        current_player = (current_player + 1) % num_players

    '''
    Display tableau.
    '''
    print(f'ROUND {round}')
    print()

    print("FACTORIES")
    print()
    factory_set.print()

    print("POOL")
    if first_player_token:
        print("First Player Token")
    pool.print()
    print()

    print(f"PLAYER {current_player + 1} BOARD")
    playerboard_set.player_boards[current_player].print()

    '''
    Make choices.
    '''
    first_player_token = playerboard_set.player_boards[current_player].take_turn(first_player_token, factory_set, pool, lid)

    playerboard_set.player_boards[current_player].print()

    input("\nPress enter to continue")
