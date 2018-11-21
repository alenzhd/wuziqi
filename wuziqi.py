#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#wuziqi.py
#Author:fengqi

from graphics import *
import time
###
num = [[0 for a in range(16)] for a in range(16)]
dx = [1,1,0,-1,-1,-1,0,1] #x,y方向向量
dy = [0,1,1,1,0,-1,-1,-1]
is_end = False
go_first = 1 #先手标志
start = 1 #轮换下棋标志
ai = 1 #AI下棋标志
L1_max=-100000 #剪枝阈值
L2_min=100000
list=[] #保存已画棋子
RESTART_FLAG = False
QUIT_FLAG = False
###
win = GraphWin("五子棋",550,451)
aiFirst = Text(Point(500,100),"")
manFirst = Text(Point(500,140),"")
notice = Text(Point(500,290),"") #提示轮到谁落子
notice.setFill('red')
last_ai = Text(Point(500,330),"") #AI最后落子点
last_man = Text(Point(500,370),"") #玩家最后落子点
QUIT = Text(Point(500,20),"退出")
QUIT.setFill('red')
RESTART = Text(Point(500,60),"重玩")
RESTART.setFill('red')
#数据初始化，把棋盘上的棋子和提示清空
def init():
    global is_end,start,go_first,RESTART_FLAG
    is_end=False
    start=1
    go_first=1
    RESTART_FLAG=False
    QUIT_FLAG=False
    for i in range(16):
        for j in range(16):
            if(num[i][j]!=0):
                num[i][j]=0
    for i in range(len(list)):
        list[-1].undraw()
        list.pop(-1)
    aiFirst.setText("AI 先手")
    manFirst.setText("我先手")
    notice.setText("")
    last_ai.setText("")
    last_man.setText("")
#画棋盘
def drawWin():
    win.setBackground('yellow')
    for i in range(0,451,30):
        line=Line(Point(i,0),Point(i,450))
        line.draw(win)
    for j in range(0,451,30):
        line=Line(Point(0,j),Point(450,j))
        line.draw(win)
    Rectangle(Point(460,5),Point(540,35)).draw(win)
    Rectangle(Point(460,45),Point(540,75)).draw(win)
    Rectangle(Point(460,85),Point(540,115)).draw(win)
    Rectangle(Point(460,125),Point(540,155)).draw(win)
    Rectangle(Point(452,275),Point(548,305)).draw(win)
    Rectangle(Point(452,307),Point(548,395)).draw(win)
    aiFirst.draw(win)
    manFirst.draw(win)
    notice.draw(win)
    last_ai.draw(win)
    last_man.draw(win)
    QUIT.draw(win)
    RESTART.draw(win)
#判断该点是否在棋盘范围内
def inBoard(x,y):
    if(x>=0 and x<=15 and y>=0 and y<=15): return True
    else: return False
#判断该点是否可落子，即是否在棋盘内且没有落子
def downOk(x,y):
    if(inBoard(x,y) and num[x][y]==0): return True
    else: return False
#该点值是否和i值相等，即该点棋子颜色和i相同
def sameColor(x,y,i):
    if(inBoard(x,y) and num[x][y]==i): return True
    else: return False
#在给定的方向v(v区分正负)上，和该点同色棋子的个数
def numInline(x,y,v):
    i=x+dx[v]; j=y+dy[v]
    s=0; ref=num[x][y]
    if(ref==0): return 0
    while(sameColor(i,j,ref)):
        s=s+1; i=i+dx[v]; j=j+dy[v]
    return s
#该点四个方向里(即v不区分正负)，活四局势的个数
def liveFour(x,y):
    key=num[x][y]; s=0
    for u in range(4):
        samekey=1
        samekey,i=numofSamekey(x,y,u,1,key,samekey)
        if(not downOk(x+dx[u]*i,y+dy[u]*i)):
            continue
        samekey,i=numofSamekey(x,y,u,-1,key,samekey)
        if(not downOk(x+dx[u]*i,y+dy[u]*i)):
            continue
        if(samekey==4):
            s=s+1
    return s
#该点八个方向里(即v区分正负)，冲四局势的个数
def chongFour(x,y):
    key=num[x][y]; s=0
    for u in range(8):
        samekey=0; flag=True; i=1
        while(sameColor(x+dx[u]*i,y+dy[u]*i,key) or flag):
            if(not sameColor(x+dx[u]*i,y+dy[u]*i,key)):
                if(flag and inBoard(x+dx[u]*i,y+dy[u]*i) and num[x+dx[u]*i][y+dy[u]*i]!=0):
                    samekey-=10
                flag=False
            samekey+=1
            i+=1
        i-=1
        if(not inBoard(x+dx[u]*i,y+dy[u]*i)):
            continue
        samekey,i=numofSamekey(x,y,u,-1,key,samekey)
        if(samekey==4):
            s+=1
    return s-liveFour(x,y)*2
#该点四个方向里活三，以及八个方向里断三的个数
def liveThree(x,y):
    key=num[x][y]; s=0
    for u in range(4):
        samekey=1
        samekey,i=numofSamekey(x,y,u,1,key,samekey)
        if(not downOk(x+dx[u]*i,y+dy[u]*i)):
            continue
        if(not downOk(x+dx[u]*(i+1),y+dy[u]*(i+1))):
            continue
        samekey,i=numofSamekey(x,y,u,-1,key,samekey)
        if(not downOk(x+dx[u]*i,y+dy[u]*i)):
            continue
        if(not downOk(x+dx[u]*(i-1),y+dy[u]*(i-1))):
            continue
        if(samekey==3):
            s+=1
    for u in range(8):
        samekey=0; flag=True; i=1
        while(sameColor(x+dx[u]*i,y+dy[u]*i,key) or flag):
            if(not sameColor(x+dx[u]*i,y+dy[u]*i,key)):
                if(flag and inBoard(x+dx[u]*i,y+dy[u]*i) and num[x+dx[u]*i][y+dy[u]*i]!=0):
                    samekey-=10
                flag=False
            samekey+=1
            i+=1
        if(not downOk(x+dx[u]*i,y+dy[u]*i)):
            continue
        if(inBoard(x+dx[u]*(i-1),y+dy[u]*(i-1)) and num[x+dx[u]*(i-1)][y+dy[u]*(i-1)]==0):
            continue
        samekey,i=numofSamekey(x,y,u,1,key,samekey)
        if(not downOk(x+dx[u]*i,y+dy[u]*i)):
            continue
        if(samekey==3):
            s+=1
    return s
#该点在四个方向里，是否有六子或以上连线
def overLine(x,y):
    flag=False
    for u in range(4):
        if((numInline(x,y,u)+numInline(x,y,u+4))>4):
            flag=True
    return flag
#该黑子点是否是禁手点，黑子禁手直接判输
def ban(x,y):
    if(sameColor(x,y,3-go_first)):
        return False
    flag=((liveThree(x,y)>1) or (overLine(x,y)) or ((liveFour(x,y)+chongFour(x,y))>1))
    return flag
#统计在u方向上，和key值相同的点的个数，即和key同色的连子个数
def numofSamekey(x,y,u,i,key,sk):
    if(i==1):
        while(sameColor(x+dx[u]*i,y+dy[u]*i,key)):
            sk+=1
            i+=1
    elif(i==-1):
        while(sameColor(x+dx[u]*i,y+dy[u]*i,key)):
            sk+=1
            i-=1
    return sk,i
#游戏是否结束，如果有五子连线或出现禁手
def gameOver(x,y):
    global is_end
    for u in range(4):
        if((numInline(x,y,u)+numInline(x,y,u+4))>=4):
            is_end=True
            return True
    return False
#对该点落子后的局势进行估分
def getScore(x,y):
    global is_end
    if(ban(x,y)):
        return 0
    if(gameOver(x,y)):
        is_end=False
        return 10000
    score=liveFour(x,y)*1000+(chongFour(x,y)+liveThree(x,y))*100
    for u in range(8):
        if(inBoard(x+dx[u],y+dy[u]) and num[x+dx[u]][y+dy[u]]!=0):
            score=score+1
    return score
#博弈树第一层
def AI1():
    global L1_max
    L1_max=-100000
    if(num[8][8]==0 and go_first==ai):
        return go(8,8)
    keyi=-1; keyj=-1
    for x in [8,7,9,6,10,5,11,4,12,3,13,2,14,1,15,0]:
        for y in [8,7,9,6,10,5,11,4,12,3,13,2,14,1,15,0]:
            if(not downOk(x,y)):
                continue
            num[x][y]=ai
            tempp=getScore(x,y)
            if(tempp==0):
                num[x][y]=0; continue
            if(tempp==10000):
                return go(x,y)
            tempp=AI2()
            num[x][y]=0
            if(tempp>L1_max): #取极大
                L1_max=tempp; keyi=x; keyj=y
    go(keyi,keyj)
#博弈树第二层
def AI2():
    global L2_min
    L2_min=100000
    for x in [8,7,9,6,10,5,11,4,12,3,13,2,14,1,15,0]:
        for y in [8,7,9,6,10,5,11,4,12,3,13,2,14,1,15,0]:
            if(not downOk(x,y)):
                continue
            num[x][y]=3-ai
            tempp=getScore(x,y)
            if(tempp==0):
                num[x][y]=0; continue
            if(tempp==10000):
                num[x][y]=0; return -10000
            tempp=AI3(tempp)
            if(tempp<L1_max): #L1层剪枝
                num[x][y]=0; return -10000
            num[x][y]=0
            if(tempp<L2_min): #取极小
                L2_min=tempp
    return L2_min
#博弈树第三层
def AI3(p2):
    keyp=-100000
    for x in [8,7,9,6,10,5,11,4,12,3,13,2,14,1,15,0]:
        for y in [8,7,9,6,10,5,11,4,12,3,13,2,14,1,15,0]:
            if(not downOk(x,y)):
                continue
            num[x][y]=ai
            tempp=getScore(x,y)
            if(tempp==0):
                num[x][y]=0; continue
            if(tempp==10000):
                num[x][y]=0; return 10000
            if(tempp-p2*2>L2_min): #L2层剪枝
                num[x][y]=0; return 10000
            num[x][y]=0
            if(tempp-p2*2>keyp): #取极大
                keyp=tempp-p2*2
    return keyp
#选手下棋
def manPlay():
    p=win.getMouse()
    if(Restart(p) or Quit(p)): return
    x=round(p.getX()/30)
    y=round(p.getY()/30)
    if(downOk(x,y)): go(x,y)
    else: manPlay()
#落下一子并且判断游戏是否结束
def go(x,y):
    global is_end
    c=Circle(Point(x*30,y*30),13)
    if(start==ai):
        num[x][y]=ai
        last_ai.setText("AI 落子:\n(x:y)=("+str(x)+":"+str(y)+")")
        if(go_first==ai): c.setFill('black')
        else: c.setFill('white')
    else:
        num[x][y]=3-ai
        last_man.setText("玩家落子:\n(x:y)=("+str(x)+":"+str(y)+")")
        if(go_first==ai): c.setFill('white')
        else: c.setFill('black')
    c.draw(win)
    list.append(c)
    if(ban(x,y)):
        if(start==ai):
            notice.setText("AI 禁手,玩家赢!\n点击重玩")
        else:
            notice.setText("玩家禁手,AI 赢!\n点击重玩")
        is_end=True
    elif(gameOver(x,y)):
        if(start==ai):
            notice.setText("AI 赢!\n点击重玩")
        else:
            notice.setText("玩家赢!\n点击重玩")
##是否重新开始游戏
def Restart(p):
    global RESTART_FLAG
    x=p.getX(); y=p.getY()
    if((abs(500-x)<40) and (abs(60-y)<15)): #restart
        init()
        RESTART_FLAG=True
        notice.setText("重新开始")
        time.sleep(1)
        return True
    else:
        return False
##是否退出游戏
def Quit(p):
    global QUIT_FLAG, is_end
    x=p.getX(); y=p.getY()
    if((abs(500-x)<40) and (abs(20-y)<15)): #quit
        init()
        QUIT_FLAG=True
        is_end=True
        notice.setText("退出")
        time.sleep(1)
        return True
    else:
        return False
##选择先后手
def whoStart(p):
    global start, go_first
    x=p.getX(); y=p.getY()
    if((abs(500-x)<40) and (abs(100-y)<15)): #AI 先手
        start=1
        go_first=1
        aiFirst.setText("AI 执黑")
        manFirst.setText("玩家执白")
        return True
    elif((abs(500-x)<40) and (abs(140-y)<15)): #玩家先手
        start=2
        go_first=2
        aiFirst.setText("AI 执白")
        manFirst.setText("玩家执黑")
        return True
    else:
        return False
##------------------------------------------------------------------##
#主程序入口
if __name__=='__main__':
    init()
    drawWin()
    notice.setText("请选择先手")
    p=win.getMouse()
    while(not whoStart(p) and not Quit(p)):
        p=win.getMouse()
    while(not is_end):
        RESTART_FLAG=False
        if(start==ai):
            notice.setText("AI 正在下棋...")
            AI1()
        else:
            notice.setText("请你下棋...")
            manPlay()
        start=3-start
        if(RESTART_FLAG):
            notice.setText("请选择先手")
            p=win.getMouse()
            while(not whoStart(p) and not Quit(p)):
                p=win.getMouse()
        elif(not QUIT_FLAG and is_end):
            p=win.getMouse()
            while(not Restart(p) and not Quit(p)):
                p=win.getMouse()
            if(RESTART_FLAG):
                notice.setText("请选择先手")
                p=win.getMouse()
                while(not whoStart(p) and not Quit(p)):
                    p=win.getMouse()