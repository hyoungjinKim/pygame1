import pygame
import random
###########################################
# 기본 초기화 (반드시 해야 하는 것들)

pygame.init() #초기화

#화면 크기 설정
screen_width=600 #가로
screen_height=800 #세로

screen=pygame.display.set_mode((screen_width,screen_height))

#화면 타이틀 설정
pygame.display.set_caption("hyoung jin game")#게임 이름

#FPS
clock=pygame.time.Clock()
##############################################

#배경 이미지 불러오기
background= pygame.image.load("제목 없음.png")

#캐릭터 불러오기
character=pygame.image.load("캐릭터.png")
character_size=character.get_rect().size#이미지   크기 구하기
character_width=character_size[0]#캐릭터 가로크기
character_height=character_size[1]#캐릭터 세로크기
character_X_pos=(screen_width/2)-(character_width/2) #화면 가로 크기 절반에 위치
character_Y_pos=screen_height-character_height #화면 세로 크기 가장 아래

endimg= pygame.image.load("엔딩.jpg")
#이동할 좌표
to_x=0
to_y=0

#이동 속도
character_speed=0.5


#적 캐릭터

enemy=pygame.image.load('악당.png')
enemy_size=enemy.get_rect().size#이미지 크기 구하기
enemy_width=enemy_size[0]#캐릭터 가로크기
enemy_height=enemy_size[1]#캐릭터 세로크기
enemy_X_pos=random.randint(0,screen_width-enemy_width)#랜덤 가로 위치
enemy_Y_pos=0 #화면 세로 크기 가장 아래
enemy_speed=5
enemys=[]





#아이템
item=pygame.image.load('아이템.png')
item_size=item.get_rect().size
item_width=item_size[0]
item_height=item_size[1]
item_X_pos=random.randint(0,screen_width-item_width)
item_Y_pos=screen_height-item_height
items=[]

item_to_remove=-1
#스코어
score=0

# 폰트 정의
game_font=pygame.font.Font(None, 40) #폰트 객체 생성 (폰트, 크기)
Win_font=pygame.font.Font(None,100)

#총 시간
total_time=60

#시작 시간
start_ticks=pygame.time.get_ticks()#시작 tick을 받아옴

#배경 음악
bgsound= pygame.mixer.Sound("C:/Users/isacc/Desktop/panggame/배경음악.wav")
bgsound.play(-1)

#이벤트 루프
running = True#게임이 진행 중인가?
while running:
    dt=clock.tick(60)#게임 화면의 초당 프레임 수 설정
    print("FPS:"+str(clock.get_fps()))
     #타이머 집어 넣기
    #경과 시간 계산
    elapsed_time=(pygame.time.get_ticks()-start_ticks)/1000 #경과시간을 초 단위로 표시
    timer =game_font.render(str(int(total_time-elapsed_time)),True,(255,255,255))
    Win = Win_font.render(('Win'),True,(255,255,255))
    for event in pygame.event.get():
        
        if event.type==pygame.QUIT: #창 종료 이벤트 발생 하였는가?
            running=False#게임 진행 중이 아님
        if event.type==pygame.KEYDOWN: #키가 눌러졌는지 확인
            if event.key==pygame.K_LEFT:#캐릭터 왼쪽으로
                to_x-=character_speed
            elif event.key==pygame.K_RIGHT:#캐릭터 오른쪽으로
                to_x+=character_speed
            if character_Y_pos==screen_height-character_height:
                if event.key==pygame.K_UP:#캐릭터 위로
                    to_y-=4
        if event.type==pygame.KEYUP: #방향키를 떼면 멈춤
            if event.key == pygame.K_LEFT or event.key ==pygame.K_RIGHT:
                to_x=0
            elif event.key == pygame.K_UP or event.key ==pygame.K_DOWN:
                to_y=0
    character_X_pos+=to_x*dt
    character_Y_pos+=(to_y *dt)+10




    #가로 경계값 처리
    if character_X_pos<0:
        character_X_pos=0
    elif character_X_pos>screen_width-character_width:
        character_X_pos=screen_width-character_width
    #세로 경계값 처리
    if character_Y_pos<0:
        character_Y_pos=0
        
    elif character_Y_pos>screen_height-character_height:
        character_Y_pos=screen_height-character_height
    
    enemy_Y_pos+= enemy_speed
    
    if enemy_Y_pos > screen_height:
        enemy_Y_pos=0
        enemy_X_pos=random.randint(0,screen_width-enemy_width)
        score+=10
        enemy_speed+=1
    
    #속도 제한
    if enemy_speed>=15:
        enemy_speed=15    
        

        
    #충돌 처리
    character_rect=character.get_rect()
    character_rect.left=character_X_pos
    character_rect.top=character_Y_pos
    
    enemy_rect=enemy.get_rect()
    enemy_rect.left=enemy_X_pos
    enemy_rect.top=enemy_Y_pos
    
    item_rect=item.get_rect()
    item_rect.left=item_X_pos
    item_rect.top=item_Y_pos
    if character_rect.colliderect(item_rect):
        score+=50
        item_X_pos=random.randint(0,screen_width-item_width)
    
    
    #화면 출력
    screen.blit(background,(0,0)) #배경 그리기
    screen.blit(character,(character_X_pos,character_Y_pos))#캐릭터 그리기
    screen.blit(enemy,(enemy_X_pos,enemy_Y_pos))#적그리기
    screen.blit(item,(item_X_pos,item_Y_pos))#아이템 그리기
    

    #충돌 체크
    over=Win_font.render(('GAME OVER'), True, (255,255,255))
    if character_rect.colliderect(enemy_rect):
        screen.blit(endimg,(0,0))
        screen.blit(over,(100,380))
        running=False

    

    score1=game_font.render((("score:")+str(int(score))),True,(255,255,255))
    screen.blit(score1,(10,10))
    #출력할 글자, True,글자 색상
    screen.blit(timer,(560,10))
    if total_time-elapsed_time<=0:
        screen.blit(Win,(230,380))
        running=False


    pygame.display.update()#게임화면 다시 그리기
#잠시 대기
pygame.time.delay(2000)#2초 정도 대기
#pygame 종료
pygame.quit()