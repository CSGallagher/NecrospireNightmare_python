import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Default difficulty
CHALLENGE = "medium"
print(f"Settings on {CHALLENGE}")

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
        "POISON_LENGTH": 20
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
        "WIN_CONDITION_KEY": 10,
        "POISON_LENGTH": 50
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
        "WIN_CONDITION_KEY": 50,
        "POISON_LENGTH": 100
    }
}

# Pygame setup
TILE_SIZE = 100
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Necrospire Nightmare")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
LIGHT_GREEN = (144, 238, 144)  # Soft Light Green for "Easy" button
CORAL = (255, 127, 80)         # Warm Coral for "Medium" button
MUTED_AMBER = (255, 191, 73)   # Muted Amber for "Hard" button
MUTED_BLUE = (163, 200, 228)   # Muted Light Blue for instruction box
BLACK = (0, 0, 0)              # Black for borders and text

# Font
font = pygame.font.Font(None, 48)

# Tile names and explanations
TILE_EXPLANATIONS = {
    "Empty": "A plain, empty tile.",
    "Enemy": "A fierce enemy is lurking here.",
    "Mana": "A tile filled with mystical mana energy.",
    "Trap": "Be careful! This tile holds a dangerous trap.",
    "Portal": "A portal that leads to another dimension.",
    "Key": "A valuable key that helps unlock new paths.",
    "Healing": "A healing tile to restore health.",
    "Poison": "A poisonous tile that inflicts damage with each move.",
    "Elixir": "A healing elixir that removes poison."
}
# Load images for tiles and resize them to fit the TILE_SIZE
tile_images = {
    "Empty": pygame.image.load("empty_tile4.png"),
    "Enemy": pygame.image.load("enemy_tile4.png"),
    "Mana": pygame.image.load("mana_tile3.jpg"),  # Mana tile image
    "Trap": pygame.image.load("trap_tile8.jpg"),
    "Portal": pygame.image.load("portal_tile2.png"),
    "Key": pygame.image.load("key_tile3.png"),
    "Healing": pygame.image.load("healing_tile3.png"),
    "Poison": pygame.image.load("poison_tile.jpg"),  # Add your poison tile image here
    "Elixir": pygame.image.load("elixir_tile.jpg"),  # Add your elixir tile image here
    "Boss": pygame.image.load("player_sprite.png")
}
# Load the background image
background_image = pygame.image.load("PippiNecromancer.jpg")  # Replace with your image file path
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale to fit the screen
explanation_background = pygame.image.load("explanationBackground9.png")
explanation_background = pygame.transform.scale(explanation_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
# Function to display tile explanations
def display_tile_explanation_screen():
    running = True
    screen.blit(explanation_background, (0, 0))  # Draw the background image first
    while running:

        # Set up font for title and descriptions
        title_font = pygame.font.Font(None, 72)
        description_font = pygame.font.Font(None, 28)

        # Title text
        title_text = title_font.render("Tile Explanations", False, BLACK)
        
        screen.blit(title_text, ((SCREEN_WIDTH - title_text.get_width()) // 2, 20))  # Center the title at the top

        # Set initial vertical offset for the elements below the title
        y_offset = 100  # Start drawing from below the title

        # Iterate through tile explanations
        for tile, explanation in TILE_EXPLANATIONS.items():
            # Load the tile image (Ensure the tile image is scaled to fit the layout)
            tile_image = tile_images[tile]
            tile_image = pygame.transform.scale(tile_image, (50, 50))  # Scale the image

            # Calculate the horizontal alignment for the tile image, tile name, and explanation
            tile_image_x = (SCREEN_WIDTH - tile_image.get_width() - 400) // 2  # Align left of text and centered
            tile_name_x = tile_image_x + tile_image.get_width() + 10  # 10px padding between image and name

            # Calculate the vertical position of the title to be vertically centered with the tile image
            tile_name_y = y_offset + (tile_image.get_height() - description_font.get_height()) // 2

            # Draw the tile image
            screen.blit(tile_image, (tile_image_x, y_offset))

            # Render the tile name and explanation
            tile_name_text = description_font.render(f"{tile}: {explanation}", False, BLACK)

            # Draw tile name
            screen.blit(tile_name_text, (tile_name_x, tile_name_y))

            # Update the offset for the next tile explanation
            y_offset += max(tile_image.get_height(), tile_name_text.get_height()) + 10  # Add some spacing between items

        # Draw a back button at the bottom, moved down by 50 pixels
        back_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100 + 25, 200, 50)
        pygame.draw.rect(screen, LIGHT_GREEN, back_button)
        pygame.draw.rect(screen, BLACK, back_button, 3)  # Black border for the back button

        # Create a font for the back button text
        back_button_font = pygame.font.Font(None, 20)  # Adjust font size for back button
        back_text = back_button_font.render(f"Commence Nightmare", False, BLACK)
        screen.blit(back_text, (back_button.x + (back_button.width - back_text.get_width()) // 2,
                                back_button.y + (back_button.height - back_text.get_height()) // 2))
        pygame.display.update()  # Update the display

        # Event handling for back button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    running = False  # Exit the tile explanation screen and return to the start screen

# Function to display difficulty options
def display_difficulty_screen():
    global CHALLENGE
    running = True
    while running:
        screen.blit(background_image, (0, 0))  # Draw the background image first

        # Define a smaller box for instructions on the right side of the screen
        box_width = 150  # Adjust width of the instruction box
        box_height = 75  # Adjust height of the instruction box
        box_x = SCREEN_WIDTH - box_width - 20  # Position it 20px away from the right side of the screen
        box_y = (SCREEN_HEIGHT - box_height) // 2  # Center it vertically

        # Set up the font for the instruction text (smaller text size)
        instruction_font = pygame.font.Font(None, 18)  # Smaller font size for instructions
        instruction_text = f"You must collect all keys and clear all enemies to escape the nightmare."

        # Function to wrap text into multiple lines
        def wrap_text(text, font, max_width):
            words = text.split(" ")
            lines = []
            current_line = ""

            for word in words:
                # Check if adding the word to the current line would exceed the width
                if font.size(current_line + word)[0] <= max_width:
                    current_line += word + " "
                else:
                    if current_line:
                        lines.append(current_line.strip())
                    current_line = word + " "

            # Add the last line
            if current_line:
                lines.append(current_line.strip())

            return lines

        # Wrap the text to fit within the box width
        wrapped_text = wrap_text(instruction_text, instruction_font, box_width - 20)  # 20px padding on each side

        # Calculate total height of wrapped text
        total_text_height = sum(instruction_font.get_height() + 5 for _ in wrapped_text) - 5  # Add spacing between lines

        # Create a white box on the right side
        pygame.draw.rect(screen, MUTED_BLUE, pygame.Rect(box_x, box_y, box_width, box_height))  # White box
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(box_x, box_y, box_width, box_height), 2)  # Black border

        # Now we want to center the wrapped text inside the box
        y_offset = box_y + (box_height - total_text_height) // 2  # Center the text vertically

        # Render and draw the wrapped text inside the box
        for line in wrapped_text:
            instruction_render = instruction_font.render(line, True, (0, 0, 0))  # Black text

            # Center the text horizontally within the box
            x_offset = box_x + (box_width - instruction_render.get_width()) // 2

            # Draw the line of text
            screen.blit(instruction_render, (x_offset, y_offset))

            # Move to the next line
            y_offset += instruction_font.get_height() + 5  # Add spacing between lines

        # Adjust the vertical position to be closer to the bottom
        button_height = 50  # Height of each button
        spacing = 20  # Space between buttons
        title_font = pygame.font.Font(None, 72)  # Font for the title (larger font size)
        button_font = pygame.font.Font(None, 30)  # Font for the buttons

        # Horizontal centering for the buttons
        button_width = 200  # Width of each button
        center_x = (SCREEN_WIDTH - button_width) // 2  # Calculate the x position to center the button

        # Position buttons closer to the bottom
        easy_button = pygame.Rect(center_x, SCREEN_HEIGHT - button_height - spacing * 2, button_width, button_height)
        medium_button = pygame.Rect(center_x, SCREEN_HEIGHT - button_height * 2 - spacing * 3, button_width, button_height)
        hard_button = pygame.Rect(center_x, SCREEN_HEIGHT - button_height * 3 - spacing * 4, button_width, button_height)

        # Draw buttons on the screen
        pygame.draw.rect(screen, LIGHT_GREEN, easy_button)
        pygame.draw.rect(screen, CORAL, medium_button)
        pygame.draw.rect(screen, MUTED_AMBER, hard_button)

        # Draw black borders around the buttons (same rectangle, but with thickness)
        border_thickness = 3  # You can adjust this thickness
        pygame.draw.rect(screen, (0, 0, 0), easy_button, border_thickness)  # Black border around the "Easy" button
        pygame.draw.rect(screen, (0, 0, 0), medium_button, border_thickness)  # Black border around the "Medium" button
        pygame.draw.rect(screen, (0, 0, 0), hard_button, border_thickness)  # Black border around the "Hard" button

        # Render text on buttons (Centered on each button)
        easy_text = button_font.render("Easy (3 keys)", True, (0, 0, 0))
        medium_text = button_font.render("Medium (10 keys)", True, (0, 0, 0))
        hard_text = button_font.render("Hard (50 keys)", True, (0, 0, 0))

        # Center the text on each button
        screen.blit(easy_text, (easy_button.x + (easy_button.width - easy_text.get_width()) // 2, easy_button.y + (easy_button.height - easy_text.get_height()) // 2))
        screen.blit(medium_text, (medium_button.x + (medium_button.width - medium_text.get_width()) // 2, medium_button.y + (medium_button.height - medium_text.get_height()) // 2))
        screen.blit(hard_text, (hard_button.x + (hard_button.width - hard_text.get_width()) // 2, hard_button.y + (hard_button.height - hard_text.get_height()) // 2))

        # Title text
        title_text = title_font.render("Necrospire Nightmare", True, (97, 33, 33))  # Dark Red text for the title
        screen.blit(title_text, ((SCREEN_WIDTH - title_text.get_width()) // 2, 20))  # Position the title at y=20

        pygame.display.update()

        # Event handling for buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(event.pos):
                    CHALLENGE = "easy"
                    display_tile_explanation_screen()  # Go to the tile explanation screen
                    running = False
                elif medium_button.collidepoint(event.pos):
                    CHALLENGE = "medium"
                    display_tile_explanation_screen()  # Go to the tile explanation screen
                    running = False
                elif hard_button.collidepoint(event.pos):
                    CHALLENGE = "hard"
                    display_tile_explanation_screen()  # Go to the tile explanation screen
                    running = False

    print(f"Difficulty selected: {CHALLENGE}")

# Start screen loop
display_difficulty_screen()
# Settings based on selected difficulty
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
POISON_LENGTH = settings["POISON_LENGTH"]
TILE_SIZE = 100
SCREEN_WIDTH = GRID_ROWS*TILE_SIZE
SCREEN_HEIGHT = GRID_COLS*TILE_SIZE

# Player settings
player = {
    "name": "Rabel Blago",
    "health": MAX_HEALTH,
    "mana": 0,
    "action_points": 3,
    "position": [0, 0],
    "keys_collected": 0,
    "souls_collected": 0,
    "moves_made": 0,
    "turns_taken": 0,
    "poisoned": False,  # New status effect for poison
    "poison_turns_left": 0  # Track how many turns the poison lasts
}

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Necrospire Nightmare")



# Load player image (replace with your player image file)
player_image = pygame.image.load("RabelBlago.png")  # Make sure to use the correct image file path

# Resize the player image to fit the tile size (optional, but recommended)
player_image = pygame.transform.scale(player_image, (TILE_SIZE, TILE_SIZE))

# Resize all tile images to match TILE_SIZE (100x100)
for key in tile_images:
    tile_images[key] = pygame.transform.scale(tile_images[key], (TILE_SIZE, TILE_SIZE))


# Dungeon generation
def generate_dungeon(rows, cols, isBoss = False):
    # Start with an empty dungeon
    dungeon = [["Empty" for _ in range(cols)] for _ in range(rows)]
    
    # Get all empty tile positions
    empty_positions = [(r, c) for r in range(rows) for c in range(cols)]
    
    # Shuffle the empty positions to randomly place tiles
    random.shuffle(empty_positions)
    
    # Create a list to store all keys and mana tiles with their lifespan
    all_keys = []
    all_mana = []
    all_healing = []
    
    # Place initial key
    for i in range(KEY_START):
        r, c = empty_positions.pop()
        dungeon[r][c] = "Key"
        all_keys.append({"position": (r, c), "lifespan": 0})  # Track position and lifespan
    
    # Place initial mana tiles
    for i in range(MANA_START):
        r, c = empty_positions.pop()
        dungeon[r][c] = "Mana"
        all_mana.append({"position": (r, c), "lifespan": 0})  # Track position and lifespan
    
    # Place intial traps
    for i in range(TRAP_START):
        r, c = empty_positions.pop()
        dungeon[r][c] = "Trap"
    
    # Place initial portals
    for i in range(PORTAL_START):
        r, c = empty_positions.pop()
        dungeon[r][c] = "Portal"
    
    # Place initial healing tiles
    for i in range(HEALING_START):
        r, c = empty_positions.pop()
        dungeon[r][c] = "Healing"
        all_healing.append({"position": (r, c), "inactive_turns": 0, "active": True})  # Track position and inactivity

    # Place the "Boss" or "Enemy" tile based on the isBoss flag
    if isBoss:
        # Ensure Boss tile doesn't spawn on top of the player
        r, c = rows - 1, cols - 1
        # Remember the original tile type for restoration later
        original_tile = dungeon[r][c]
        dungeon[r][c] = "Boss"
        boss_placed = True
        boss_position = (r,c)
        boss_health = 500  # Boss starts with 500 health
        print(f"Boss spawned with health {boss_health}") # Debugging
    else:
        # Place initial enemies in random tiles (not just empty)
        for _ in range(ENEMY_START):
            r, c = random.choice(empty_positions)
            dungeon[r][c] = "Enemy"
        boss_placed = False
        boss_position = None
        original_tile = None
        boss_health = "Dummy"
  
    return dungeon, all_keys, all_mana, all_healing, boss_placed, boss_position, original_tile, boss_health  # Return dungeon, all keys and mana tiles

# Display the dungeon grid and player
def display_dungeon(dungeon, player_pos, boss_position, boss_placed):
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            tile = dungeon[r][c]
            screen.blit(tile_images[tile], (c * TILE_SIZE, r * TILE_SIZE))

    # Draw the player image at the player's position
    player_rect = player_image.get_rect()  # Get the rect of the player image
    player_rect.topleft = (player_pos[1] * TILE_SIZE, player_pos[0] * TILE_SIZE)  # Set position based on player coordinates
    screen.blit(player_image, player_rect)  # Draw the player image on the screen
    if boss_placed:
        # Draw the boss image at the boss position
        boss_rect = tile_images["Boss"].get_rect()
        boss_rect.topleft = (boss_position[1] * TILE_SIZE, boss_position[0] * TILE_SIZE)
        screen.blit(tile_images["Boss"], boss_rect)  # Draw the boss image on the screen


# Add a new variable to store the previous position of the player
previous_position = player["position"].copy()

# Handle tile effects
def handle_tile(dungeon, all_mana, all_keys, all_healing, boss_placed, boss_health):
    global previous_position  # Make sure to modify the global previous_position
    r, c = player["position"]
    tile_type = dungeon[r][c]
    
    # Only process the tile logic if the player has moved to a new tile
    if [r, c] != previous_position:
        print(f"Player stepped on a {tile_type} tile at position ({r}, {c})")  # Debugging line
        tile_type = dungeon[r][c]
       # print(f"You stepped on a {tile_type} tile.")
        
        if tile_type == "Enemy":
            boss_health = combat(boss_placed, boss_health)
            if boss_health == "Dummy":
                dungeon[r][c] = "Empty"  # Remove enemy
        elif tile_type == "Mana":
            manaGain = random.randint(20, 60)  # Example range for mana gain, can be adjusted as needed
            print(f"You found a mana tile! Gaining {manaGain} mana.")
            player["mana"] += manaGain
            dungeon[r][c] = "Empty"  # Remove mana tile
            
            # If mana reaches 100, kill all but one enemy
            if player["mana"] >= MANA_KILL:
                player["mana"] -= MANA_KILL
                if boss_placed == False:
                    kill_enemies(dungeon)
                else:
                    boss_health = boss_health - 100
                    print(f"Mana strike on boss. Boss health drops 100 to {boss_health}")
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
            
            # Set the healing tile to inactive after use
            for healing_tile in all_healing:
                if healing_tile["position"] == (r, c):
                    healing_tile["active"] = False
                    break
        #elif tile_type == "Empty":
            #print("The tile is empty.")
        elif tile_type == "Boss":
            print(f"Encountering Boss with health {boss_health}")  # Debugging line
            boss_health = combat(boss_placed, boss_health)  # Engage in combat with the boss if player lands on it
            if boss_health <= 0:
                print("You have defeated the Boss!")
                dungeon[r][c] = "Empty"  # Remove the Boss
        elif tile_type == "Poison" and not player["poisoned"]:
            player["poisoned"] = True
            player["poison_turns_left"] = POISON_LENGTH  # Poison lasts for 4 turns
            print(f"You have been poisoned for {POISON_LENGTH} turns or until you find a cure!")
            dungeon[r][c] = "Empty"
        elif tile_type == "Elixir":
            if player["poisoned"]:
                player["poisoned"] = False
                player["poison_turns_left"] = 0
                print("The Elixir removed the poison effect!")
            dungeon[r][c] = "Empty"
        # Update the previous position to the current position after handling the tile
        if player["poisoned"]:
            player["health"] -= 5  # Damage from poison
            print(f"You are poisoned! Lose 5 health. Health: {player['health']}")
            player["poison_turns_left"] -= 1
            if player["poison_turns_left"] <= 0:
                player["poisoned"] = False
                print("The poison effect has worn off.")

        previous_position = [r, c]
    return boss_health
# Combat mechanics
def combat(boss_placed, boss_health):
    print("An enemy appears!")
    player_roll = roll_dice()
    if boss_placed:
        enemy_roll = roll_dice()
    else:
        enemy_roll = roll_dice(custom = True)
    print(f"Player rolls {player_roll}, Enemy rolls {enemy_roll}")
    enemy_damage = random.choice([5, 10, 15, 20, 25, 30, 35])  # Ensure this is an integer
    # If player rolls higher than enemy
    if player_roll > enemy_roll:
        if boss_placed:
            damage = random.randint(25, 50)
            print(f"Boss health before damage: {boss_health}")  # Debugging line
            boss_health -= damage  # Boss takes damage
            print(f"You dealt {damage} damage to the Boss! Boss health is now {boss_health}.")
        else:
            print("You defeated the enemy!")
            boss_health = "Dummy"
        player["souls_collected"] += 1
    else:
        enemy_damage = random.choice([5, 10, 15, 20, 25, 30, 35])  # Boss's damage
        print(f"The enemy hits you! Lose {enemy_damage} health.")
        player["health"] -= enemy_damage  # Player takes damage

    return boss_health  # Return the updated boss health

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
def roll_dice(sides=6, custom = False):
    if custom:
        # Return a random value from 2, 3, or 4 for the enemy's roll
        return random.choice([1, 2, 3])
    else:
        # Regular dice roll
        return random.randint(1, sides)

# Handle player movement and tile interaction
def move_player(direction, dungeon, all_keys, all_mana, all_healing, boss_placed, boss_health):
    r, c = player["position"]
    moved = False  # Flag to track if player moved
    if direction == "up" and r > 0:
        player["position"] = [r - 1, c]
        moved = True
    elif direction == "down" and r < GRID_ROWS - 1:
        player["position"] = [r + 1, c]
        moved = True
    elif direction == "left" and c > 0:
        player["position"] = [r, c - 1]
        moved = True
    elif direction == "right" and c < GRID_COLS - 1:
        player["position"] = [r, c + 1]
        moved = True
    else:
        print("You can't move in that direction!")
        return moved, boss_health

    # Consume an action point
    player["action_points"] -= 1
    if player["action_points"] < 0:
        print("No action points left! End your turn.")
        player["action_points"] = 0

    # Check tile interaction
    if moved:
        boss_health = handle_tile(dungeon, all_mana, all_keys, all_healing, boss_placed, boss_health)
        player["moves_made"] += 1
        player["turns_taken"] += 1  # Increase turn count
        if player["moves_made"] % 10 == 0:  # Poison starts after 10 moves
            spawn_poison_tiles(dungeon)
        if player["poisoned"] and player["moves_made"] % 15 == 0:  # Spawn Elixir tiles every 10 moves
            spawn_elixir_tiles(dungeon)
    # Track player moves and spawn enemies after every 3 moves

    if not boss_placed and player["moves_made"] % TURN_COUNT_ENEMY == 0:
        spawn_enemy(dungeon)
    if player["turns_taken"] % TURN_COUNT_KEY_SPAWN == 0:
        spawn_key(dungeon, all_keys)
    if player["turns_taken"] % TURN_COUNT_MANA_SPAWN == 0:
        spawn_mana(dungeon, all_mana)
    
    # Update keys' and mana tiles' lifespan
    update_lifespan(dungeon, all_keys, all_mana)
    return moved, boss_health

# Handle Boss movement towards the player
def move_boss(dungeon, player_position, boss_position, original_tile, boss_health):
    r, c = boss_position
    pr, pc = player_position
    boss_placed = True
    # List of adjacent tiles to the Boss
    adjacent_tiles = [
        (r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)
    ]
    
    # Remove any out-of-bound tiles
    valid_tiles = [
        (r_new, c_new) for r_new, c_new in adjacent_tiles if 0 <= r_new < len(dungeon) and 0 <= c_new < len(dungeon[0])
    ]
    
    # Find the tile with the minimum distance to the player
    closest_tile = min(valid_tiles, key=lambda tile: (abs(tile[0] - pr) + abs(tile[1] - pc)))
    
    # Remove the Boss from its current position and replace it with the original tile type
    dungeon[r][c] = original_tile
    
    # Place the Boss on the new tile
    br, bc = closest_tile
    original_tile = dungeon[br][bc]  # Save the new tile's original state
    dungeon[br][bc] = "Boss"  # Replace the new tile with Boss
    
    # Check if the boss moved to the player's tile
    if (br, bc) == (pr, pc):
        print("The Boss has encountered the player!")
        # Trigger combat between boss and player
        boss_health = combat(boss_placed, boss_health)  # Adjust health if needed

    return dungeon, closest_tile, original_tile, boss_health  # Return the updated dungeon and new Boss position

# Update lifespan function to handle keys and mana properly
def update_lifespan(dungeon, all_keys, all_mana):
    # Update keys' lifespan
    for key in all_keys[:]:  # Iterate over a copy of the list
        key["lifespan"] += 1  # Increment the lifespan of each key
        if key["lifespan"] >= TURN_COUNT_KEY_DEATH:
            # Remove the key if its lifespan has reached 5
            r, c = key["position"]
            dungeon[r][c] = "Empty"  # Set the tile to "Empty"
            all_keys.remove(key)  # Remove the key from the keys list

    # Update mana's lifespan
    for mana in all_mana[:]:  # Iterate over a copy of the list
        mana["lifespan"] += 1
        if mana["lifespan"] >= TURN_COUNT_MANA_DEATH:
            # Remove mana if lifespan has reached 5
            r, c = mana["position"]
            dungeon[r][c] = "Empty"  # Set the tile to "Empty"
            all_mana.remove(mana)  # Remove the mana tile from the list

# Spawn new mana tiles 
def spawn_mana(dungeon, all_mana):
    empty_tiles = [(r, c) for r in range(GRID_ROWS) for c in range(GRID_COLS) if dungeon[r][c] == "Empty"]
    if empty_tiles:
        r, c = random.choice(empty_tiles)
        dungeon[r][c] = "Mana"
        all_mana.append({"position": (r, c), "lifespan": 0})  # Explicitly set lifespan to 0 for new mana tiles

# Spawn an enemy on a random tile (including occupied ones)
def spawn_enemy(dungeon):
    all_tiles = [(r, c) for r in range(GRID_ROWS) for c in range(GRID_COLS)]
    random.shuffle(all_tiles)  # Shuffle to randomize spawn position
    for r, c in all_tiles:
        if dungeon[r][c] == "Empty":  # Only spawn on empty tiles
            dungeon[r][c] = "Enemy"
            break

# Spawn poison tiles (called after 10 moves)
def spawn_poison_tiles(dungeon):
    empty_tiles = [(r, c) for r in range(GRID_ROWS) for c in range(GRID_COLS) if dungeon[r][c] == "Empty"]
    if empty_tiles:
        r, c = random.choice(empty_tiles)
        # Avoid adding portals during the boss fight
        if dungeon[r][c] != "Portal":  # Ensure we are not accidentally adding a portal
            dungeon[r][c] = "Poison"
            print(f"Poison tile added at ({r}, {c})")  # Debugging line

# Spawn elixir tiles (called every 15 moves)
def spawn_elixir_tiles(dungeon):
    # Check if there is already an Elixir tile on the board
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            if dungeon[r][c] == "Elixir":
                print("An Elixir tile already exists. No new Elixir tile will be added.")
                return  # Exit the function if an Elixir tile already exists

    # If no Elixir tile exists, spawn a new one
    empty_tiles = [(r, c) for r in range(GRID_ROWS) for c in range(GRID_COLS) if dungeon[r][c] == "Empty"]
    if empty_tiles:
        r, c =random.choice(empty_tiles)
        dungeon[r][c] = "Elixir"
        print(f"Elixir tile added at ({r}, {c})")  # Debugging line

# Spawn a new key on a random tile
def spawn_key(dungeon, all_keys):
    empty_tiles = [(r, c) for r in range(GRID_ROWS) for c in range(GRID_COLS) if dungeon[r][c] == "Empty"]
    if empty_tiles:
        r, c = random.choice(empty_tiles)
        dungeon[r][c] = "Key"
        all_keys.append({"position": (r, c), "lifespan": 0})  # Explicitly set lifespan to 0 for new keys

# Win condition: Player wins when they have collected 3 keys and there are no enemies left
def check_win(dungeon, boss_health):
    if boss_health != "Dummy":
        if boss_health <= 0:
            print("Congratulions you've defeated the boss")
            return True
        else:
            return False
    if player["keys_collected"] >= WIN_CONDITION_KEY:
        for row in dungeon:
            if "Enemy" in row and boss_health == "Dummy":
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

# Handle healing tile state: active or inactive
def handle_healing_tiles(dungeon, all_healing):
    for healing_tile in all_healing:
        r, c = healing_tile["position"]
        # If the healing tile is active (the player has not used it yet)
        if healing_tile["active"]:
            healing_tile["inactive_turns"] = 0  # Reset inactive turns if active

        else:
            # Only increase inactive turns if the tile is inactive
            healing_tile["inactive_turns"] += 1  # Increase inactive turns if inactive
            dungeon[r][c] = "Empty"  # Mark as empty when inactive
            # If it has been inactive for 10 turns, it respawns as a healing tile
            if healing_tile["inactive_turns"] >= 10:
                dungeon[r][c] = "Healing"  # Respawn healing tile
                healing_tile["active"] = True  # Set the tile back to active
                healing_tile["inactive_turns"] = 0  # Reset the inactive turns
            
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

    dungeon, all_keys, all_mana, all_healing, boss_placed, boss_position, original_tile, boss_health = generate_dungeon(GRID_ROWS, GRID_COLS, isBoss=False)  # Generate new dungeon with Boss tile
    print(f"Welcome to Necrospire Nightmare, {player['name']}!")
    print("Starting the game with the following settings:")
    print(settings)
    # Pygame event loop
    player_moves = 0  # Counter to track the number of player moves
    running = True
    while running and player["health"] > 0:
        screen.fill((0, 0, 0))  # Clear the screen
        display_dungeon(dungeon, player["position"], boss_position, boss_placed)

        # Show player stats
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"Health: {player['health']}, Mana: {player['mana']}", True, (255, 255, 255))
        screen.blit(health_text, (10, SCREEN_HEIGHT - 40))

        keys_collected_text = font.render(f"Keys: {player['keys_collected']}, Souls: {player['souls_collected']}", True, (255, 255, 255))
        screen.blit(keys_collected_text, (10, SCREEN_HEIGHT - 80))

        # Handle events
        moved = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    moved, boss_health = move_player("up", dungeon, all_keys, all_mana, all_healing, boss_placed, boss_health)
                elif event.key == pygame.K_DOWN:
                    moved, boss_health = move_player("down", dungeon, all_keys, all_mana, all_healing, boss_placed, boss_health)
                elif event.key == pygame.K_LEFT:
                    moved, boss_health = move_player("left", dungeon, all_keys, all_mana, all_healing, boss_placed, boss_health)
                elif event.key == pygame.K_RIGHT:
                    moved, boss_health = move_player("right", dungeon, all_keys, all_mana, all_healing, boss_placed, boss_health)
                elif event.key == pygame.K_r:
                    roll_dice()
                elif event.key == pygame.K_e:
                    end_turn()

        # Handle tile interactions, including healing tiles
        boss_health = handle_tile(dungeon, all_mana, all_keys, all_healing, boss_placed, boss_health)  # Regular tile interactions
                # Only handle healing tiles if the player moved
        if moved:
            handle_healing_tiles(dungeon, all_healing)  # Handle healing tiles' inactivity and respawn

        pygame.display.update()
        # Increment player moves
        if moved:
            player_moves += 1
        # Move the Boss towards the Player after each turn
        if boss_placed and player_moves % 5 == 0 and moved:
            dungeon, boss_position, original_tile, boss_health = move_boss(dungeon, player["position"], boss_position, original_tile, boss_health)

        # Check win condition
        if check_win(dungeon, boss_health):
            screen.fill((0, 0, 0))  # Clear the screen
            pygame.display.update()
            pygame.time.wait(3000)  # Wait for 3 seconds before quitting the game
            if boss_placed == True:
                print("You've defeated the game!")
                pygame.quit()
                sys.exit()
            # After winning, generate the new dungeon with the Boss tile
            print("You won! Preparing for the Boss Fight...")
            dungeon, all_keys, all_mana, all_healing, boss_placed, boss_position, original_tile, boss_health = generate_dungeon(GRID_ROWS, GRID_COLS, isBoss=True)
            
            # Reset player's position and stats for the new dungeon if needed
            player["position"] = [0, 0]  # Starting position for the boss dungeon
            player["health"] = MAX_HEALTH
            player["mana"] = 0
            player["action_points"] = 3
            player["keys_collected"] = 0
            player["souls_collected"] = 0
            player["moves_made"] = 0
            player["turns_taken"] = 0
            print("Boss Dungeon started!")

        # Check if player health reaches 0
        if player["health"] <= 0:
            print("You have perished in the Necrospire. Game Over!")
            running = False

    pygame.quit()

if __name__ == "__main__":
    main(settings)
