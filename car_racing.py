import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game")

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
RED = (200, 0, 0)
BLUE = (0, 102, 204)
BLACK = (0, 0, 0)
LIGHT_BLUE = (135, 206, 250)
DARK_GRAY = (30, 30, 30)
POLICE_BLUE = (0, 51, 153)
POLICE_RED = (204, 0, 0)
TAXI_YELLOW = (255, 221, 51)
VAN_GRAY = (180, 180, 180)
BORDER_YELLOW = (255, 204, 0)
GRASS_GREEN = (80, 200, 80)
BUSH_GREEN = (34, 139, 34)

# Car settings
CAR_WIDTH, CAR_HEIGHT = 36, 68  # smaller player car
car_x = WIDTH // 2 - CAR_WIDTH // 2
car_y = HEIGHT - CAR_HEIGHT - 20
car_speed = 9  # was 5, faster horizontal movement

# Obstacle settings
OBSTACLE_TYPES = [
    {"type": "red", "width": 40, "height": 90},
    {"type": "orange", "width": 40, "height": 90},
]
obstacle_speed = 4  # was 5, slower for more reaction time
obstacle_frequency = 30  # frames
obstacles = []  # Each: [x, y, type, width, height]

# Coin settings
COIN_RADIUS = 12
COIN_COLOR = (255, 215, 0)  # Gold
COIN_OUTLINE = (255, 255, 255)
coin_frequency = 45  # frames
coins = []  # Each: [x, y]

# Road settings
road_width = 250
road_x = WIDTH // 2 - road_width // 2
lane_marker_width = 10
lane_marker_height = 50
lane_marker_gap = 20
lane_marker_y = 0

# Fonts
font = pygame.font.SysFont("Arial", 48)
small_font = pygame.font.SysFont("Arial", 32)

LEADERBOARD_FILE = "leaderboard.txt"
LEADERBOARD_SIZE = 5

# Add a variable to control minimum vertical gap between obstacles
# Increase vertical gap for more space
MIN_OBSTACLE_VERTICAL_GAP = 700  # was 300
last_obstacle_y = -MIN_OBSTACLE_VERTICAL_GAP

# For diagonal obstacle spacing, track previous obstacle lanes
prev_obstacle_lanes = set()

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, "r") as f:
        lines = f.readlines()
    scores = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Try to parse as tuple (name, score)
        if ',' in line:
            parts = line.split(',', 1)
            name = parts[0].strip()
            try:
                score = int(parts[1].strip())
            except ValueError:
                continue
            scores.append((name, score))
        else:
            # Old format: just an integer
            try:
                score = int(line)
                scores.append(("Player", score))
            except ValueError:
                continue
    return scores[:LEADERBOARD_SIZE]

def save_leaderboard(scores):
    with open(LEADERBOARD_FILE, "w") as f:
        for entry in scores[:LEADERBOARD_SIZE]:
            if isinstance(entry, tuple):
                f.write(f"{entry[0]},{entry[1]}\n")
            else:
                f.write(f"Player,{entry}\n")

def draw_bush(x, y):
    pygame.draw.ellipse(screen, BUSH_GREEN, (x, y, 32, 24))
    pygame.draw.ellipse(screen, (0, 100, 0), (x+8, y+8, 20, 14))
    pygame.draw.ellipse(screen, (60, 179, 113), (x+16, y+4, 16, 12))

def draw_road():
    # Draw grass
    screen.fill(GRASS_GREEN)
    # Draw road
    pygame.draw.rect(screen, (40, 40, 40), (road_x, 0, road_width, HEIGHT))
    # Draw yellow borders
    pygame.draw.rect(screen, BORDER_YELLOW, (road_x-12, 0, 12, HEIGHT))
    pygame.draw.rect(screen, BORDER_YELLOW, (road_x+road_width, 0, 12, HEIGHT))
    # Draw lane dividers
    lane_count = 3
    lane_width = road_width // lane_count
    for i in range(1, lane_count):
        x = road_x + i * lane_width
        y = 0
        while y < HEIGHT:
            pygame.draw.rect(screen, (255, 255, 255), (x-3, y+20, 6, 40), border_radius=3)
            y += 80
    # Draw bushes (corners and sides)
    for y in [30, HEIGHT-60]:
        for x in [10, WIDTH-42]:
            draw_bush(x, y)
    for y in range(100, HEIGHT-100, 120):
        draw_bush(10, y)
        draw_bush(WIDTH-42, y)

def draw_player_car(x, y):
    # Taxi body
    pygame.draw.rect(screen, TAXI_YELLOW, (x+5, y+10, CAR_WIDTH-10, CAR_HEIGHT-20), border_radius=16)
    # Windows
    pygame.draw.rect(screen, BLACK, (x+13, y+18, CAR_WIDTH-26, 28), border_radius=8)
    # Taxi sign
    sign_rect = pygame.Rect(x+CAR_WIDTH//2-18, y+10, 36, 14)
    pygame.draw.rect(screen, (255, 255, 255), sign_rect, border_radius=5)
    font_sign = pygame.font.SysFont("Arial", 12, bold=True)
    sign_text = font_sign.render("CRAZY", True, (0,0,0))
    screen.blit(sign_text, (sign_rect.x + (sign_rect.width-sign_text.get_width())//2, sign_rect.y+1))
    # Wheels
    pygame.draw.ellipse(screen, (60,60,60), (x+2, y+20, 12, 28))
    pygame.draw.ellipse(screen, (60,60,60), (x+CAR_WIDTH-14, y+20, 12, 28))
    pygame.draw.ellipse(screen, (60,60,60), (x+2, y+CAR_HEIGHT-38, 12, 28))
    pygame.draw.ellipse(screen, (60,60,60), (x+CAR_WIDTH-14, y+CAR_HEIGHT-38, 12, 28))
    # Headlights
    pygame.draw.ellipse(screen, (255, 255, 180), (x+14, y+CAR_HEIGHT-14, 10, 8))
    pygame.draw.ellipse(screen, (255, 255, 180), (x+CAR_WIDTH-24, y+CAR_HEIGHT-14, 10, 8))
    # Rear lights
    pygame.draw.ellipse(screen, (255, 80, 80), (x+14, y+6, 10, 8))
    pygame.draw.ellipse(screen, (255, 80, 80), (x+CAR_WIDTH-24, y+6, 10, 8))
    # Taxi stripes
    for i in range(3):
        pygame.draw.rect(screen, (0,0,0), (x+CAR_WIDTH//2-10+i*7, y+40, 5, 10), border_radius=2)


def draw_obstacle_car(x, y, car_type, width, height):
    if car_type == "red":
        # Red sports car
        pygame.draw.rect(screen, (200, 30, 30), (x+5, y+10, width-10, height-20), border_radius=16)
        pygame.draw.rect(screen, BLACK, (x+13, y+18, width-26, 28), border_radius=8)
        # Stripes
        pygame.draw.rect(screen, (255,255,255), (x+width//2-6, y+18, 4, height-36), border_radius=2)
        pygame.draw.rect(screen, (255,255,255), (x+width//2+2, y+18, 4, height-36), border_radius=2)
        # Wheels
        pygame.draw.ellipse(screen, (60,60,60), (x+2, y+20, 12, 28))
        pygame.draw.ellipse(screen, (60,60,60), (x+width-14, y+20, 12, 28))
        pygame.draw.ellipse(screen, (60,60,60), (x+2, y+height-38, 12, 28))
        pygame.draw.ellipse(screen, (60,60,60), (x+width-14, y+height-38, 12, 28))
    elif car_type == "orange":
        # Orange sports car
        pygame.draw.rect(screen, (255, 140, 0), (x+5, y+10, width-10, height-20), border_radius=16)
        pygame.draw.rect(screen, BLACK, (x+13, y+18, width-26, 28), border_radius=8)
        # Stripes
        pygame.draw.rect(screen, (255,255,255), (x+width//2-3, y+18, 6, height-36), border_radius=2)
        # Wheels
        pygame.draw.ellipse(screen, (60,60,60), (x+2, y+20, 12, 28))
        pygame.draw.ellipse(screen, (60,60,60), (x+width-14, y+20, 12, 28))
        pygame.draw.ellipse(screen, (60,60,60), (x+2, y+height-38, 12, 28))
        pygame.draw.ellipse(screen, (60,60,60), (x+width-14, y+height-38, 12, 28))
    else:
        # Default: red car
        pygame.draw.rect(screen, (200, 30, 30), (x+5, y+10, width-10, height-20), border_radius=16)
        pygame.draw.rect(screen, BLACK, (x+13, y+18, width-26, 28), border_radius=8)
        pygame.draw.rect(screen, (255,255,255), (x+width//2-6, y+18, 4, height-36), border_radius=2)
        pygame.draw.rect(screen, (255,255,255), (x+width//2+2, y+18, 4, height-36), border_radius=2)
        pygame.draw.ellipse(screen, (60,60,60), (x+2, y+20, 12, 28))
        pygame.draw.ellipse(screen, (60,60,60), (x+width-14, y+20, 12, 28))
        pygame.draw.ellipse(screen, (60,60,60), (x+2, y+height-38, 12, 28))
        pygame.draw.ellipse(screen, (60,60,60), (x+width-14, y+height-38, 12, 28))

def draw_coin(x, y):
    pygame.draw.circle(screen, COIN_COLOR, (x, y), COIN_RADIUS)
    pygame.draw.circle(screen, COIN_OUTLINE, (x, y), COIN_RADIUS, 2)
    pygame.draw.circle(screen, (255, 255, 153), (x, y), COIN_RADIUS//2)

OBSTACLE_LANES = [
    0,  # left
    1,  # center
    2   # right
]

def get_lane_x(lane, car_width):
    if lane == 0:
        return road_x + 20
    elif lane == 1:
        return road_x + road_width//2 - car_width//2
    else:
        return road_x + road_width - car_width - 20

def show_game_over(coin_count, leaderboard, is_new_high):
    y_base = HEIGHT // 2 - 120
    # Draw semi-transparent background for readability
    overlay = pygame.Surface((WIDTH, 320), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, y_base-20))
    text = font.render("GAME OVER", True, RED)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_base))
    coin_text = small_font.render(f"Coins: {coin_count}", True, COIN_COLOR)
    screen.blit(coin_text, (WIDTH // 2 - coin_text.get_width() // 2, y_base + 60))
    restart_text = small_font.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, y_base + 110))
    # Leaderboard
    lb_title = small_font.render("Leaderboard (Most Coins)", True, WHITE)
    screen.blit(lb_title, (WIDTH // 2 - lb_title.get_width() // 2, y_base + 170))
    for i, entry in enumerate(leaderboard):
        score = entry[1] if isinstance(entry, tuple) else entry
        color = COIN_COLOR if is_new_high and coin_count == score else WHITE
        name = entry[0] if isinstance(entry, tuple) else "---"
        lb_entry = small_font.render(f"{i+1}. {name}: {score}", True, color)
        screen.blit(lb_entry, (WIDTH // 2 - lb_entry.get_width() // 2, y_base + 200 + i*32))
    pygame.display.flip()

def show_welcome_screen():
    bg = pygame.Surface((WIDTH, HEIGHT))
    bg.fill((60, 180, 120))
    # Draw a stylized road
    pygame.draw.rect(bg, (40, 40, 40), (road_x, 0, road_width, HEIGHT))
    pygame.draw.rect(bg, BORDER_YELLOW, (road_x-12, 0, 12, HEIGHT))
    pygame.draw.rect(bg, BORDER_YELLOW, (road_x+road_width, 0, 12, HEIGHT))
    # Lane dividers
    lane_count = 3
    lane_width = road_width // lane_count
    for i in range(1, lane_count):
        x = road_x + i * lane_width
        y = 0
        while y < HEIGHT:
            pygame.draw.rect(bg, (255, 255, 255), (x-3, y+20, 6, 40), border_radius=3)
            y += 80
    # Bushes
    for y in [30, HEIGHT-60]:
        for x in [10, WIDTH-42]:
            draw_bush(x, y)
    for y in range(100, HEIGHT-100, 120):
        draw_bush(10, y)
        draw_bush(WIDTH-42, y)
    # Welcome text (split into two lines)
    title_font = pygame.font.SysFont("Arial", 36, bold=True)
    title1 = title_font.render("Welcome to", True, (255, 255, 255))
    title2 = title_font.render("SFNOC CAR RACING!", True, (255, 255, 255))
    # Draw semi-transparent background for text
    overlay = pygame.Surface((WIDTH, 140), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    bg.blit(overlay, (0, 30))
    bg.blit(title1, (WIDTH//2 - title1.get_width()//2, 40))
    bg.blit(title2, (WIDTH//2 - title2.get_width()//2, 90))
    # Press key to continue
    prompt = small_font.render("Press any key to start", True, (255,255,255))
    bg.blit(prompt, (WIDTH//2 - prompt.get_width()//2, 150))
    # Instructions at the bottom
    instr1 = small_font.render("Use keyboard right and left arrows", True, (255,255,255))
    instr2 = small_font.render("to steer the car", True, (255,255,255))
    bg.blit(instr1, (WIDTH//2 - instr1.get_width()//2, HEIGHT-70))
    bg.blit(instr2, (WIDTH//2 - instr2.get_width()//2, HEIGHT-40))
    screen.blit(bg, (0,0))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def get_player_name():
    show_welcome_screen()
    input_box = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 32, 200, 48)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False
    prompt = small_font.render('Enter your name:', True, WHITE)
    start_button_text = small_font.render('Start Game', True, WHITE)
    start_button_width = start_button_text.get_width() + 40
    start_button = pygame.Rect(WIDTH//2 - start_button_width//2, HEIGHT//2 + 40, start_button_width, 40)
    start_button_color = pygame.Color('green')
    show_start = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                color = color_active if active else color_inactive
                if show_start and start_button.collidepoint(event.pos):
                    done = True
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        show_start = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif len(text) < 16 and event.unicode.isprintable():
                        text += event.unicode
        screen.fill((0, 150, 0))
        draw_road()
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 - 100))
        txt_surface = small_font.render(text if text else 'Player', True, WHITE)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+10))
        pygame.draw.rect(screen, color, input_box, 2)
        if show_start:
            pygame.draw.rect(screen, start_button_color, start_button, border_radius=8)
            screen.blit(start_button_text, (start_button.x + (start_button.width - start_button_text.get_width())//2, start_button.y + 8))
        pygame.display.flip()
    return text if text.strip() else 'Player'

def get_obstacle_speed(coin_count):
    if coin_count >= 60:
        return 7
    elif coin_count >= 30:
        return 5
    else:
        return 4

def main():
    global car_x, lane_marker_y, obstacles, coins, last_obstacle_y, prev_obstacle_lanes
    player_name = get_player_name()
    clock = pygame.time.Clock()
    running = True
    game_over = False
    frame_count = 0
    score = 0
    coin_count = 0
    center_lane = 1
    car_x = get_lane_x(center_lane, CAR_WIDTH)
    obstacles = []
    coins = []
    lane_marker_y = 0
    leaderboard = load_leaderboard()
    is_new_high = False
    last_obstacle_lanes = set()
    last_obstacle_y = -MIN_OBSTACLE_VERTICAL_GAP
    prev_obstacle_lanes = set()
    last_obs_y_per_lane = [-MIN_OBSTACLE_VERTICAL_GAP for _ in OBSTACLE_LANES]
    force_side_lane_counter = random.randint(120, 240)
    force_side_lane_next = False
    wall_cooldown = 0
    WALL_VERTICAL_GAP = 2 * MIN_OBSTACLE_VERTICAL_GAP
    SAFE_GAP = int(CAR_HEIGHT * 3.5)
    DIAGONAL_GAP = int(CAR_HEIGHT * 4)
    last_spawned_obs_y = -CAR_HEIGHT * 5  # Track last obstacle spawn y
    while running:
        screen.fill((0, 150, 0))  # Green grass background
        draw_road()
        draw_player_car(car_x, car_y)

        # Dynamic obstacle speed based on coins
        current_obstacle_speed = get_obstacle_speed(coin_count)
        # Move lane markers
        lane_marker_y += current_obstacle_speed
        if lane_marker_y > lane_marker_height + lane_marker_gap:
            lane_marker_y = 0

        # Handle obstacles and coins
        if not game_over:
            if frame_count % obstacle_frequency == 0:
                # Only spawn if last obstacle is far enough down
                if not obstacles or (obstacles and all(obs[1] > last_spawned_obs_y + CAR_HEIGHT * 5 for obs in obstacles)):
                    new_obstacles = []
                    lanes_to_block = set()
                    can_spawn_wall = False
                    if wall_cooldown <= 0:
                        last_wall_y = max([obs[1] for obs in obstacles if len(obs) > 6 and obs[6]] + [-WALL_VERTICAL_GAP])
                        if all(obs[1] < -WALL_VERTICAL_GAP for obs in obstacles):
                            can_spawn_wall = True
                    if can_spawn_wall:
                        open_lane = random.choice(OBSTACLE_LANES)
                        for lane in OBSTACLE_LANES:
                            if lane == open_lane:
                                continue
                            car_choice = random.choice(OBSTACLE_TYPES)
                            x = get_lane_x(lane, car_choice["width"])
                            obs_y = -car_choice["height"]
                            obs = [x, obs_y, car_choice["type"], car_choice["width"], car_choice["height"], lane, True]
                            new_obstacles.append(obs)
                            last_obs_y_per_lane[lane] = obs_y
                        wall_cooldown = random.randint(6, 10)
                    else:
                        wall_cooldown -= 1
                        if force_side_lane_next:
                            lanes_to_block.add(center_lane)
                            force_side_lane_next = False
                            force_side_lane_counter = random.randint(120, 240)
                        else:
                            force_side_lane_counter -= 1
                            if force_side_lane_counter <= 0:
                                force_side_lane_next = True
                        # Randomly select 1 or 2 lanes to place obstacles in (never all 3)
                        num_obstacles = random.choice([1, 2])
                        candidate_lanes = OBSTACLE_LANES[:]
                        random.shuffle(candidate_lanes)
                        chosen_lanes = candidate_lanes[:num_obstacles]
                        for lane in chosen_lanes:
                            car_choice = random.choice(OBSTACLE_TYPES)
                            x = get_lane_x(lane, car_choice["width"])
                            new_obs_y = -car_choice["height"]
                            can_spawn = True
                            for obs in obstacles:
                                # Avoid obstacles in all lanes at the same y
                                if len([o for o in obstacles if abs(o[1] - new_obs_y) < 1 and o[5] != lane]) >= 2:
                                    can_spawn = False
                                    break
                                # Ensure diagonal gap to obstacles in any other lane
                                if lane != obs[5] and abs(new_obs_y - obs[1]) < DIAGONAL_GAP:
                                    can_spawn = False
                                    break
                            if lane in lanes_to_block:
                                can_spawn = True
                            if can_spawn:
                                new_obstacles.append([x, new_obs_y, car_choice["type"], car_choice["width"], car_choice["height"], lane, False])
                                last_obs_y_per_lane[lane] = new_obs_y
                        if not new_obstacles:
                            lane = random.choice(OBSTACLE_LANES)
                            car_choice = random.choice(OBSTACLE_TYPES)
                            x = get_lane_x(lane, car_choice["width"])
                            new_obs_y = -car_choice["height"]
                            new_obstacles.append([x, new_obs_y, car_choice["type"], car_choice["width"], car_choice["height"], lane, False])
                            last_obs_y_per_lane[lane] = new_obs_y
                    obstacles.extend(new_obstacles)
                    if new_obstacles:
                        last_spawned_obs_y = -car_choice["height"]
                obstacles.extend(new_obstacles)
            for obs in obstacles:
                obs[1] += current_obstacle_speed
                draw_obstacle_car(obs[0], obs[1], obs[2], obs[3], obs[4])
            # Remove off-screen obstacles
            for obs in obstacles:
                if obs[1] < HEIGHT:
                    last_obs_y_per_lane[obs[5]] = obs[1]
            obstacles = [obs for obs in obstacles if obs[1] < HEIGHT]
            # Collision detection (only way to set game_over)
            for obs in obstacles:
                car_rect = pygame.Rect(car_x, car_y, CAR_WIDTH, CAR_HEIGHT)
                obs_rect = pygame.Rect(obs[0], obs[1], obs[3], obs[4])
                if car_rect.colliderect(obs_rect):
                    game_over = True
                    leaderboard = load_leaderboard()
                    leaderboard.append((player_name, coin_count))
                    name_to_score = {}
                    for name, score in leaderboard:
                        if name not in name_to_score or score > name_to_score[name]:
                            name_to_score[name] = score
                    leaderboard = sorted(name_to_score.items(), key=lambda x: x[1], reverse=True)[:LEADERBOARD_SIZE]
                    is_new_high = coin_count in [entry[1] for entry in leaderboard[:1]]
                    save_leaderboard(leaderboard)
            score += 1

            # --- COINS ---
            if frame_count % coin_frequency == 0:
                possible_lanes = [0, 1, 2]
                obstacle_lanes_y = [(obs[5], obs[1], obs[4]) for obs in obstacles if obs[1] < 100]
                safe_lanes = []
                for lane in possible_lanes:
                    if not any(lane == obs_lane and abs(obs_y + obs_h//2) < 100 for obs_lane, obs_y, obs_h in obstacle_lanes_y):
                        safe_lanes.append(lane)
                if safe_lanes:
                    coin_lane = random.choice(safe_lanes)
                    coin_x = get_lane_x(coin_lane, CAR_WIDTH//2) + CAR_WIDTH//4
                    coins.append([coin_x, -COIN_RADIUS*2, coin_lane])
            for coin in coins:
                coin[1] += current_obstacle_speed
                draw_coin(coin[0], coin[1])
            car_rect = pygame.Rect(car_x, car_y, CAR_WIDTH, CAR_HEIGHT)
            new_coins = []
            for coin in coins:
                coin_rect = pygame.Rect(coin[0] - COIN_RADIUS, coin[1] - COIN_RADIUS, COIN_RADIUS*2, COIN_RADIUS*2)
                if car_rect.colliderect(coin_rect):
                    coin_count += 1
                else:
                    if coin[1] < HEIGHT + COIN_RADIUS:
                        new_coins.append(coin)
            coins = new_coins

        # Draw score and coin count
        score_text = small_font.render(f"Score: {score//10}", True, WHITE)
        screen.blit(score_text, (10, 10))
        coin_text = small_font.render(f"Coins: {coin_count}", True, COIN_COLOR)
        screen.blit(coin_text, (10, 40))

        if game_over:
            show_game_over(coin_count, leaderboard, is_new_high)

        pygame.display.flip()
        clock.tick(60)
        frame_count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main()  # Restart
                        return
                    elif event.key == pygame.K_q:
                        running = False

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and car_x > road_x + 5:
                car_x -= car_speed
            if keys[pygame.K_RIGHT] and car_x < road_x + road_width - CAR_WIDTH - 5:
                car_x += car_speed

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 