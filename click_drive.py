import pygame
import csv
from pygame.locals import *
pygame.init()
pygame.mouse.set_visible(1)
# Infinite Recharge Field .jpg is originally 1346x709 pixels
# Add 200x200 for potential controls / status areas
size = width, height = (1546, 909)
gameBackground = pygame.image.load("InfiniteRechargeField.png")
# Astro icon is 65x65 so offsets to plot should be 1/2 that 32x32
astroMav = pygame.image.load("astroMavTrans65x65.png")
astroOffset = astroOffsetX, astroOffsetY = (32, 32)

# Set a screen surface
screen = pygame.display.set_mode(size)
pathColour = (214, 32, 41) # Mavericks colour from the website
buttonFont = pygame.font.SysFont ('Ariel', 35)

# Add a "path" surface that's transparent!
blankSurface = pygame.surface.Surface(size, pygame.SRCALPHA)

# Export coordinates to a .csv file
# The Romi processes point as DriveDistance(0.3, 5_in, drive), TurnDegrees(0.3, 90_deg, drive)
# ...where the first param is directon and speed
# ...and the second param is distance or deg
# ...and the third param is the drive object
#
# Given that the Romi is 6" wide and Astro is 30" wide, a 5:1 field to Romi scale is used
# ...the FRC field is 26'11 1/4" by 52'5 1/4" ...
# ...at 5:1 a scaled Romi field of approx 62.5" by 124.9" is assumed ...
# ...in the x dimention 10.77 pixels per inch and ...
# ...in the y dimention 11.34 pixels per inch will serve as conversion factors.
# i.e. a shift from (100, 100) to (208, 100) represents 10" of travel
# i.e. a shift from (100, 100) to (100, 213) represents 10" of travel

commandQueue = list()
clock = pygame.time.Clock()

def moveAstro(astroSurface, astroPosition, speed):
   currentPosition = astroPosition
   astroX, astroY = astroPosition
   if type(commandQueue[0]) != int:
      targetX, targetY = commandQueue[0][0][0], commandQueue[0][0][1]
      if type(targetX) == int:
         if (abs(targetX - astroX) < 1) and (abs(targetY - astroY) < 1):
            if len(commandQueue[0]) == 1:
               # Knowing the first path has only 1 point left, drop the first path
               commandQueue.pop(0)
            else:
               # Drop the first two points from the first path only
               commandQueue[0].pop(0)
            return astroSurface, astroPosition
         else:
            # Direction component to determine is Astro is going up / down / right / left.
            directionX, directionY = 1, 1
            if astroX > targetX:
               directionX = -1
            if astroY > targetY:
               directionY = -1
            # Slope component determines Y speed scaling factor per 1 X speed.
            scaleX, scaleY = 1, 1
            # If the X delta is greater than the Y delta, scale X to serve Y = 1
            # If the Y delta is greater than the X delta, scale Y to serve X = 1
            if abs(astroX - targetX) < abs(astroY - targetY):
               scaleX = abs(astroX - targetX) * (1 / abs(astroY - targetY))
               scaleY = 1
            else:
               scaleX = 1
               scaleY = abs(astroY - targetY) * (1 / abs(astroX - targetX))
            # Work out relative increment / step size for next tick
            if abs(astroX - targetX) < speed:
               incrementX = abs(astroX - targetX) * scaleX
            else:
               incrementX = speed * scaleX
            if abs(astroY - targetY) < speed:
               incrementY = abs(astroY - targetY) * scaleY
            else:
               incrementY = speed * scaleY      
            # Update surface and return newPos to update main game loop
            newPos = (round(astroX + (incrementX * directionX)), round(astroY + (incrementY * directionY)))
            astroSurface = blankSurface.copy()
            astroSurface.blit(astroMav, (newPos[0] - astroOffsetX, newPos[1] - astroOffsetY))
            return astroSurface, newPos

def romiAngle(romiPosition):
   currentPosition = romiPosition
   romiX, romiY = romiPosition
   if type(commandQueue[0]) != int:
      targetX, targetY = commandQueue[0][0][0], commandQueue[0][0][1]
      print ("Romi is at (", romiX, ", ", romiY, ") heading to (", targetX, ", ", targetY, ")")
   

def main():
   pathSurface = blankSurface.copy()
   astroPosition = (1240, 235)
   astroSurface = pygame.surface.Surface(size, pygame.SRCALPHA)
   astroSurface.blit (astroMav, (astroPosition[0] - astroOffsetX, astroPosition[1] - astroOffsetY))
   commandQueue.append ([astroPosition])
   pathArray = list()
   lastPos = (0,0)
   pos = (0,0)
   # Set the path names and values of the QuickPath buttons
   # Gather Pieces From Home
   textButton1 = buttonFont.render ('Home Gather', True, pathColour)
   pygame.draw.rect (screen, (240, 240, 240), [1351, 5, 190, 40])
   screen.blit (textButton1, (1356, 10))
   # Run Through the Trench and Shoot Three Times
   textButton2 = buttonFont.render ('Trench Shoot', True, pathColour)
   pygame.draw.rect (screen, (240, 240, 240), [1351, 50, 190, 40])
   screen.blit (textButton2, (1356, 60))
   # Setup at the top of the trench
   textButton3 = buttonFont.render ('Trench Entry', True, pathColour)
   pygame.draw.rect (screen, (240, 240, 240), [1351, 95, 190, 40])
   screen.blit (textButton3, (1356, 105))
      
   while True:
      # Set fixed paths assigned to game buttons
      quickPath1 = [(1240, 235)]
      quickPath2 = [(868, 95), (487, 92), (487, 92), (487, 92), (487, 92)]
      quickPath3 = [(870, 95)]
      
      for event in pygame.event.get():
            if pos != (0,0):
               lastPos = pos
            if event.type == QUIT:
               pygame.quit()
               return
            elif event.type == MOUSEBUTTONDOWN:
               if event.button == 1:  #1 is left click : ADD POSITION to the operator path plan
                  # Left Click - gather mouse click position
                  pos = pygame.mouse.get_pos()
                  if pos[0]<1346 and pos[1]<709: # A click on the game board is a path point
                     # Repeated clicks are a "fast shot" control method
                     if pos == lastPos:
                        pygame.draw.circle(pathSurface, (0, 0, 255), pos, 5)
                        print("Add Fast Shot to Path")
                        pathArray.append(pos) # sequences of duplicate points represent SHOTs.
                     else:
                        pygame.draw.circle(pathSurface, pathColour, pos, 5)
                        print("Added path point ", pos)
                        pathArray.append(pos)
                  elif pos[0]>1346 and pos[1]<=40:
                     # Quick Path Button #1 clicked, get it to the commandQueue!
                     commandQueue.append (quickPath1)
                     print ("Added Quick Path #1 'Home Gather' to commandQueue ", commandQueue)
                  elif pos[0]>1346 and pos[1]<=90:
                     # Quick Path Button #2 clicked, get it to the commandQueue!
                     commandQueue.append (quickPath2)
                     print ("Added Quick Path #2 'Trench Shoot' to commandQueue ", commandQueue)
                  elif pos[0]>1346 and pos[1]<=140:
                     # Quick Path Button #2 clicked, get it to the commandQueue!
                     commandQueue.append (quickPath3)
                     print ("Added Quick Path #3 'Trench Entry' to commandQueue ", commandQueue)
                  else:
                     print("Left click outside of field ", pos)
               elif event.button == 2: #2 is middle click : ADD SHOT to the operator path plan
                  pygame.draw.circle(pathSurface, (0, 0, 255), pos, 5)
                  print("Add Shot to Path")
                  pathArray.append(pos) # sequences of duplicate points represent SHOTs.
               elif event.button == 3: #3 is right click : COMMIT the path to run
                  if len(pathArray) > 0:
                     # Do something to COMMIT THE PATH to the commandQueue and reset the pathArray
                     commandQueue.append (pathArray)
                     print ("Added Operator Path to commandQueue ", commandQueue)
                     pathArray = list()
                     pathSurface = blankSurface.copy()
            
      if len(pathArray) > 1:
          for segment in range(0,len(pathArray)-1):
              pygame.draw.line(pathSurface, pathColour, pathArray[segment], pathArray[segment+1])
          
      if len(commandQueue) > 0:
         romiAngle(astroPosition)
         astroSurface, astroPosition = moveAstro(astroSurface, astroPosition, 10)
         
                             
      screen.blit (gameBackground,[0,0])
      screen.blit (pathSurface, [0,0])
      screen.blit (astroSurface, [0,0])
      pygame.display.flip()
      clock.tick(60)

# Execute game:
main()
