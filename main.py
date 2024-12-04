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