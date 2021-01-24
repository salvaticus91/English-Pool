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

def cart2pol(x): # Convert from cartesian to polar
    rho = np.sqrt(x[0]**2 + x[1]**2)
    phi = np.arctan2(x[1],x[0])
    return(rho,phi)

def pol2cart(rho,phi): # Convert from polar to cartesian
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return((x,y))

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
        # change HEIGHT to self.table_size[1]
        # change WIDTH to self.table_size[1]
        # self.mid = self.table_size[0]/2
        # self.top = self.rail_size 
        # self.table_size[1]-self.rail_size
        # self.table_size[0]-self.rail_size
        baulk_pos = self.table_size[0]/5#-self.cloth_size[1]/6
        baulk_dia = self.table_size[1]/3
        baulk_rect = (baulk_pos,baulk_dia+self.rail_size,baulk_dia,baulk_dia)
        
        pygame.draw.arc(gameDisplay,self.line_colour,baulk_rect,PI/2,-PI/2)        
        pygame.draw.line(gameDisplay,self.line_colour,(self.rail_size+self.table_size[0]/5,0),(self.rail_size+self.table_size[0]/5,self.table_size[1]))
        
        pygame.draw.line(gameDisplay,self.line_colour,(self.table_size[0]/2,self.rail_size),(self.table_size[0]/2,self.table_size[1]-self.rail_size)) # middle line
        pygame.draw.line(gameDisplay,self.line_colour,(self.table_size[0]/2,self.rail_size),(self.table_size[0]-self.rail_size,self.table_size[1]-self.rail_size)) # x diagonal one
        pygame.draw.line(gameDisplay,self.line_colour,(self.table_size[0]-self.rail_size,self.rail_size),(self.table_size[0]/2,self.table_size[1]-self.rail_size)) # x diagonal two
        pygame.draw.rect(gameDisplay,self.line_colour,baulk_rect,2) # baulk rectangle

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

HEIGHT = 480
WIDTH = 840

PI = 3.142 # I should probably just use numpy, but will leave here until I get the classes working alright

pygame.init() # not actually sure what this does exactly
gameDisplay = pygame.display.set_mode([840,480]) # 
pygame.display.set_caption('Pool Game')

clock = pygame.time.Clock()
# Initialise
gametable = table()
running = True
while running: # Game Loop
	# If the player clicks the close window button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
	    running = False
    gametable.update_display()
    #clock.tick()
    pygame.display.flip()
pygame.quit()
