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
    Restock factories
    '''
    current_player = playerboard_set.resolve(lid)
    if current_player < 0:
        # GAME ENDS
        pass

    factory_set.add_tiles(drawbag, lid)

    '''
    Commence turn taking.
    '''

    print("FACTORIES")
    factory_set.print()

    print("POOL")
    pool.print()

    print(f"PLAYER {current_player + 1} BOARD")
    playerboard_set.player_boards[current_player].print()

    temp = input("HALT")




    # # TESTING
    # drawbag.print()
    # print()
    # lid.print()

    # factory_set.print()

    # factory_set.add_tiles(drawbag, lid)

    # factory_set.print()

    # print()

    # drawbag.print()
    # print()
    # lid.print()
