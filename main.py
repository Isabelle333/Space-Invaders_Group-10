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