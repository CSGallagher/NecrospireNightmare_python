import pygame
import random

# Initialize Pygame
pygame.init()

CHALLENGE = "medium"
print(f'settings on {CHALLENGE}')
# Dungeon settings

DIFFICULTY_SETTINGS = {
    "easy": {
        "GRID_ROWS": 5,
        "GRID_COLS": 5,
        "KEY_START": 3,
        "TRAP_START": 3,
        "PORTAL_START": 2,
        "HEALING_START": 3,
        "MANA_START": 2,
        "ENEMY_START": 3,
        "MANA_KILL": 80,
        "TRAP_DAMAGE": 10,
        "MAX_HEALTH": 100,
        "TURN_COUNT_ENEMY": 4,
        "TURN_COUNT_KEY_SPAWN": 6,
        "TURN_COUNT_MANA_SPAWN": 4,
        "TURN_COUNT_KEY_DEATH": 4,
        "TURN_COUNT_MANA_DEATH": 4,
        "WIN_CONDITION_KEY": 3,
    },
    "medium": {
        "GRID_ROWS": 8,
        "GRID_COLS": 8,
        "KEY_START": 5,
        "TRAP_START": 5,
        "PORTAL_START": 4,
        "HEALING_START": 5,
        "MANA_START": 3,
        "ENEMY_START": 5,
        "MANA_KILL": 100,
        "TRAP_DAMAGE": 20,
        "MAX_HEALTH": 100,
        "TURN_COUNT_ENEMY": 3,
        "TURN_COUNT_KEY_SPAWN": 8,
        "TURN_COUNT_MANA_SPAWN": 6,
        "TURN_COUNT_KEY_DEATH": 5,
        "TURN_COUNT_MANA_DEATH": 5,
        "WIN_CONDITION_KEY": 3,
    },
    "hard": {
        "GRID_ROWS": 10,
        "GRID_COLS": 10,
        "KEY_START": 8,
        "TRAP_START": 8,
        "PORTAL_START": 6,
        "HEALING_START": 6,
        "MANA_START": 4,
        "ENEMY_START": 8,
        "MANA_KILL": 120,
        "TRAP_DAMAGE": 30,
        "MAX_HEALTH": 100,
        "TURN_COUNT_ENEMY": 2,
        "TURN_COUNT_KEY_SPAWN": 10,
        "TURN_COUNT_MANA_SPAWN": 8,
        "TURN_COUNT_KEY_DEATH": 6,
        "TURN_COUNT_MANA_DEATH": 6,
        "WIN_CONDITION_KEY": 5,
    }
}

# Function for user input to select difficulty
def get_difficulty():
    global CHALLENGE
    print("Select difficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    choice = input("Enter the number of your choice: ")

    if choice == "1":
        CHALLENGE = "easy"
    elif choice == "2":
        CHALLENGE = "medium"
    elif choice == "3":
        CHALLENGE = "hard"
    else:
        print("Invalid choice, defaulting to 'medium'.")
        CHALLENGE = "medium"

    print(f"Settings: {CHALLENGE}")

# Select difficulty before game starts
get_difficulty()

settings = DIFFICULTY_SETTINGS[CHALLENGE]
GRID_ROWS = settings["GRID_ROWS"]
GRID_COLS = settings["GRID_COLS"]
KEY_START = settings["KEY_START"]
TRAP_START = settings["TRAP_START"]
PORTAL_START = settings["PORTAL_START"]
HEALING_START = settings["HEALING_START"]
MANA_START = settings["MANA_START"]
ENEMY_START = settings["ENEMY_START"]
MANA_KILL = settings["MANA_KILL"]
TRAP_DAMAGE = settings["TRAP_DAMAGE"]
MAX_HEALTH = settings["MAX_HEALTH"]
TURN_COUNT_ENEMY = settings["TURN_COUNT_ENEMY"]
TURN_COUNT_KEY_SPAWN = settings["TURN_COUNT_KEY_SPAWN"]
TURN_COUNT_MANA_SPAWN = settings["TURN_COUNT_MANA_SPAWN"]
TURN_COUNT_KEY_DEATH = settings["TURN_COUNT_KEY_DEATH"]
TURN_COUNT_MANA_DEATH = settings["TURN_COUNT_MANA_DEATH"]
WIN_CONDITION_KEY = settings["WIN_CONDITION_KEY"]

TILE_TYPES = ["Empty", "Enemy", "Mana", "Trap", "Portal", "Key", "Healing"]
TILE_SIZE = 100
SCREEN_WIDTH = GRID_ROWS*TILE_SIZE
SCREEN_HEIGHT = GRID_COLS*TILE_SIZE
# Player settings
player = {
    "name": "Rabel Blago",
    "health": MAX_HEALTH,
    "mana": 0,  # Start with 0 mana
    "action_points": 3,
    "position": [0, 0],
    "keys_collected": 0,
    "souls_collected": 0,
    "moves_made": 0,  # Track player moves for mana spawning
    "turns_taken": 0,  # Track total turns to spawn new keys
}

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Necrospire Nightmare")

# Load images for tiles and resize them to fit the TILE_SIZE
tile_images = {
    "Empty": pygame.image.load("empty_tile.png"),
    "Enemy": pygame.image.load("enemy_tile.png"),
    "Mana": pygame.image.load("mana_tile.png"),  # Mana tile image
    "Trap": pygame.image.load("trap_tile.png"),
    "Portal": pygame.image.load("portal_tile.png"),
    "Key": pygame.image.load("key_tile.png"),
    "Healing": pygame.image.load("healing_tile.png"),
}

# Load player image (replace with your player image file)
player_image = pygame.image.load("RabelBlago.png")  # Make sure to use the correct image file path

# Resize the player image to fit the tile size (optional, but recommended)
player_image = pygame.transform.scale(player_image, (TILE_SIZE, TILE_SIZE))

# Resize all tile images to match TILE_SIZE (100x100)
for key in tile_images:
    tile_images[key] = pygame.transform.scale(tile_images[key], (TILE_SIZE, TILE_SIZE))

# Dungeon generation
def generate_dungeon(rows, cols):
    # Start with an empty dungeon
    dungeon = [["Empty" for _ in range(cols)] for _ in range(rows)]
    
    # Get all empty tile positions
    empty_positions = [(r, c) for r in range(rows) for c in range(cols)]
    
    # Shuffle the empty positions to randomly place tiles
    random.shuffle(empty_positions)
    
    # Create a list to store all keys and mana tiles with their lifespan
    all_keys = []
    all_mana = []
    
    # Place initial key
    for i in range(KEY_START):
        r, c = empty_positions.pop()
        dungeon[r][c] = "Key"
        all_keys.append({"position": (r, c), "lifespan": 0})  # Track position and lifespan
        print(f"Initial Key placed at {r}, {c} with lifespan {0}")  # Debugging output
    
    # Place initial mana tiles
    for i in range(MANA_START):
        r, c = empty_positions.pop()
        dungeon[r][c] = "Mana"
        all_mana.append({"position": (r, c), "lifespan": 0})  # Track position and lifespan
        print(f"Initial Mana placed at {r}, {c} with lifespan {0}")  # Debugging output
    
    # Place intial traps
    for i in range(TRAP_START):
        r, c = empty_positions.pop()
        dungeon[r][c] = "Trap"
    
    # Place initial portals
    for i in range(PORTAL_START):
        r, c = empty_positions.pop()
        dungeon[r][c] = "Portal"
    
    # Place intial  healing tiles
    for i in range(HEALING_START):
        r, c = empty_positions.pop()
        dungeon[r][c] = "Healing"
    
    # Place initial enemies in random tiles (not just empty)
    for _ in range(ENEMY_START):
        r, c = random.choice(empty_positions)
        dungeon[r][c] = "Enemy"
    
    return dungeon, all_keys, all_mana  # Return dungeon, all keys and mana tiles

# Display the dungeon grid and player
def display_dungeon(dungeon, player_pos):
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            tile = dungeon[r][c]
            screen.blit(tile_images[tile], (c * TILE_SIZE, r * TILE_SIZE))

    # Draw the player image at the player's position
    player_rect = player_image.get_rect()  # Get the rect of the player image
    player_rect.topleft = (player_pos[1] * TILE_SIZE, player_pos[0] * TILE_SIZE)  # Set position based on player coordinates
    screen.blit(player_image, player_rect)  # Draw the player image on the screen

# Handle tile effects
def handle_tile(dungeon, all_mana, all_keys):
    r, c = player["position"]
    tile_type = dungeon[r][c]
    print(f"You stepped on a {tile_type} tile.")
    
    if tile_type == "Enemy":
        combat()
        dungeon[r][c] = "Empty"  # Remove enemy
    elif tile_type == "Mana":
        manaGain = random.randint(20, 60)  # Example range for mana gain, can be adjusted as needed
        print(f"You found a mana tile! Gaining {manaGain} mana.")
        player["mana"] += manaGain
        dungeon[r][c] = "Empty"  # Remove mana tile
        
        # If mana reaches 100, kill all but one enemy
        if player["mana"] >= MANA_KILL:
            player["mana"] -= MANA_KILL
            kill_enemies(dungeon)
    elif tile_type == "Trap":
        print(f"You triggered a trap! Lose {TRAP_DAMAGE} health.")
        player["health"] -= TRAP_DAMAGE
    elif tile_type == "Portal":
        print("You activated a portal! Teleporting...")
        player["position"] = [random.randint(0, GRID_ROWS - 1), random.randint(0, GRID_COLS - 1)]
    elif tile_type == "Key":
        print("You collected a key!")
        player["keys_collected"] += 1
        dungeon[r][c] = "Empty"
    elif tile_type == "Healing":
        # Generate a random healing amount between 5 and 35 in increments of 5
        healing_amount = random.choice([5, 10, 15, 20, 25, 30, 35])
        print(f"You found a healing tile! Restoring {healing_amount} health.")
        player["health"] += healing_amount
        
        # Ensure the player's health does not exceed the maximum of 100
        if player["health"] > MAX_HEALTH:
            player["health"] = MAX_HEALTH
    elif tile_type == "Empty":
        print("The tile is empty.")

# Combat mechanics
def combat():
    print("An enemy appears!")
    player_roll = roll_dice()
    enemy_roll = roll_dice()
    print(f"Player rolls {player_roll}, Enemy rolls {enemy_roll}")
    enemy_damage = random.choice([5, 10, 15, 20, 25, 30, 35])  # Ensure this is an integer
    if player_roll > enemy_roll:
        print("You defeated the enemy!")
        player["souls_collected"] += 1
    else:
        print(f"The enemy hits you! Lose {enemy_damage} health.")
        player["health"] -= enemy_damage  # Fix this by removing the curly braces

# Kill all but one enemy
def kill_enemies(dungeon):
    enemy_positions = []
    
    # Collect all enemy positions
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            if dungeon[r][c] == "Enemy":
                enemy_positions.append((r, c))
    
    # Kill all but one enemy
    while len(enemy_positions) > 1:
        r, c = enemy_positions.pop()
        dungeon[r][c] = "Empty"

# Roll a dice
def roll_dice(sides=6):
    return random.randint(1, sides)

# Handle player movement and tile interaction
def move_player(direction, dungeon, all_keys, all_mana):
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
    handle_tile(dungeon, all_mana, all_keys)

    # Track player moves and spawn enemies after every 3 moves
    player["moves_made"] += 1
    player["turns_taken"] += 1  # Increase turn count
    if player["moves_made"] % TURN_COUNT_ENEMY == 0:
        spawn_enemy(dungeon)
    if player["turns_taken"] % TURN_COUNT_KEY_SPAWN == 0:
        spawn_key(dungeon, all_keys)
    if player["turns_taken"] % TURN_COUNT_MANA_SPAWN == 0:
        spawn_mana(dungeon, all_mana)
    
    # Update keys' and mana tiles' lifespan
    update_lifespan(dungeon, all_keys, all_mana)

# Update lifespan function to handle keys and mana properly
def update_lifespan(dungeon, all_keys, all_mana):
    # Update keys' lifespan
    for key in all_keys[:]:  # Iterate over a copy of the list
        key["lifespan"] += 1  # Increment the lifespan of each key
        print(f"Key at {key['position']} has lifespan {key['lifespan']}")  # Debugging output
        if key["lifespan"] >= TURN_COUNT_KEY_DEATH:
            # Remove the key if its lifespan has reached 5
            r, c = key["position"]
            dungeon[r][c] = "Empty"  # Set the tile to "Empty"
            all_keys.remove(key)  # Remove the key from the keys list
            print(f"Key at {key['position']} removed")  # Debugging output

    # Update mana's lifespan
    for mana in all_mana[:]:  # Iterate over a copy of the list
        mana["lifespan"] += 1
        print(f"Mana at {mana['position']} has lifespan {mana['lifespan']}")  # Debugging output
        if mana["lifespan"] >= TURN_COUNT_MANA_DEATH:
            # Remove mana if lifespan has reached 5
            r, c = mana["position"]
            dungeon[r][c] = "Empty"  # Set the tile to "Empty"
            all_mana.remove(mana)  # Remove the mana tile from the list
            print(f"Mana at {mana['position']} removed")  # Debugging output

# Spawn new mana tiles 
def spawn_mana(dungeon, all_mana):
    empty_tiles = [(r, c) for r in range(GRID_ROWS) for c in range(GRID_COLS) if dungeon[r][c] == "Empty"]
    if empty_tiles:
        r, c = random.choice(empty_tiles)
        dungeon[r][c] = "Mana"
        all_mana.append({"position": (r, c), "lifespan": 0})  # Explicitly set lifespan to 0 for new mana tiles
        print(f"New Mana spawned at {r}, {c} with lifespan 0")  # Debugging output

# Spawn an enemy on a random tile (including occupied ones)
def spawn_enemy(dungeon):
    all_tiles = [(r, c) for r in range(GRID_ROWS) for c in range(GRID_COLS)]
    random.shuffle(all_tiles)  # Shuffle to randomize spawn position
    for r, c in all_tiles:
        if dungeon[r][c] == "Empty":  # Only spawn on empty tiles
            dungeon[r][c] = "Enemy"
            break

# Spawn a new key on a random tile
def spawn_key(dungeon, all_keys):
    empty_tiles = [(r, c) for r in range(GRID_ROWS) for c in range(GRID_COLS) if dungeon[r][c] == "Empty"]
    if empty_tiles:
        r, c = random.choice(empty_tiles)
        dungeon[r][c] = "Key"
        all_keys.append({"position": (r, c), "lifespan": 0})  # Explicitly set lifespan to 0 for new keys
        print(f"New Key spawned at {r}, {c} with lifespan 0")  # Debugging output

# Win condition: Player wins when they have collected 3 keys and there are no enemies left
def check_win(dungeon):
    if player["keys_collected"] >= WIN_CONDITION_KEY:
        for row in dungeon:
            if "Enemy" in row:
                return False
        print(f"Congratulations! You've collected all {WIN_CONDITION_KEY} keys and defeated all the enemies! You win!")
        
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
def main(settings):
    global GRID_ROWS, GRID_COLS, KEY_START, TRAP_START, PORTAL_START, HEALING_START, MANA_START, ENEMY_START, MANA_KILL, TRAP_DAMAGE, MAX_HEALTH, TURN_COUNT_ENEMY, TURN_COUNT_KEY_SPAWN, TURN_COUNT_MANA_SPAWN, TURN_COUNT_KEY_DEATH, TURN_COUNT_MANA_DEATH, WIN_CONDITION_KEY
    # Set the game variables based on the selected settings
    GRID_ROWS = settings["GRID_ROWS"]
    GRID_COLS = settings["GRID_COLS"]
    KEY_START = settings["KEY_START"]
    TRAP_START = settings["TRAP_START"]
    PORTAL_START = settings["PORTAL_START"]
    HEALING_START = settings["HEALING_START"]
    MANA_START = settings["MANA_START"]
    ENEMY_START = settings["ENEMY_START"]
    MANA_KILL = settings["MANA_KILL"]
    TRAP_DAMAGE = settings["TRAP_DAMAGE"]
    MAX_HEALTH = settings["MAX_HEALTH"]
    TURN_COUNT_ENEMY = settings["TURN_COUNT_ENEMY"]
    TURN_COUNT_KEY_SPAWN = settings["TURN_COUNT_KEY_SPAWN"]
    TURN_COUNT_MANA_SPAWN = settings["TURN_COUNT_MANA_SPAWN"]
    TURN_COUNT_KEY_DEATH = settings["TURN_COUNT_KEY_DEATH"]
    TURN_COUNT_MANA_DEATH = settings["TURN_COUNT_MANA_DEATH"]
    WIN_CONDITION_KEY = settings["WIN_CONDITION_KEY"]

    dungeon, all_keys, all_mana = generate_dungeon(GRID_ROWS, GRID_COLS)  # Now also returning all keys and mana_tiles
    print(f"Welcome to Necrospire Nightmare, {player['name']}!")
    print("Starting the game with the following settings:")
    print(settings)
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
                    move_player("up", dungeon, all_keys, all_mana)
                elif event.key == pygame.K_DOWN:
                    move_player("down", dungeon, all_keys, all_mana)
                elif event.key == pygame.K_LEFT:
                    move_player("left", dungeon, all_keys, all_mana)
                elif event.key == pygame.K_RIGHT:
                    move_player("right", dungeon, all_keys, all_mana)
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
    main(settings)
