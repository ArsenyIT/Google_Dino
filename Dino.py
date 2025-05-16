#Импорт Библиотек----------------------------------------------------------------------------------
import pygame
pygame.init()
from random import randint, choice
import pickle
#Создание Окна-------------------------------------------------------------------------------------
Width, Height = 1000, 400
FPS = 60

window = pygame.display.set_mode((Width, Height))
clock = pygame.time.Clock()
#Сохранение Очков----------------------------------------------------------------------------------
def scoreSave():
    global scoresbest
    if scores > scoresbest:
        f = open('scores.dat', 'wb')
        pickle.dump(scores, f)
        f.close()
        scoresbest = scores
#Загрузка Очков------------------------------------------------------------------------------------
def scoresLoad():
    global scoresbest
    try:
        f = open('scores.dat', 'rb')
        scoresbest = pickle.load(f)
        f.close()
    except:
        pass
#Картинки------------------------------------------------------------------------------------------
imgSprites = pygame.image.load('resours/sprites.png').convert_alpha()
imgBG = imgSprites.subsurface(2, 104, 2400, 26)
imgDinoStand = [imgSprites.subsurface(1514, 2, 88, 94), imgSprites.subsurface(1602, 2, 88, 94)]
imgDinoSit = [imgSprites.subsurface(1866, 36, 118, 60), imgSprites.subsurface(1984, 36, 118, 60)]
imgDinoLose = [imgSprites.subsurface(1690, 2, 88, 94)]
imgCactus = [imgSprites.subsurface(446, 2, 34, 70), imgSprites.subsurface(480, 2, 68, 70),
             imgSprites.subsurface(512, 2, 102, 70), imgSprites.subsurface(512, 2, 68, 70),
             imgSprites.subsurface(612, 2, 50, 100), imgSprites.subsurface(712, 2, 98, 100),
             imgSprites.subsurface(850, 2, 102, 100)]
imgPter= [imgSprites.subsurface(260, 0, 92, 82), imgSprites.subsurface(352, 0, 92, 82)]
imgRestart = imgSprites.subsurface(2, 2, 72, 64)
#Файлы Звуков--------------------------------------------------------------------------------------
sndJump = pygame.mixer.Sound('resours/jump.wav')
sndLevelup = pygame.mixer.Sound('resours/levelup.wav')
sndGameOver = pygame.mixer.Sound('resours/gameover.wav')
#Переменные----------------------------------------------------------------------------------------
fontScores = pygame.font.Font(None, 30)
fontMenu = pygame.font.Font(None, 50)
fontMenuSelect = pygame.font.Font(None, 60)
py, sy = 380, 0
isStand = False
speed = 10
frame = 0
bgs = [pygame.Rect(0, Height - 50, 2400, 26)]
objects = []
timer = 0
scores = 0
scoresbest = 0
level = 0
time = 0
#Класс Объектов------------------------------------------------------------------------------------              items = ['Играть','','Настройки','Разработчики','','Выход']          select = 0
class Obj:
    def __init__(self):
        objects.append(self)

        if randint(0, 4) == 0 and scores > 500:
            self.image = imgPter
            self.speed = 3
            py = Height - 30 - randint(0, 2) * 50
        else:
            self.image = [choice(imgCactus)]
            self.speed = 0
            py = Height - 20

        self.rect = self.image[0].get_rect(bottomleft = (Width, py))
        self.frame = 0
#Обновление Объектов-------------------------------------------------------------------------------
    def update(self):
        global speed, timer, sy
        self.rect.x -= speed + self.speed
        self.frame = (self.frame + 0.1) % len(self.image)

        if self.rect.colliderect(dinoRect) and speed != 0:
            speed = 0
            timer = 60
            sy = -10
            sndGameOver.play()
#Функция Удаления Объектов-------------------------------------------------------------------------
        if self.rect.right < 0:
            objects.remove(self)
#Отрисовка Объектов--------------------------------------------------------------------------------
    def draw(self):
        window.blit(self.image[int(self.frame)], self.rect)
#Начало игры---------------------------------------------------------------------------------------
scoresLoad()
play = True
#Функция Закрытия Окна-----------------------------------------------------------------------------
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
#Клавиши Действий Персонажа------------------------------------------------------------------------
    keys = pygame.key.get_pressed()
    b1, b2, b3 = pygame.mouse.get_pressed()
    pressJump = keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP] or b1
    pressSit = keys[pygame.K_LCTRL] or keys[pygame.K_s] or keys[pygame.K_DOWN] or b3
#Функция Перезапуска Игры--------------------------------------------------------------------------
    if (pressJump or pressSit) and speed == 0 and timer == 0:
        scoreSave()
        py, sy = 380, 0
        isStand = False
        speed = 10
        frame = 0
        objects = []
        scores = 0
#Прыжок Персонажа----------------------------------------------------------------------------------
    if pressJump and isStand and speed > 0:
        sy = -22
        sndJump.play()
    if isStand:
        frame = (frame + speed / 35) % 2
#Падение Персонажа---------------------------------------------------------------------------------
    py += sy
    sy = (sy + 1) * 0.97

    isStand = False
    if py > Height - 20:
        py, sy, isStand = Height - 20, 0, True

    if speed == 0: dinoImage = imgDinoLose[0]
#Присядь Персонажа---------------------------------------------------------------------------------
    elif pressSit:
        dinoImage = imgDinoSit[int(frame)]
    else:
        dinoImage = imgDinoStand[int(frame)]
#Расположение Картинок-----------------------------------------------------------------------------
    dw, dh = dinoImage.get_width(), dinoImage.get_height()
    dinoRect = pygame.Rect(150, py - dh, dw, dh)
#Цикл Перебирания Списка---------------------------------------------------------------------------
    for i in range(len(bgs)-1, -1, -1):
        bg = bgs [i]
        bg.x -= speed
#Функция Удаления Фона-----------------------------------------------------------------------------
        if bg.right < 0:
            bgs.pop(i)
#Проверка Фона-------------------------------------------------------------------------------------
    if bgs[-1].right < Width:
        bgs.append(pygame.Rect(bgs[-1].right, Height - 50, 2400, 26))
#Цикл обновления объектов--------------------------------------------------------------------------
    for obj in objects:
        obj.update()
#Таймер генерации объектов-------------------------------------------------------------------------
    if timer > 0:
        timer -= 1
    elif speed > 0:
        timer = randint(100, 150)
        Obj()
#Изменение очков-----------------------------------------------------------------------------------
    scores += speed / 50
#Подсчёт Сотен очков-------------------------------------------------------------------------------
    if scores // 100 > level:
        level = scores // 100
        sndLevelup.play()
#Изменение сложности-------------------------------------------------------------------------------
    if speed > 0:
        speed = 10 + scores // 100
#Подсчёт Времени-----------------------------------------------------------------------------------
    time = (time + 0.1) % 512
#Заливка окна и Отображение объектов на окнe-------------------------------------------------------
    d = abs(time - 256)
    window.fill((d * 0.98, d * 0.9, d * 0.99))
    for bg in bgs:
        window.blit(imgBG, bg)
    for obj in objects:
        obj.draw()
    window.blit(dinoImage, dinoRect)
    text = fontScores.render('Очки: ' + str(int(scores)), 1, 'gray')
    window.blit(text, (Width - 150, 10))
    if speed == 0 and timer == 0:
        rect = imgRestart.get_rect(center = (Width // 2, Height // 2))
        window.blit(imgRestart, rect)
    text = fontScores.render('Рекорд: ' + str(int(scoresbest)), 1, 'red')
    window.blit(text, (50, 10))
#Обновление Окна-----------------------------------------------------------------------------------
    pygame.display.update()
    clock.tick(FPS)
#Конец---------------------------------------------------------------------------------------------
scoreSave()
pygame.quit()