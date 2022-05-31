from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import time

#Function to create pygame window, as this needs to be open so we can register keyboard inputs. Pygame was used for this as the python keyboard module can't be 
# imported on the raspberry pi for some reason.
def init():
    pygame.init()
    win = pygame.display.set_mode((50, 50))
    
#Function to get whichever key is being pressed
def getKey(keyName):
    ans = False
    for eve in pygame.event.get():pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(keyName))
    if keyInput [myKey]:
        ans = True
    pygame.display.update()
    return ans

#Function to return the correct number (in string form) when a number on the numPad is pressed.
def numpad_Detection():
    if getKey('KP0'):
        print('key 0 was pressed')
        return '0'
    if getKey('KP1'):
        print('key 1 was pressed')
        return '1'
    if getKey('KP2'):
        print('key 2 was pressed')
        return '2'
    if getKey('KP3'):
        print('key 3 was pressed')
        return '3'
    if getKey('KP4'):
        print('key 4 was pressed')
        return '4'
    if getKey('KP5'):
        print('key 5 was pressed')
        return '5'
    if getKey('KP6'):
        print('key 6 was pressed')
        return '6'
    if getKey('KP7'):
        print('key 7 was pressed')
        return'7'
    if getKey('KP8'):
        print('key 8 was pressed')
        return '8'
    if getKey('KP9'):
        print('key 9 was pressed')
        return '9'
    if getKey('KP_PERIOD'):
        print('delete key was pressed')
        return 1
        
if __name__ == '__main__':
    init()
    while True:
        numpad_Detection()
