import turtle
import math
import random
import platform
import os

if platform.system() == "Windows":
	try:
		import winsound
		from playsound import playsound
	except:
		print("winsound module not avaliable.")

wn = turtle.Screen()
# wn.setup(width = 1.0, height = 1.0)
wn.bgcolor("black")
wn.title("Space Invaders")
wn.bgpic("dc.png")
wn.tracer(0)

# register the shapes
wn.register_shape("invader.gif")
wn.register_shape("player.gif")
wn.register_shape("r.gif")
#wn.register_shape("giphy.gif")

# move left
def move_left():
	ply.speed = -1

def move_right():
	ply.speed = 1

def move_ply():
	x = ply.xcor()
	x = x + ply.speed

	if x > 280:
		x = 280
	if x < -280:
		x = -280

	ply.setx(x)


def fire_bullet():
	global bulletstate

	if bulletstate == "ready":
		bulletstate = "fire"
		#winsound.PlaySound("laser.wav", winsound.SND_ASYNC)
		play_sound("enm_shot_med.wav")

		#  move bullet above player
		x = ply.xcor()
		y = ply.ycor()
		bullet.setposition(x, y + 5)
		bullet.showturtle()

#  check collision and distance
def isCollision(t1, t2):
	distance = math.sqrt( math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2) )

	if distance < 15:
		return True
	else:
		return False

def play_sound(sound_file, time = 0):
	#if system is Windows
	if platform.system() == "Windows":
		winsound.PlaySound(sound_file, winsound.SND_ASYNC)

    #on Linux
	elif platform.system() == "Linux":
		os.system("aplay -q {}&".format(sound_file))

	#on Mac
	else:
		os.system("afplay {}&".format(sound_file))

	#Repeact time
	if time > 0:
		turtle.ontimer(lambda: play_sound(sound_file, time), t = int(time * 1000) )

# draw border
draw = turtle.Turtle()
draw.hideturtle()
draw.speed(0)
draw.color("white")
draw.penup()
draw.setposition(-300, -300)
draw.pensize(3)
draw.pendown()

for _ in range(4):
	draw.fd(600)
	draw.lt(90)

#add border image
s = turtle.Turtle()
s.shape("r.gif")

# Player turtle
ply = turtle.Turtle()
ply.hideturtle()
ply.color("blue")
ply.shape("player.gif")
ply.penup()
ply.speed(0)
ply.setposition(0, -250)
ply.setheading(90)
ply.showturtle()

ply.speed = 0

# Keyboard bindings
wn.listen()
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")
wn.onkeypress(fire_bullet, "space")

# set score to 0
score = 0

# draw score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring = "Score: {}".format(score)
score_pen.write(scorestring, False, align = "left", font = ("Arial", 14, "normal"))
score_pen.hideturtle()

#write title inside window
title_pen = turtle.Turtle()
title_pen.hideturtle()
title_pen.speed(0)
title_pen.color("cyan")
title_pen.pensize("3")
title_pen.penup()
title_pen.setposition(-100, 330)
title_pen.write("Space Invaders 1.0", False, align = "center", font = ("Arial", 30, "bold"))
title_pen.setposition(250, 330)
title_pen.color("red")
title_pen.write("(By S.Fortune)", False, align = "center", font = ("Arial", 30, "bold"))

number_of_enemies = 30
enemies = []

# Add enemies
for i in range(number_of_enemies):
	enemies.append(turtle.Turtle())

enemy_start_x = -230
enemy_start_y = 250
enemy_number = 0 

# create enemy
for enemy in enemies:
	#enemy.hideturtle()
	enemy.color("red")
	enemy.shape("invader.gif")
	enemy.penup()
	enemy.speed(0)
	x = enemy_start_x + (50 * enemy_number)
	y = enemy_start_y
	enemy.setposition(x, y)

	#update enemy number
	enemy_number += 1
	if enemy_number == 10:
		enemy_start_y -= 50
		enemy_number = 0

enemyspeed = 0.15

# create bullet
bullet = turtle.Turtle()
bullet.hideturtle()
bullet.color("yellow")
bullet.shape("arrow")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(.6, .6)
bullet.setposition(0, -255)

bulletspeed = 4.5

# define bullet state
# ready - ready to fire
# fire - bullet firing

bulletstate = "ready"

play_sound("nik.wav", 0)

# Main game loop
while  True:

	for enemy in enemies:
		# move enemy
		x = enemy.xcor()
		x = x + enemyspeed
		enemy.setx(x)

		# enemy boundary checking
		# move enemy up and down
		#  move all enemies down
		if enemy.xcor() > 280:

			# move all enemies down
			for e in enemies:
				y = e.ycor()
				y -= 40
				e.sety(y)

			# change enemy direction
			enemyspeed = enemyspeed * -1

		if enemy.xcor() < -280:

			# move all enemies down
			for e in enemies:
				y = e.ycor()
				y -= 40
				e.sety(y)
			enemyspeed = enemyspeed * -1

		# check collision between bullet and enemy	
		if isCollision(bullet, enemy):
			#winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
			play_sound("exp_small.wav")

			# reset the bullet
			bullet.hideturtle()  
			bulletstate = "ready"
			bullet.setposition(0, -400)

			# update score
			score += 10
			scorestring = "Score: {}".format(score)
			score_pen.clear()
			score_pen.write(scorestring, False, align = "left", font = ("Arial", 14, "normal"))

			# reset enemy
			enemy.setposition(0, 10000)

		if isCollision(ply, enemy):
			#winsound.PlaySound("exp_user.ogg", winsound.SND_ASYNC)

			ply.hideturtle()
			enemy.hideturtle()
			play_sound("exp_big.wav")
			print("Game Over!")
			break

	# move bullet 
	if bulletstate == "fire":
		y = bullet.ycor()
		y += bulletspeed
		bullet.sety(y)

	# bullet boundary checking
	if bullet.ycor() > 275:
		bullet.hideturtle()
		bulletstate = "ready"

	wn.update()
	move_ply()


wn.mainloop()