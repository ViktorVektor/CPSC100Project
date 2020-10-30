#
# x,y array for the position of the player
player_position = [0, 0]
player_width =



def keypress_move(event):
    # if key down
    playerDX = 0
    playerDY = 0

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_d:
            playerDX = playerSpeed
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            playerDX = -playerSpeed
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
            playerDY = -playerSpeed
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_s:
            playerDY = playerSpeed
    # if key up
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_d:
            playerDX = 0
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_a:
            playerDX = 0
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_w:
            playerDY = 0
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_s:
            playerDY = 0

    player_position[0] += playerDX
    player_position[1] += playerDY