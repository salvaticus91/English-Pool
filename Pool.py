import pygame
import numpy as np

# colours
red = (255,0,0)
green = (54,89,74)
seagreen = (46,139,87)
yellow =(255,255,49)
cyan= (26,161,170)
brown = (128,0,0)
white = (255,255,255)
black = (0,0,0)



def cart2pol(z): # Convert from cartesian to polar
    x, y = z
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y,x)
    return(r,theta)

def pol2cart(r,theta): # Convert from polar to cartesian
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return((x,y))

def minus(x,y):
    return (x[0]-y[0],x[1]-y[1])

def add(x,y):
    return (x[0]+y[0],x[1]+y[1])

def multiply(x,y):
    return (x[0]*y[0],x[1]*y[1])

class ball: # a ball's velocity will always be a cartesian (cos pixels ain't polar)
    def check_collision(self): # Checks table cushion collision
        # if hit top or bottom
        edge = gametable.rail_size+gametable.cushion_size
        if (self.pos[1] <= edge) or (self.pos[1] >= gametable.table_size[1]-edge):
            self.velocity = (self.velocity[0],-self.velocity[1])
        # if hit right or left
        elif (self.pos[0] <= edge) or (self.pos[0] >= gametable.table_size[0]-edge):
            self.velocity = (-self.velocity[0],self.velocity[1])
    def decelerate(self):
        # v = u + at, if a is -ve, i.e. deceleration, v = u-at
        # if t=1, then v = un-a
        speed, angle = cart2pol(self.velocity)
        global deceleration
        if speed > deceleration:
            self.velocity=pol2cart(speed-deceleration,angle)
            #print(speed)
        elif speed <= deceleration:
            self.velocity=(0,0)
    def update_display(self):
        self.check_collision()
        self.decelerate()
        self.pos = tuple(map(sum,zip(self.pos,self.velocity)))
        pygame.draw.circle(gameDisplay,self.colour,self.pos,self.size/2)
    def __init__(self,colour,pos,size): # I need to pass the ball object the colour, position and size of the ball
        self.velocity = (0,0)
        self.pos = pos
        self.colour = colour
        self.size = size

class cueball(ball):
    def update_display(self):
        super().update_display()
        if self.velocity != (0,0):
            self.i += 1
            #print(self.pos)
            #print(self.i)
    def __init__(self,pos):
        self.i = 0
        super().__init__(white,pos,10*15/8)
        

class objectball(ball):
    def __init__(self,pos):
        self.colour = red
        super().__init__(self.colour,pos,size=20)
        


class cuestick: # I don't need to worry about this until I have the cueball working. 
    def update_display(self):
        self.curr_pos = pygame.mouse.get_pos() # mouse position
        if self.aiming:
            self.power = 0
            _, self.angle = cart2pol(minus(self.curr_pos,gamecueball.pos))
        elif not self.aiming:
            self.power, _ = cart2pol(minus(self.curr_pos,self.mouse_down))
        self.power += gamecueball.size
        self.cue_tip = add(pol2cart(self.power,self.angle),gamecueball.pos)
        self.cue_butt = add(pol2cart(self.power+self.cue_length,self.angle),gamecueball.pos)
        if self.visible == True:
            pygame.draw.line(gameDisplay,black,self.cue_tip,self.cue_butt,5)
        if gamecueball.velocity != (0,0):
            self.visible = False
        if gamecueball.velocity == (0,0):
            self.visible = True

    def __init__(self):
        self.visible = True # cue visible when all balls velocity == 0
        self.aiming = True
        self.cue_length = 200
        self.power = 0
        self.angle = 0

class table:
    def drawTable(self):
        gameDisplay.fill(self.cloth_colour) # Draw the cloth
        self.drawRails()        # draw rails
        self.drawPockets()      # draw pockets
        self.drawCushions()     # draw cushions
        self.drawGuides()

    def drawRails(self):
        # TL2TR
        pygame.draw.rect(gameDisplay,brown,(0,0,self.table_size[0],self.rail_size))
        # TR2BR
        pygame.draw.rect(gameDisplay,brown,(self.table_size[0]-self.rail_size,0,self.table_size[0],self.table_size[1]))
        # BL2BR
        pygame.draw.rect(gameDisplay,brown,(0,self.table_size[1]-self.rail_size,self.table_size[0],self.table_size[1]))
        # TL2BL
        pygame.draw.rect(gameDisplay,brown,(0,0,self.rail_size,self.table_size[1]))

    def drawPockets(self):
        size = 20
        for x in [self.rail_size,self.table_size[0]/2,self.table_size[0]-self.rail_size]:
            for y in [self.rail_size,self.table_size[1]-self.rail_size]:
                pygame.draw.circle(gameDisplay,black,(x,y),size)

    def drawCushions(self):
        # There are 6 cushions, I need to define some variables to accurately state where they are:
        xmin = self.rail_size + self.cushion_size
        x = [xmin,xmin+self.cushion_size,self.table_size[0]/2-self.cushion_size,self.table_size[0]/2-2*self.cushion_size]
        y = [self.rail_size,xmin]
        # Top cushions
        for i in range(2):
            for j in range(2):
                x = self.table_size[0]-x
                path = [(x[0],y[0]),(x[1],y[1]),(x[3],y[1]),(x[2],y[0])]
                pygame.draw.polygon(gameDisplay,seagreen,path)
            y = self.table_size[1]-y
        # Left and Right cushion
        x = [self.rail_size,xmin]
        y = [xmin,xmin+self.cushion_size,self.table_size[1]-xmin,self.table_size[1]-xmin-self.cushion_size]
        for j in range(2):
            x = self.table_size[0]-x
            path = [(x[0],y[0]),(x[1],y[1]),(x[1],y[3]),(x[0],y[2])]
            pygame.draw.polygon(gameDisplay,seagreen,path)

    def drawGuides(self): # Middle line, diagonal guides and the baulk rectangle
        # Edge size
        edge_size = self.rail_size + self.cushion_size

        # Baulk line
        baulk_loc = self.rail_size+self.table_size[0]/5
        baulk1 = (baulk_loc,edge_size)
        baulk2 = (baulk_loc,self.table_size[1]-edge_size)
        pygame.draw.line(gameDisplay,self.line_colour,baulk1,baulk2)

        # Baulk Arc
        baulk_dia = self.table_size[1]/3
        baulk_pos = baulk_loc-baulk_dia/2
        baulk_rect = (baulk_pos,baulk_dia,baulk_dia,baulk_dia)
        pygame.draw.arc(gameDisplay,self.line_colour,baulk_rect,PI/2,-PI/2)
        
        guides_test = False        
        if guides_test == True:
            pygame.draw.rect(gameDisplay,self.line_colour,baulk_rect,2)

            # X diagonals
            pygame.draw.line(gameDisplay,self.line_colour,(self.table_size[0]/2,self.rail_size),(self.table_size[0]-self.rail_size,self.table_size[1]-self.rail_size)) # x diagonal one
            pygame.draw.line(gameDisplay,self.line_colour,(self.table_size[0]-self.rail_size,self.rail_size),(self.table_size[0]/2,self.table_size[1]-self.rail_size)) # x diagonal two

            # Middle line
            mid_loc = self.table_size[0]/2
            mid1 = (mid_loc,edge_size)
            mid2 = (mid_loc,self.table_size[1]-edge_size)
            pygame.draw.line(gameDisplay,self.line_colour,mid1,mid2)


    def update_display(self): # Create table cloth, baulk line and D
        self.drawTable()

    def __init__(self,size=(7*12*10,4*12*10),rail=40,cloth_colour=green,line_colour=white):
        # Make sure the only thing here is instantiating attributes
        self.cloth_colour = cloth_colour
        self.line_colour = line_colour
        self.table_size = np.array(size)
        self.rail_size = rail
        self.cushion_size = 20
        #self.rackup()

class vector:
    def __init__():
        pass

def resolve(velocity,transfer):
    # velocity = r, a
    # transfer = r,a
    # x = r
    # y = r
    angle = velocity[1]-transfer[1]
    if np.abs(angle) > PI/2:
        print("ERROR")
        if angle > 0:
            angle += PI/2
        else:
            angle -= PI/2
    print(angle)
    x = velocity[0]*np.sin(angle)
    y = velocity[0]*np.cos(angle)
    return x, y


def checkCollision(): # Collision checking, might need a better algorithm
    for each in gameballs:
        for other in gameballs:
            if each != other:
                ratio = minus(each.pos,other.pos) # from each to other
                transfer = cart2pol(ratio) # the distance and angle between two objects
                if transfer[0]<ball_size:
                    # convert vectors from cartesian to polar
                    each_pol = cart2pol(each.velocity)
                    other_pol = cart2pol(other.velocity)
                    # resolve velocities along the transfer line
                    x1,y1 = resolve(each_pol,transfer)
                    x2,y2 = resolve(other_pol,transfer)
                    x = x1+x2 # if +ve, then other goes x magnitude
                    if x>0:
                        # each has transferred energy to other
                        each.velocity = pol2cart(y1,transfer[1])
                        r = np.sqrt(x**2+y2**2)
                        a = np.arctan2(x,y2)
                        other.velocity = pol2cart(r,a)
                        #print("This has angle: ",a)
                    else:
                        # other has transferred energy to each
                        other.velocity = pol2cart(y2,transfer[1])
                        r = np.sqrt(x**2+y1**2)
                        a = np.arctan2(x,y2)
                        each.velocity = pol2cart(r,a)
                        #print("aThis has angle: ",a)


#def rackup():
#    for col in range(5):
#        xpos = col*np.sqrt(ball_size**2-(ball_size/2)**2)+(3/4)*WIDTH-2*np.sqrt((ball_size**2-(ball_size/2)**2))
#        for j in range(col+1):
#            ypos = ball_size*j-col*(ball_size/2)+HEIGHT/2
#            gameobjectballs.append(objectball((xpos,ypos)))
#    yellows = [2,3,7,9,10,12,13]
#    for i in yellows:
#        gameobjectballs[i].colour = yellow
#        gameobjectballs[4].colour = black

HEIGHT = 480
WIDTH = 840

PI = 3.142 # I should probably just use numpy, but will leave here until I get the classes working alright

pygame.init() # not actually sure what this does exactly
gameDisplay = pygame.display.set_mode([840,480])
pygame.display.set_caption('Pool Game')

clock = pygame.time.Clock()

# Initialise
deceleration = 0.001
power_factor = 10*deceleration
gametable = table()
gamecueball = cueball((210,250)) # This is the first place the cueball is put, but this can be changed later. 
gamecuestick = cuestick()

gameobjectball = objectball((500,250))

# I just want to create and display the rack. 
#gameobjectballs = []
ball_size = 20


gameballs = []
gameballs.append(gameobjectball)
gameballs.append(gamecueball)

RUNNING = True
while RUNNING: # Game Loop
	
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # If player clicks close window button
            RUNNING = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gamecuestick.mouse_down = event.pos # the position of the mouse down
        elif event.type == pygame.MOUSEBUTTONUP:
            gamecueball.velocity = pol2cart(-gamecuestick.power*power_factor,gamecuestick.angle)
        if pygame.mouse.get_pressed() == (True,False,False): # while mouse down
            gamecuestick.aiming = False # if true freezes aim (i.e. angle)
        elif pygame.mouse.get_pressed() == (False,False,False): # while mouse up
            gamecuestick.aiming = True # if true freezes aim (i.e. angle)

    gametable.update_display()
    gamecueball.update_display()
    gamecuestick.update_display()
#    for i in gameobjectballs:
#        i.update_display()
    gameobjectball.update_display()
    
    checkCollision()
    
    #clock.tick()

    pygame.display.flip()
pygame.quit()
