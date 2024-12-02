import turtle
import pyaudio
import math
import time
import random
import wave
import threading

# Screen setup
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders with Images")
wn.tracer(0)

# Register images
wn.register_shape("alien.gif")  # Replace with your alien image file
wn.register_shape("player.gif")  # Replace with your player image file

def play_background_music():
    """Play the background music using pyaudio in a separate thread."""
    chunk_size = 1024
    music_file = "bgm.wav"  # Path to your background music file

    # Open the wave file
    wf = wave.open(music_file, 'rb')

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Loop the music indefinitely
    while True:
        data = wf.readframes(chunk_size)
        while data:
            stream.write(data)
            data = wf.readframes(chunk_size)

    # Close the stream (never reached in this case)
    stream.stop_stream()
    stream.close()
    p.terminate()

# Function to play background music in a new thread
def play_background_music_in_thread():
    """Run the play_background_music function in a separate thread."""
    bg_music_thread = threading.Thread(target=play_background_music)
    bg_music_thread.daemon = True  # This ensures the thread will exit when the program ends
    bg_music_thread.start()

# Play sound for explosion using pyaudio in a separate thread
def play_explosion_sound():
    """Play the explosion sound using pyaudio in a separate thread."""
    chunk_size = 1024
    sound_file = "explosion.wav"  # Path to your explosion sound file

    # Open the wave file
    wf = wave.open(sound_file, 'rb')

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Read and play audio in chunks
    data = wf.readframes(chunk_size)
    while data:
        stream.write(data)
        data = wf.readframes(chunk_size)

    # Close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

def play_sound_in_thread():
    """Run the play_explosion_sound function in a separate thread."""
    sound_thread = threading.Thread(target=play_explosion_sound)
    sound_thread.start()

# Play sound for laser firing using pyaudio in a separate thread
def play_laser_sound():
    """Play the laser sound using pyaudio in a separate thread."""
    chunk_size = 1024
    sound_file = "laser.wav"  # Path to your laser sound file

    # Open the wave file
    wf = wave.open(sound_file, 'rb')

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Read and play audio in chunks
    data = wf.readframes(chunk_size)
    while data:
        stream.write(data)
        data = wf.readframes(chunk_size)

    # Close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

def play_laser_in_thread():
    """Run the play_laser_sound function in a separate thread."""
    laser_thread = threading.Thread(target=play_laser_sound)
    laser_thread.start()

# Function to play win music in a separate thread
def play_win_music():
    """Play the win music using pyaudio in a separate thread."""
    chunk_size = 1024
    music_file = "you_won.wav"  # Path to your win music file

    # Open the wave file
    wf = wave.open(music_file, 'rb')

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Read and play audio in chunks
    data = wf.readframes(chunk_size)
    while data:
        stream.write(data)
        data = wf.readframes(chunk_size)

    # Close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

# Function to play sound in a new thread
def play_win_music_in_thread():
    """Run the play_win_music function in a separate thread."""
    win_music_thread = threading.Thread(target=play_win_music)
    win_music_thread.start()

# Border setup
def draw_border():
    border_pen = turtle.Turtle()
    border_pen.speed(0)
    border_pen.color("white")
    border_pen.penup()
    border_pen.setposition(-300, -300)
    border_pen.pendown()
    border_pen.pensize(3)
    for side in range(4):
        border_pen.fd(600)
        border_pen.lt(90)
    border_pen.hideturtle()

draw_border()

# Score setup
score = 0
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
score_pen.hideturtle()

def update_score():
    score_pen.clear()
    score_pen.write(f"Score: {score}", align="left", font=("Arial", 14, "normal"))

update_score()

# Player setup
player = turtle.Turtle()
player.shape("player.gif")  # Set the player image
player.penup()
player.speed(0)
player.setposition(0, -280)
player.move_speed = 10

# Bullet setup
class Bullet(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("triangle")
        self.color("yellow")
        self.penup()
        self.speed(0)
        self.setheading(90)
        self.shapesize(0.5, 0.5)
        self.hideturtle()
        self.active = False

    def fire(self, x, y):
        if not self.active:
            self.setposition(x, y + 10)
            self.showturtle()
            self.active = True
            play_laser_in_thread()

    def move(self):
        if self.active:
            self.sety(self.ycor() + 15)
            if self.ycor() > 275:
                self.hideturtle()
                self.active = False

bullets = [Bullet() for _ in range(5)]  # Pool of bullets

# Enemy setup
class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.shape("alien.gif")  # Set the alien image
        self.penup()
        self.speed(0)
        self.setposition(x, y)

    def move(self, dx, dy):
        self.setx(self.xcor() + dx)
        self.sety(self.ycor() + dy)

enemies = []
enemy_rows = 5
enemy_cols = 10
enemy_start_x = -225
enemy_start_y = 250
enemy_spacing_x = 50
enemy_spacing_y = 40

for row in range(enemy_rows):
    for col in range(enemy_cols):
        x = enemy_start_x + (col * enemy_spacing_x)
        y = enemy_start_y - (row * enemy_spacing_y)
        enemies.append(Enemy(x, y))

enemy_dx = 2
enemy_dy = 10
enemy_delay = 0.02


def fire_bullet():
    for bullet in bullets:
        if not bullet.active:
            bullet.fire(player.xcor(), player.ycor())
            break

# Collision detection
def is_collision(obj1, obj2):
    distance = math.sqrt((obj1.xcor() - obj2.xcor())**2 + (obj1.ycor() - obj2.ycor())**2)
    return distance < 15

# Alien Bullet setup
class AlienBullet(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("triangle")
        self.color("red")
        self.penup()
        self.speed(0)
        self.setheading(270)  # Bullet moves downward
        self.shapesize(0.5, 0.5)
        self.hideturtle()
        self.active = False

    def fire(self, x, y):
        if not self.active:
            self.setposition(x, y - 10)
            self.showturtle()
            self.active = True

    def move(self):
        if self.active:
            self.sety(self.ycor() - 15)
            if self.ycor() < -300:
                self.hideturtle()
                self.active = False

alien_bullets = [AlienBullet() for _ in range(5)]  # Pool of alien bullets

def alien_fire_bullet():
    if enemies:
        # Select up to 4 random aliens (or 1 if only 1 alien remains)
        firing_aliens = random.sample(enemies, min(4, len(enemies)))
        for enemy in firing_aliens:
            for bullet in alien_bullets:
                if not bullet.active:
                    bullet.fire(enemy.xcor(), enemy.ycor())
                    break

# Game over and winning messages
def display_message(text):
    message_pen = turtle.Turtle()
    message_pen.speed(0)
    message_pen.color("white")
    message_pen.penup()
    message_pen.hideturtle()
    message_pen.setposition(0, 0)
    message_pen.write(text, align="center", font=("Arial", 36, "normal"))
    message_pen.setposition(0, -40)
    message_pen.write(f"Final Score: {score}", align="center", font=("Arial", 24, "normal"))
    wn.update()
    time.sleep(1)
    if text == "YOU WON!":
        play_win_music_in_thread()  # Play win music when the player wins
    time.sleep(3) 

# Movement control variables
player_direction = 0  # -1 for left, 1 for right, 0 for no movement

# Functions to start and stop movement
def move_left_start():
    global player_direction
    player_direction = -1  # Move left

def move_right_start():
    global player_direction
    player_direction = 1  # Move right

def stop_movement():
    global player_direction
    player_direction = 0  # Stop moving

# Continuous movement update
def update_player_position():
    if player_direction == -1:  # Moving left
        player.setx(max(player.xcor() - player.move_speed, -280))
    elif player_direction == 1:  # Moving right
        player.setx(min(player.xcor() + player.move_speed, 280))
 
# Keyboard bindings for continuous movement
wn.listen()
wn.onkeypress(move_left_start, "Left")    # Start moving left
wn.onkeypress(move_right_start, "Right")  # Start moving right
wn.onkeyrelease(stop_movement, "Left")    # Stop moving left
wn.onkeyrelease(stop_movement, "Right")   # Stop moving right
wn.onkeypress(fire_bullet, "space")       # Fire bullet

# Start background music when the game begins
play_background_music_in_thread()

# Function to adjust enemy speed
def adjust_enemy_speed():
    global enemy_delay
    remaining_enemies = len(enemies)

    if remaining_enemies > 40:
        enemy_delay = 0.02
    elif remaining_enemies > 30:
        enemy_delay = 0.015
    elif remaining_enemies > 20:
        enemy_delay = 0.011
    elif remaining_enemies > 10:
        enemy_delay = 0.006
    elif remaining_enemies > 1:
        enemy_delay = 0.003
    else: 
        enemy_delay = 0.001

# Main game loop
game_over = False
last_shot_time = time.time()  # Timer to control alien shooting

while not game_over:
    wn.update()
    
    # Update player position based on movement direction
    update_player_position()

    # Move player bullets
    for bullet in bullets:
        bullet.move()

    # Move alien bullets
    for bullet in alien_bullets:
        bullet.move()

        # Check for collision with player
        if is_collision(bullet, player):
            bullet.hideturtle()
            bullet.active = False
            player.hideturtle()  # Hide the player
            game_over = True
            display_message("GAME OVER")
            break

    if game_over:
        break

    # Fire bullets from random aliens every 4 seconds
    current_time = time.time()
    if current_time - last_shot_time >= 4:  # Fire bullets every 4 seconds
        alien_fire_bullet()
        last_shot_time = current_time
    
    adjust_enemy_speed()

    # Move enemies
    all_enemies_reversed = False
    for enemy in enemies:
        enemy.move(enemy_dx, 0)

        # Reverse direction and move down if hitting the boundary
        if enemy.xcor() > 280 or enemy.xcor() < -280:
            all_enemies_reversed = True

        # Check for collision with player
        if is_collision(player, enemy):
            game_over = True
            display_message("GAME OVER")
            break

    if game_over:
        break

    if all_enemies_reversed:
        enemy_dx *= -1
        for enemy in enemies:
            enemy.move(0, -enemy_dy)
            if enemy.ycor() < -250:  # Check if enemies reach player
                game_over = True
                display_message("GAME OVER")
                break

    if game_over:
        break

    # Check for bullet collisions with enemies
    for bullet in bullets:
        if bullet.active:
            for enemy in enemies:
                if is_collision(bullet, enemy):
                    bullet.hideturtle()
                    bullet.active = False
                    enemy.hideturtle()
                    enemies.remove(enemy)
                    score
                    score += 10
                    update_score()
                    play_sound_in_thread()
                    break

    # Check if all enemies are eliminated
    if not enemies:
        display_message("YOU WON!")
        game_over = True

    time.sleep(enemy_delay)