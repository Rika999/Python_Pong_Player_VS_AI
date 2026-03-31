import turtle
import random

# Screen setup
wn = turtle.Screen()
wn.title("Pong")
wn.bgcolor("black")
wn.setup(width=800, height=650) # Extra height for text
wn.tracer(0)

# Game State
score_a = 0
score_b = 0
best_score = 0
ball_speed = 0.15

# UI Elements
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 250)

def update_ui():
    pen.clear()
    pen.write(f"Player: {score_a}  AI: {score_b}  |  Best: {best_score}\nPress 'Enter' to restart", 
              align="center", font=("Courier", 16, "normal"))

def create_paddle(x):
    p = turtle.Turtle()
    p.speed(0)
    p.shape("square")
    p.color("white")
    p.shapesize(stretch_wid=5, stretch_len=1)
    p.penup()
    p.goto(x, 0)
    return p

paddle_a = create_paddle(-350)
paddle_b = create_paddle(350)

ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.dx = 0
ball.dy = 0

def reset_ball(served_by_ai=True):
    global ball_speed
    ball.goto(0, 0)
    ball_speed = 0.15
    ball.dx = -ball_speed if served_by_ai else ball_speed
    ball.dy = random.uniform(-0.15, 0.15) # Random initial trajectory

# Initial call
reset_ball()
update_ui()

# Movement functions
def paddle_a_up():
    if paddle_a.ycor() < 250:
        paddle_a.sety(paddle_a.ycor() + 40)

def paddle_a_down():
    if paddle_a.ycor() > -250:
        paddle_a.sety(paddle_a.ycor() - 40)

def restart_game():
    global score_a, score_b, best_score
    if score_a > best_score:
        best_score = score_a
    score_a, score_b = 0, 0
    update_ui()
    reset_ball()

# Key bindings
wn.listen()
wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "s")
wn.onkeypress(restart_game, "Return")

# Main Loop
while True:
    wn.update()
    
    # Move ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Basic AI
    if paddle_b.ycor() < ball.ycor() and abs(paddle_b.ycor() - ball.ycor()) > 15:
        paddle_b.sety(paddle_b.ycor() + 0.12)
    elif paddle_b.ycor() > ball.ycor() and abs(paddle_b.ycor() - ball.ycor()) > 15:
        paddle_b.sety(paddle_b.ycor() - 0.12)

    # Top/Bottom collisions
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1
    elif ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    # Scoring
    if ball.xcor() > 390:
        score_a += 1
        update_ui()
        reset_ball(served_by_ai=True)
        
    elif ball.xcor() < -390:
        score_b += 1
        update_ui()
        reset_ball(served_by_ai=False)

    # Paddle collisions
    if (ball.xcor() > 340 and ball.xcor() < 350) and (abs(ball.ycor() - paddle_b.ycor()) < 50):
        ball.setx(340)
        ball_speed += 0.01
        ball.dx = -ball_speed
        
    if (ball.xcor() < -340 and ball.xcor() > -350) and (abs(ball.ycor() - paddle_a.ycor()) < 50):
        ball.setx(-340)
        ball_speed += 0.01
        ball.dx = ball_speed