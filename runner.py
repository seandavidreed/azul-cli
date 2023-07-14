import azul

# Initialize game components.
drawbag = azul.DrawBag(num_tiles=20)
factory_set = azul.FactorySet(num_factories=5)
lid = azul.TileMatrix()
pool = azul.TileMatrix()


# # GAME LOOP
# while True:

#     ''' 1. Resolve playerboards (move tiles from stage to mosaic and remainder to lid, tally scores). '''

#     ''' 2. Check each playerboard for win conditions. Initiate end of game sequence if true. '''

#     ''' 3. Restock factories '''

#     ''' 4. Determine starting player '''

# TESTING
drawbag.print()
print()
lid.print()

factory_set.print()

factory_set.add_tiles(drawbag, lid)

factory_set.print()

print()

drawbag.print()
print()
lid.print()
