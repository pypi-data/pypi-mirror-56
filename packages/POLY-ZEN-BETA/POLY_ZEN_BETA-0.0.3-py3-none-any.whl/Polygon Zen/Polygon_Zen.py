import pygame
import COLLISIONS
import playsound
from random import randint
from math import sin,cos
pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(8)
screenscale = (1200,600)#const screen scale
pygame.display.set_caption('polygon zen')
try:
    pygame.display.set_icon(pygame.image.load('menubg.png'))
except Exception as Exc:
    print(Exc)
def nullf():
    pass
class game:
    class music:
        songs = {'':''
            }
    class sounds:
        dict = {'button':'music//buttonhit.mp3'
            }
    col = 0,0,0 #background constant
    win = pygame.display.set_mode((1200, 600))
    images = [pygame.image.load('menubg.png'),pygame.image.load('harmcube.gif')]
    playerimages = {'front': 'PlayerFRONT.bmp',
                    '2/3':'PlayerHP2.bmp',
                    '1/3':'PlayerHP1.bmp',
                    'fade': 'PlayerFade.png'
        }
    class HARM:
        class cube:
            def __init__(self,x,y,drx='ranangle',dry='ranangle',size=3,list=None,lingers=False,rot=True):
                self.x = x
                self.lingers = lingers
                self.y = y
                self.size = size
                self.rot = rot
                self.deg = 0 
                if 'ranangle' in drx or 'ranangle' in dry:
                    self.ang = True
                    self.random = randint(1,360)
                    self.drx = sin(self.random)
                    self.dry = cos(self.random)
                else:
                    self.random = randint(1,8)
                    self.drx = self.random
                    self.dry = self.random
                    self.ang=False
                    
                self.width = size
                self.height = size
                self.pop = False
                self.cd = self.size + 10
                
                self.image = pygame.transform.scale(pygame.image.load('harmcube.gif'),(self.width,self.height))
                self.imagerot = pygame.transform.rotate(self.image,self.deg)
            def upd(self,win):
                try:
                    pygame.draw.circle(win,(255,255,255),(int(self.x) + round(self.width/2),int(self.y) + round(self.height/2)),self.cd)
                except Exception:
                    pass
                self.deg += 1
                if self.cd >= 0:
                    self.cd -= 1
                if self.deg >= 360:
                    self.deg = 0
                if self.ang:
                    self.x += self.drx
                    self.y -= self.dry
                else:
                    if self.random == 1:
                        self.x -= 1
                    elif self.random == 2:
                        self.x -= 1
                        self.y -= 1
                    elif self.random == 3:
                        self.y -= 1
                    elif self.random == 4:
                        self.y -= 1
                        self.x  += 1
                    elif self.random == 5:
                        self.x += 1
                    elif self.random == 6:
                        self.x += 1
                        self.y  -= 1
                    elif self.random == 7:
                        self.y -= 1
                    elif self.random == 8:
                        self.y -= 1
                        self.x -= 1
                if not self.lingers:
                    if self.x <= 0 or self.x + self.width >= 1200 or self.y <= 0 or self.y + self.height >= 600:
                        self.pop = True
                if not self.rot:
                    win.blit(self.image,(self.x,self.y))
                else:
                    self.imagerot = pygame.transform.rotate(self.image,self.deg)
                    win.blit(self.imagerot,(self.x,self.y))
                
                
    class player:
        def __init__(self,x=600,y=300,win=None,vel=1):
            self.x = x
            self.y = y
            self.width=20
            self.vel = vel
            self.height=20
            self.endimage = pygame.image.load(game.playerimages['fade'])
            self.currentimage = pygame.image.load(game.playerimages['front'])
        def offset(x,y):
            self.x = x
            self.y = y
        def Upd(self,win=None):
            self.k = pygame.key.get_pressed()
            if self.k[pygame.K_LEFT] and self.x >= 0:
                self.x -= self.vel
            elif self.k[pygame.K_RIGHT] and self.x + self.width <= 1200:
                self.x += self.vel
            elif self.k[pygame.K_DOWN] and self.y + self.height <= 600:
                self.y += self.vel
            elif self.k[pygame.K_UP] and self.y >= 0:
                self.y -= self.vel
            win.blit(self.currentimage,(self.x,self.y))
    class text:
        def __init__(self,x,y,text='unset',font='sans',size=30,bold=False,col=(10,40,200)):
            self.x = x
            self.y = y
          
    
            self.textfont = pygame.font.SysFont(font,size,bold)
            self.text = text

            self.render = self.textfont.render(text,size,col)
            
    
        
        def update(self,win):
            win.blit(self.render,(self.x,self.y))
            
        
    class button:
        def __init__(self,x,y,ctp=None,text='unset',width=50,height=30,function=nullf,font='sans',size=30,bold=False,col=(10,40,200)):
            self.x = x
            self.y = y
            self.ctp = ctp
            #self.sound = pygame.mixer.Sound(game.sounds.dict['button'])
            self.sound = 'music//buttonhit.mp3'
            self.textfont = pygame.font.SysFont(font,size,bold)
            self.text = text
            self.width = width
            self.height = height
            self.function = function
            self.clicked = False
            self.delay=10
            self.render = self.textfont.render(text,size,col)
            self.image = pygame.transform.scale(pygame.image.load('button.png'),(self.width,self.height))
            self.image_clicked = pygame.transform.scale(pygame.image.load('button_clicked.png'),(self.width,self.height))
    
        
        def update(self,win):
            
            mx,my = pygame.mouse.get_pos()
            
            if not self.clicked:
                win.blit(self.image,(self.x,self.y))
            else:
                win.blit(self.image_clicked,(self.x,self.y))
            win.blit(self.render,(self.x + 3,self.y))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if mx >= self.x and mx <= self.x + self.width:
                            if my >= self.y and my <= self.y + self.height:
                                #playsound.playsound(self.sound)
                                #self.function()
                                try:
                                    if self.ctp != None:
                                        try:
                                            self.ctp.pause()#set_volume(0)
                                        except Exception as e:
                                            print(e)
                                    playsound.playsound(self.sound)
                                    self.function()
                                    
                                except Exception as e:
                                    print(e)
                               
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
        def default():
            pass
           

    
    class main:
        def menu():
            c1 = pygame.mixer.Channel(0)
            c1.play(pygame.mixer.Sound('music//menu.wav'),loops=-1)
            levels = game.button(90,90,ctp=c1,width=70,text='levels',function=game.levels.levels)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        try:
                            pygame.quit()
                            exit()
                        except Exception:
                            exit()
                
                game.win.fill((game.col))
                
                game.win.blit(game.images[0],(0,0))
                levels.update(game.win)
                pygame.display.update()
            
            


            pass
    class levels:
        def get_pos():
            final = pygame.mixer_music.get_pos()
            return final / 100
        def levels():
            c1 = pygame.mixer.Channel(0)
            c1.play(pygame.mixer.Sound('music//menu.wav'),loops=-1)
            level1 = game.button(90,90,ctp=c1,width=70,text='level 1',function=game.levels.l1)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        try:
                            pygame.quit()
                            exit()
                        except Exception:
                            exit()
                
                game.win.fill((game.col))
                
                game.win.blit(game.images[0],(0,0))
                level1.update(game.win)
                pygame.display.update()

        def l1():
            cubelist = []
            def get_pos():
                return pygame.mixer_music.get_pos() / 1000
            timeb = game.text(90,90,str(get_pos()))#game.button(90,90,width=70,text=game.levels.get_pos())
            for x in range(0,100):
                cubelist.append(game.HARM.cube(90,90,size=10))
            p = game.player(600,300)
            song = pygame.mixer_music.load('music//Danimal_Cannon_and_Zef_-_Logic_Gatekeeper-1426437680.ogg')
            print(game.levels.get_pos())
            pygame.mixer_music.play()
            pygame.display.toggle_fullscreen()
            while True:
                timeb = game.text(90,90,str(get_pos()))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        try:
                            pygame.quit()
                            exit()
                        except Exception:
                            exit()
                game.win.fill((game.col))
                p.Upd(win=game.win)
                timeb.update(game.win)
                for i in cubelist:
                    i.upd(game.win)
                    COLLISIONS.IfCollide(i,p)
                    if i.pop:
                        cubelist.pop(cubelist.index(i))
                    
                    
                pygame.display.update()
            #pass
game.main.menu()
       
