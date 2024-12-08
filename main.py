import turtle
import math
import time
import random
import wave


# Screen setup
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders with Images")
wn.tracer(0)

# Register images
wn.register_shape("alien.gif") 
wn.register_shape("player.gif") 


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
