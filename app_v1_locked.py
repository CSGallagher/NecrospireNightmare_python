import pygame
import random

# Initialize Pygame
pygame.init()

# Dungeon settings
GRID_ROWS = 5
GRID_COLS = 5
TILE_TYPES = ["Empty", "Enemy", "Treasure", "Trap", "Portal", "Key", "Healing"]
TILE_SIZE = 100
SCREEN_WIDTH = GRID_COLS * TILE_SIZE
SCREEN_HEIGHT = GRID_ROWS * TILE_SIZE

# Player settings
player = {
    "name": "Rabel Blago",
    "health": 100,
    "mana": 50,
    "action_points": 3,
    "position": [0, 0],
    "keys_collected": 0,
    "souls_collected": 0,
    "moves_made": 0,  # Track player moves for enemy spawning
    "turns_taken": 0  # Track total turns to spawn new keys
}

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Necrospire Nightmare")

# Load images for tiles and resize them to fit the TILE_SIZE
tile_images = {
    "Empty": pygame.image.load("empty_tile.png"),
    "Enemy": pygame.image.load("enemy_tile.png"),
    "Treasure": pygame.image.load("treasure_tile.png"),
    "Trap": pygame.image.load("trap_tile.png"),
    "Portal": pygame.image.load("portal_tile.png"),
    "Key": pygame.image.load("key_tile.png"),
    "Healing": pygame.image.load("healing_tile.png"),
}

# Resize all tile images to match TILE_SIZE (100x100)
for key in tile_images:
    tile_images[key] = pygame.transform.scale(tile_images[key], (TILE_SIZE, TILE_SIZE))

def generate_dungeon(rows, cols):
    # Start with an empty dungeon
    dungeon = [["Empty" for _ in range(cols)] for _ in range(rows)]
    
    # Get all empty tile positions
    empty_positions = [(r, c) for r in range(rows) for c in range(cols)]
    
    # Shuffle the empty positions to randomly place tiles
    random.shuffle(empty_positions)
    
    # Create a list to store keys with their lifespan
    keys = []
    
    # Place 3 traps, 3 keys, and 3 portals
    for i in range(3):
        r, c = empty_positions.pop()
        if i == 0:
            dungeon[r][c] = "Trap"
        elif i == 1:
            dungeon[r][c] = "Key"
            keys.append({"position": (r, c), "lifespan": 0})  # Track position and lifespan
        else:
            dungeon[r][c] = "Portal"
    
    # Place 3 healing tiles
    for i in range(3):
        r, c = empty_positions.pop()
        dungeon[r][c] = "Healing"
    
    # Place 3 treasure tiles
    for i in range(3):
        r, c = empty_positions.pop()
        dungeon[r][c] = "Treasure"
    
    # Place 3 enemies in random tiles (not just empty)
    for _ in range(3):
        r, c = random.choice(empty_positions)
        dungeon[r][c] = "Enemy"
    
    return dungeon, keys  # Return dungeon and keys list


# Display the dungeon grid
def display_dungeon(dungeon, player_pos):
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            tile = dungeon[r][c]
            screen.blit(tile_images[tile], (c * TILE_SIZE, r * TILE_SIZE))

    # Draw player (no animation, just a placeholder)
    pygame.draw.circle(screen, (0, 255, 255), (player_pos[1] * TILE_SIZE + TILE_SIZE // 2, player_pos[0] * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 3)

# Roll a dice
def roll_dice(sides=6):
    return random.randint(1, sides)

# Handle player movement
def move_player(direction, dungeon, keys):
    r, c = player["position"]
    if direction == "up" and r > 0:
        player["position"] = [r - 1, c]
    elif direction == "down" and r < GRID_ROWS - 1:
        player["position"] = [r + 1, c]
    elif direction == "left" and c > 0:
        player["position"] = [r, c - 1]
    elif direction == "right" and c < GRID_COLS - 1:
        player["position"] = [r, c + 1]
    else:
        print("You can't move in that direction!")
        return

    # Consume an action point
    player["action_points"] -= 1
    if player["action_points"] < 0:
        print("No action points left! End your turn.")
        player["action_points"] = 0

    # Check tile interaction
    handle_tile(dungeon)

    # Track player moves and spawn enemies after every 3 moves
    player["moves_made"] += 1
    player["turns_taken"] += 1  # Increase turn count
    if player["moves_made"] % 3 == 0:
        spawn_enemy(dungeon)
    if player["turns_taken"] % 8 == 0:
        spawn_key(dungeon)
    
    # Update keys' lifespan
    for key in keys:
        key["lifespan"] += 1  # Increment the lifespan of each key
        if key["lifespan"] >= 5:
            # Remove the key if its lifespan has reached 5
            r, c = key["position"]
            dungeon[r][c] = "Empty"  # Set the tile to "Empty"
            keys.remove(key)  # Remove the key from the keys list


# Handle tile effects
def handle_tile(dungeon):
    r, c = player["position"]
    tile_type = dungeon[r][c]
    print(f"You stepped on a {tile_type} tile.")
    if tile_type == "Enemy":
        combat()
        dungeon[r][c] = "Empty"  # Remove enemy
    elif tile_type == "Treasure":
        print("You found a treasure! Gain 20 mana.")
        player["mana"] += 20
        dungeon[r][c] = "Empty"
    elif tile_type == "Trap":
        print("You triggered a trap! Lose 15 health.")
        player["health"] -= 15
    elif tile_type == "Portal":
        print("You activated a portal! Teleporting...")
        player["position"] = [random.randint(0, GRID_ROWS - 1), random.randint(0, GRID_COLS - 1)]
    elif tile_type == "Key":
        print("You collected a key!")
        player["keys_collected"] += 1
        dungeon[r][c] = "Empty"
    elif tile_type == "Healing":
        print("You found a healing tile! Restoring 20 health.")
        player["health"] += 20
        if player["health"] > 100:
            player["health"] = 100  # Maximum health is 100
    elif tile_type == "Empty":
        print("The tile is empty.")

# Combat mechanics
def combat():
    print("An enemy appears!")
    player_roll = roll_dice()
    enemy_roll = roll_dice()
    print(f"Player rolls {player_roll}, Enemy rolls {enemy_roll}")

    if player_roll > enemy_roll:
        print("You defeated the enemy!")
        player["souls_collected"] += 1
    else:
        print("The enemy hits you! Lose 20 health.")
        player["health"] -= 20

# Spawn an enemy on a random tile (including occupied ones)
def spawn_enemy(dungeon):
    all_tiles = [(r, c) for r in range(GRID_ROWS) for c in range(GRID_COLS)]
    random.shuffle(all_tiles)  # Shuffle to randomize spawn position
    for r, c in all_tiles:
        if dungeon[r][c] == "Empty":  # Only spawn on empty tiles
            dungeon[r][c] = "Enemy"
            break

# Spawn a new key on a random tile
def spawn_key(dungeon):
    empty_tiles = [(r, c) for r in range(GRID_ROWS) for c in range(GRID_COLS) if dungeon[r][c] == "Empty"]
    if empty_tiles:
        r, c = random.choice(empty_tiles)
        dungeon[r][c] = "Key"

# Win condition: Player wins when they have collected 3 keys and there are no enemies left
def check_win(dungeon):
    if player["keys_collected"] >= 3:
        for row in dungeon:
            if "Enemy" in row:
                return False
        print("Congratulations! You've collected all 3 keys and defeated all the enemies! You win!")
        
        # Load the "Pippi80s.jpg" image when the player wins
        win_image = pygame.image.load("Pippi80s.jpg")
        
        # Scale the image to fill the entire screen
        win_image = pygame.transform.scale(win_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Display the image
        screen.blit(win_image, (0, 0))
        pygame.display.update()  # Update the display to show the image
        
        # Wait for a moment before quitting or continuing
        pygame.time.wait(3000)  # Wait for 3 seconds
        
        return True
    return False


# End turn and reset action points
def end_turn():
    print("Ending your turn...")
    player["action_points"] = 3

# Main game loop
def main():
    dungeon, keys = generate_dungeon(GRID_ROWS, GRID_COLS)  # Now also returning keys
    print(f"Welcome to Necrospire Nightmare, {player['name']}!")
    
    # Pygame event loop
    running = True
    while running and player["health"] > 0:
        screen.fill((0, 0, 0))  # Clear the screen
        display_dungeon(dungeon, player["position"])

        # Show player stats
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"Health: {player['health']}, Mana: {player['mana']}", True, (255, 255, 255))
        screen.blit(health_text, (10, SCREEN_HEIGHT - 40))

        keys_collected_text = font.render(f"Keys: {player['keys_collected']}, Souls: {player['souls_collected']}", True, (255, 255, 255))
        screen.blit(keys_collected_text, (10, SCREEN_HEIGHT - 80))

        pygame.display.update()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_player("up", dungeon, keys)
                elif event.key == pygame.K_DOWN:
                    move_player("down", dungeon, keys)
                elif event.key == pygame.K_LEFT:
                    move_player("left", dungeon, keys)
                elif event.key == pygame.K_RIGHT:
                    move_player("right", dungeon, keys)
                elif event.key == pygame.K_r:
                    roll_dice()
                elif event.key == pygame.K_e:
                    end_turn()

        # Check win condition
        if check_win(dungeon):
            screen.fill((0, 0, 0))  # Clear the screen
            pygame.display.update()
            pygame.time.wait(3000)  # Wait for 3 seconds before quitting the game
            running = False

        # Check if player health reaches 0
        if player["health"] <= 0:
            print("You have perished in the Necrospire. Game Over!")
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()
