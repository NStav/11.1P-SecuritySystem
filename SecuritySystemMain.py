from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import tkinter as tk
from gpiozero import LED
import RPi.GPIO as GPIO
import time
import requests
from auth import authenticate
from imgur_upload import upload_image
import KeyPressTester as key

#creating the window for the GUI
win = tk.Tk()
win.geometry('390x300')
win.title("Security Interface")

#pin set up and variable declaration
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
PIR_PIN = 23
GPIO.setup(PIR_PIN, GPIO.IN)
led = LED(14)
passcode_var=tk.StringVar()
passcode = ""
activated = False
myFont = tk.font.Font(family = 'Helvetica', size = 20, weight = "bold")
subFont = tk.font.Font(family = 'Helvetica', size = 15, weight = "bold")

#button functions
def Submit():
    global passcode
    passcode=passcode_var.get()
    passcode_var.set("")
    
def SetPasscode():
    label = tk.Label(text='Enter numeric passcode below')
    label.grid(row=4, column=1)
    entry = tk.Entry(textvariable = passcode_var)
    entry.grid(row=5, column=1)
    SubmitButton = tk.Button(win, text = "Submit", font = subFont, command = Submit, bg = "bisque2", height = 1, width = 12)
    SubmitButton.grid(row=6, column=1)

def Activate():
    if(passcode.isnumeric() == False or passcode == ""):
        print('Cannot activate as the passcode you set is either empty or not numeric')
    else:
        print('activate')
        global activated
        activated = True
        win.destroy()
    
def close():
    win.destroy()


def Main_Menu():
    PasscodeButton = tk.Button(win, text = "Set Passcode", font = myFont, command = SetPasscode, bg = "bisque2", height = 1, width = 24)
    PasscodeButton.grid(row=0, column=1)

    ActivateButton = tk.Button(win, text = "Activate", font = myFont, command = Activate, bg = "green", height = 1, width = 24)
    ActivateButton.grid(row=1, column=1)
    
    win.protocol("WM_DELETE_WINDOW", close)
    win.mainloop()


Main_Menu()
if(activated == True):
    client = authenticate()
    input_passcode = ""
    key.init()
    led.on()
    
    #to stop the system tiggering on the user when leaving their room after activating the
    #system, it may be commented out as when demonstrating how the system works I don't want'
    # to have to wait for it to activate
    time.sleep(180)
    
    while (input_passcode != passcode):
        key_press = key.numpad_Detection()
        time.sleep(0.15)
        # numpad_Detection checks if a numpad key is being pressed, if so it returns a string
        # version of that number which returned into the variable key_press, thus if test is a
        # string then a keypad number was pressed meaning that following if condition is met
        # and we can add their input key into their current attempt at the passcode.
        if (type(key_press) is str):
            input_passcode += key_press
        # I made the del key return an int instead so that we know if the del key specifically
        # is pressed meaning we should delete their most recent input number.
        if(type(key_press) is int):
            input_passcode = input_passcode[:-1]
        
        if GPIO.input(PIR_PIN):
            #takes photo using raspberry pi webcam and uploads image privately to imgur
            image = upload_image(client)
            #retrieves image link from imgur and sets it as one of the values sent in the IFTTT
            payload = {'value1': image['link']}
            #contacts the IFTT webhook, causing security alert to be sent to phone and
            # triggering an event on the particle argon
	    # dont forget to add webhook key from 11.2P submission
            requests.post('https://maker.ifttt.com/trigger/motion_detected/with/key/*insert webhook key*', data = payload)
            requests.post('https://maker.ifttt.com/trigger/motion_detected_contact_argon/with/key/*insert webhook key*')
            print('IFTTT sent')
            time.sleep(5)
led.off()
GPIO.cleanup()
pygame.quit()
