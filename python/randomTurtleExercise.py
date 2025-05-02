import turtle, random
from turtle import *

# 윈도우 창 셋팅
window = Screen()
window.title('거북이로 객체지향 사각형 그리기')

# rgb 모드로 변경
turtle.colormode(255)

# 색상 랜덤값 추출 함수
def randomColor() :
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    return (r, g, b)


# 이동 함수
def move(t) :
    width = random.randint(1, 100)
    height = random.randint(1, 100)

    # 사각형 그리기
    for i in range(4) :        
        # 전진
        t.forward(width) if i % 2 else t.forward(height)
        # 우회전
        t.right(90)


# 거북이 생성
tutles = []
for i in range(10) :
    t = turtle.Turtle()
    t.shape('turtle')
    t.penup()

    # 색상 랜덤 선택
    t.color(randomColor())

    # 선 굵기 랜덤 지정
    t.pensize(random.randint(1, 10))

    # 시작 위치 랜덤 지정
    t.goto(random.randint(-300, 300), random.randint(-300, 300))
    tutles.append(t)


# 거북이 이동
for t in tutles :
    t.pendown()
    # 사각형 그리기
    move(t)

window.exitonclick()