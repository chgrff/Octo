'''
PC08

AUTHORS: Christopher Griffin and Maria Theresa Villatoro
DATE: November 4th, 2022


DESCRIPTION:
Octo, the hungry octopus, moves accross the screen (Arrow Keys and W/A/S/D) to 'eat' green squares. When the octopus collides 
with the squares they disappear. The user has 30 seconds before the window closes and their time is up. Collecting all 5 randomly placed
squares means Victory!

GOAL: Collect all green squares before time runs out!
'''
#Start Stuff
import pygame,random
pygame.init()

#Create a window
w = 500
h = 500
win = pygame.display.set_mode((w, h))

#global varaiables
x=w/2
y=h/2
step=10
Counter = 0

#set colors
green=(100,200,30) #color for squares
fontColor=(255,255,255) #FontColor white

font = pygame.font.SysFont('Arial Black', 30)
bigfont = pygame.font.SysFont('Arial Black', 75)

#Dr.Z's OOP Repository 35 & 36
bckgnd = pygame.image.load("Ocean.jpg").convert()
bckgnd = pygame.transform.scale(bckgnd,(w,h)) 

#Loads Player image
octopus = pygame.image.load('player.png')


#Our player
class Player:
    def __init__(self):
    
      self.bw = 30 # box width
      self.bh = 30 # box height
      self.x = w/2
      self.y = h/2  #stuck in the middle
    
      self.rect=pygame.Rect(self.x,self.y,40,40) 

    def draw(self):
        win.blit(octopus,(self.x, self.y)) #blit octo to the same coord as our rect

    def movement(self):                                                        
        """"Allows for movement with Arrow keys and W/A/S/D, Harvested from PCO7"""
        global step
        self.rect=pygame.Rect(self.x,self.y,30,30)
        #Arrow down and 'S' move surface down
        if event.type == pygame.KEYDOWN:
            if event.key == (pygame.K_DOWN):
                self.y+=step
            elif  event.key == (pygame.K_s):
                self.y+=step
        #Arrow up and 'W' move surface up
            elif event.key == (pygame.K_UP):
                self.y-=step
            elif event.key == (pygame.K_w):
                self.y-=step
        #Arrow left and 'A' move surface left
            elif event.key == (pygame.K_LEFT):
                self.x-=step
            elif event.key == (pygame.K_a):
               self.x-=step
        #Arrow right and 'D' move surface right
            elif event.key == (pygame.K_RIGHT):
                self.x+=step
            elif event.key == (pygame.K_d):
                self.x+=step
    
    # Handles screen wrapping along the Y - Axis 
    def Ywrap(self,h):
        """if on top move to bottom and vise versa, Started in PC06, modified for PC07, moves up to PC08"""
        if (self.y>h):
            self.y=0
        elif (self.y<0):
           self.y=h
        return self.y

    # Handles screen wrapping along the X - Axis 
    def Xwrap(self,w):
        """if on left move to right and vise versa, Started in PC06, modified for PC07, moves up to PC08"""
        if (self.x>w):
            self.x=0
        elif (self.x<0):
            self.x=w
        return self.x

# The green squares
class Edibles:
    def __init__(self,x,y):
        self.bw = 10 # box width
        self.bh = 10 # box height

        #place these food items randomly on the screen
        self.x = random.randint(100,450)
        self.y = random.randint(100,450) 

        self.box = pygame.Rect(self.x,self.y,self.bw,self.bh)  #Define space
        self.face = pygame.Surface((self.bw,self.bh)) #create surface to fill
        self.face.fill(green) #fill surface

        self.draw=True #draw yourself Bool toggle

    '''Dr.Z's OOP Repository lines 122-133'''
    def show(self):
        if (self.draw):
            # only draw when self.draw is "on" (True)
            win.blit(self.face,(self.x,self.y))

    def collide(self,rect):
        if (self.draw):
                # Only collide if drawing is on
                if self.box.colliderect(rect):
                    print("yum") #reference to know if collision happens
                    self.draw = False # turn off drawing
                     
                    #counts when there is a collision between Octo and the Edibles
                    global Counter
                    Counter = Counter+1 
                    return Counter

        #When we count (5) collisions, display that you have won the game
        if (Counter == 5):
            Winfont = pygame.font.SysFont('Arial Black', 100)
            win.blit(Winfont.render("Winner!", True, (fontColor)), (50, 175))
            #pygame.quit()
        
    
'''Dr.Z's OOP Repoitory lines 151-162'''
class Timer:
    def __init__(self,limit=30):
        self.limit = limit
        self.clock = pygame.time.Clock()
        self.start=  pygame.time.get_ticks() # get starter tick at Timer instantiation
        self.timeLeft = self.countDown()
        
    def countDown(self):
        '''Note: Will count down based on time passed, not frame rate, or call frequency.
        Retuurns whole value time in seconds (int)'''
        currTime=(self.start + pygame.time.get_ticks())/1000 #calculate how many seconds
        return int(self.limit + - currTime) # returns whole second numbers

#Make (5) edibles in the Edible List 
EdibleList=[]
for edible in range(5):
    EdibleList.append(Edibles(x,y))

#Animation Controls
running=True
clock = pygame.time.Clock()
timer=Timer()
Octo=Player()

while running:
    
    win.blit(bckgnd,(0,0)) #updates background image

    for edible in EdibleList:
        edible.show()
    
    for edible in EdibleList:
        edible.collide(Octo.rect)
    
    for event in pygame.event.get():
        # Events (Octo's Movement) 
        Octo.movement()
        y=Octo.Ywrap(h)
        x=Octo.Xwrap(w)
        
        if event.type == pygame.QUIT: 
             running = False
    
    #Draw Octo to the screen
    Octo.draw()

    #Timer on screen
    Time=str(timer.countDown())
    win.blit(font.render(Time, True, (fontColor)), (400, 30))
    
    #Score Countdown on screen 
    scoredisplay=str(5-Counter)
    win.blit(font.render(scoredisplay, True, (fontColor)), (50, 30))
    
    #When 30 seconds has passed close the window and print Time's Up! 
    if (timer.countDown()==0):
        pygame.quit()
        print("Time's Up!")
    
    pygame.display.update()
    clock.tick(30)