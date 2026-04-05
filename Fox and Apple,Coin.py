import pgzrun
from random import randint

# =======================
# Screen Size
# =======================
WIDTH = 1200
HEIGHT = 800

# =======================
# Game Variables
# =======================
score = 0
gameover = False
game_started = False
timer_minutes = 1  # default
timer_seconds = 0

# =======================
# Actors
# =======================
wolf = Actor("fox")
wolf.pos = (100, 100)

coin = Actor("coin")
coin.pos = (200, 200)

apple = Actor("apple")
apple.pos = (300, 300)

# =======================
# Helper Functions
# =======================
def draw():
    screen.clear()
    if not game_started:
        # Start menu
        screen.draw.text("Set Game Duration (minutes):", center=(WIDTH//2, HEIGHT//3), fontsize=60, color="yellow")
        screen.draw.text(f"{timer_minutes}", center=(WIDTH//2, HEIGHT//2), fontsize=80, color="white")
        screen.draw.text("Use UP/DOWN to change, ENTER to start, 0 = No Timer", center=(WIDTH//2, HEIGHT//2 + 100), fontsize=40, color="yellow")
    elif gameover:
        # Game over screen
        screen.draw.text("Game Over", center=(WIDTH//2, 150), fontsize=60, color="yellow")
        screen.draw.text(f"Final Score: {score}", center=(WIDTH//2, 300), fontsize=50, color="white")
        screen.draw.text("Click Anywhere to Restart", center=(WIDTH//2, 450), fontsize=40, color="yellow")
    else:
        # Game screen
        wolf.draw()
        coin.draw()
        apple.draw()
        screen.draw.text(f"Score: {score}", topleft=(10, 10), fontsize=40, color="white")
        if timer_seconds > 0:
            screen.draw.text(f"Time Left: {int(timer_seconds)}s", topright=(WIDTH-10, 10), fontsize=40, color="red")

def place_coin():
    coin.x = randint(20, WIDTH - 20)
    coin.y = randint(20, HEIGHT - 20)

def place_apple():
    apple.x = randint(20, WIDTH - 20)
    apple.y = randint(20, HEIGHT - 20)

def start_game():
    global game_started, score, gameover, timer_seconds
    game_started = True
    gameover = False
    score = 0
    wolf.pos = (100, 100)
    place_coin()
    place_apple()
    timer_seconds = timer_minutes * 60 if timer_minutes > 0 else 0

def update():
    global score, timer_seconds, gameover
    if not game_started or gameover:
        return

    # Movement
    if keyboard.left:
        wolf.x -= 5
    if keyboard.right:
        wolf.x += 5
    if keyboard.up:
        wolf.y -= 5
    if keyboard.down:
        wolf.y += 5

    # Keep wolf inside screen
    wolf.x = max(0, min(WIDTH, wolf.x))
    wolf.y = max(0, min(HEIGHT, wolf.y))

    # Collision
    if wolf.colliderect(coin):
        score += 10
        place_coin()
    if wolf.colliderect(apple):
        score += 20
        place_apple()

    # Timer countdown
    if timer_seconds > 0:
        timer_seconds -= 1/60  # approx 60 FPS
        if timer_seconds <= 0:
            timer_seconds = 0
            gameover = True

def on_key_down(key):
    global timer_minutes
    if not game_started:
        if key == keys.UP:
            timer_minutes += 1
        elif key == keys.DOWN:
            timer_minutes = max(0, timer_minutes - 1)
        elif key == keys.RETURN:
            start_game()

def on_mouse_down(pos):
    if gameover:
        start_game()

pgzrun.go()