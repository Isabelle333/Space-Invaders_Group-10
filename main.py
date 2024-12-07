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
