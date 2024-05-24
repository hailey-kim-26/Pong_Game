#pong_game.py

import turtle as t
import time

# CONSTANTS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_SPEED = 30
BALL_SPEED_X = 0.1
BALL_SPEED_Y = -0.1
SCORE_FONT = ("Arial", 20, "normal")
SCORE_POS = (0, 260)
PAUSED = False

# record scores of paddle A and B
scoreA = 0
scoreB = 0

#  create a window
window = t.Screen()
window.title("Pong Game")
window.bgcolor("black")
window.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
window.tracer(0)

# create paddles A and B
def create_paddle(x, y):
    paddle = t.Turtle()
    paddle.speed(0)
    paddle.shape("square")
    paddle.color("white")
    paddle.shapesize(stretch_wid=PADDLE_HEIGHT/20, stretch_len=PADDLE_WIDTH/20)
    paddle.penup()
    paddle.goto(x, y)
    return paddle

paddle_A = create_paddle(-350, 0)
paddle_B = create_paddle(350, 0)

# create a ball
ball = t.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = BALL_SPEED_X
ball.dy = BALL_SPEED_Y

# update the score
display_score = t.Turtle()
display_score.speed(0)
display_score.color("white")
display_score.penup()
display_score.hideturtle()
display_score.goto(*SCORE_POS)
display_score.write("Player A: 0 Player B: 0", align="center", font=SCORE_FONT)

# function to update score
def update_score():
    display_score.clear()
    display_score.write("Player A: {} Player B: {}".format(scoreA, scoreB), align="center", font=SCORE_FONT)

# move paddles
def move_paddle_up(paddle):
    y = paddle.ycor() + PADDLE_SPEED
    if y + PADDLE_HEIGHT/2 < SCREEN_HEIGHT/2:
        paddle.sety(y)

def move_paddle_down(paddle):
    y = paddle.ycor() - PADDLE_SPEED
    if y - PADDLE_HEIGHT/2 > -SCREEN_HEIGHT/2:
        paddle.sety(y)

# pause the game
def toggle_pause():
    global PAUSED
    PAUSED = not PAUSED

# keyboard bindings
window.listen()
window.onkeypress(lambda: move_paddle_up(paddle_A), "w")
window.onkeypress(lambda: move_paddle_down(paddle_A), "s")
window.onkeypress(lambda: move_paddle_up(paddle_B), "Up")
window.onkeypress(lambda: move_paddle_down(paddle_B), "Down")
window.onkeypress(toggle_pause, "Escape")


# function to detect collision
def is_collision(paddle, ball):
    return (paddle.xcor() - PADDLE_WIDTH/2 < ball.xcor() < paddle.xcor() + PADDLE_WIDTH/2
            and paddle.ycor() - PADDLE_HEIGHT/2 < ball.ycor() < paddle.ycor() + PADDLE_HEIGHT/2)

# Main game loop
while True:
    window.update()

    # move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # check border
    if ball.ycor() > SCREEN_HEIGHT/2-20 or ball.ycor() < -SCREEN_HEIGHT/2+20:
        ball.dy *= -1

    # paddle and ball collisions
    if is_collision(paddle_A, ball) or is_collision(paddle_B, ball):
        ball.dx *= -1

    # pause the game if press 'esc'
    if PAUSED:
        time.sleep(0.1)
        continue

    # score updates and game reset
    if ball.xcor() > SCREEN_WIDTH/2:
        scoreA += 1
        update_score()
        ball.dx *= -1
    elif ball.xcor() < -SCREEN_WIDTH/2:
        scoreB += 1
        update_score()
        ball.dx *= -1