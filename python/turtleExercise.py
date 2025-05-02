import turtle as t

# 윈도우 창 셋팅
window = t.Screen()
window.title('거북이로 객체지향 도형 그리기')   # 윈도우 창 제목

# t1 거북이
t1 = t.Turtle()

t1.shape('turtle')  # 거북이 모양 셋팅
t1.home()           # 원점 이동

# t1 거북이 사각형 그리기
for i in range(4) :
    t1.forward(100) # 앞으로 100 이동
    t1.right(90)    # 오른쪽으로 90도 회전


# t2 거북이
t2 = t.Turtle()

t2.shape('turtle')
t2.color('red')     # 펜 색상 설정
t2.pensize(5)       # 펜 굵기 설정

# t2 거북이 특정 위치로 이동 시키기
t2.penup()      # 선 그리지 않는 상태 (원점 이동 후, 그리기)
t2.goto(-100, 100)

# t2 거북이 직사각형 그리기
t2.pendown()    # 선 그리는 상태

for i in range(4) :
    t2.backward(50 if i % 2 == 0 else 100)  # 가로는 50, 세로는 100 이동
    t2.right(90)


# t3 거북이
t3 = t.Turtle()

t3.shape('turtle')
t3.color('blue')
t3.pensize(10)

# t3 거북이 특정 위치로 이동 시키기
t3.penup()
t3.goto(150, 150)

# t3 거북이 삼각형 그리기
t3.pendown()

for i in range(3) :
    t3.forward(50)
    t3.left(120)    # 왼쪽으로 120도 회전


# t4 거북이
t4 = t.Turtle()

t4.shape('turtle')
t4.color('green')
t4.pensize(3)

# t4 거북이 특정 위치로 이동 시키기
t4.penup()
t4.goto(-200, -200)

# t4 거북이 원 그리기
t4.pendown()
t4.circle(30)   # 반지름 30

window.exitonclick()                        # 마우스 클릭 시, 창 닫기