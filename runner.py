import azul

# Initialize game components.
drawbag = azul.DrawBag(num_tiles=20)
factory_set = azul.FactorySet(num_factories=5)
playerboard_set = azul.PlayerBoardSet(num_players=2)
lid = azul.TileMatrix()
pool = azul.TileMatrix()
current_player = 0


# GAME LOOP
while True:
    ''' 
    Resolve playerboards (move tiles from stage to mosaic and remainder to lid, tally scores).
    Restock factories.
    '''
    current_player = playerboard_set.resolve(lid)
    if current_player < 0:
        # GAME ENDS
        pass

    factory_set.add_tiles(drawbag, lid)

    '''
    Display tableau.
    '''
    print("FACTORIES")
    factory_set.print()

    print("POOL")
    pool.print()

    print(f"PLAYER {current_player + 1} BOARD")
    playerboard_set.player_boards[current_player].print()

    '''
    Make choices.
    '''
    tile_set = playerboard_set.player_boards[current_player].take_turn(factory_set, pool)

    factory_set.print()
    pool.print()
    print(tile_set)
    playerboard_set.player_boards[current_player].print()

    temp = input("HALT")

    




#     # GAME LOOP
#     while True:
        
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
