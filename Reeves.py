#test Link: https://youtu.be/f0j--Y6G4Fg
#test Link: https://www.youtube.com/watch?v=f0j--Y6G4Fg
#Customs
import pafy
import vlc
import tkinter
import pyautogui
import sys
import os
import time
import requests

#Build the root
root = tkinter.Tk()
width  = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.title("Reeves [Beta]")
root.geometry('800x40')
root.geometry("+%d+%d" % ((width/2)-400, (height-150)))
root.wm_attributes("-topmost", 1)
root.resizable(False, False)

#Url label
linkLabel = tkinter.Label(root, text = "Link:")
linkLabel.place(x=0, y=0, width= 40, height=20)

#Url input field
urlInput = tkinter.Entry(root, bd = 3)
urlInput.place(x=40, y=0, width = 300, height = 20)

#Initialize vlc
media = vlc.MediaPlayer()

#load images for buttons
startImage = tkinter.PhotoImage(file = os.getcwd()+"/Images/play.png")
pauseImage = tkinter.PhotoImage(file = os.getcwd()+"/Images/pause.png")
stopImage = tkinter.PhotoImage(file = os.getcwd()+"/Images/stop.png")
soundImage = tkinter.PhotoImage(file = os.getcwd()+"/Images/sound.png")
fullImage = tkinter.PhotoImage(file = os.getcwd()+"/Images/full.png")
windowImage = tkinter.PhotoImage(file = os.getcwd()+"/Images/windowed.png")

#Initialize array containing values from text file
userDecision = True
result = dict()
def loadFile(unsliced):
    global state
    if os.path.exists(os.getcwd()+"/Censcript/" + unsliced.strip("https://www.youtube.com/watch?v=") + ".txt"):
        path = open(os.getcwd()+"/Censcript/" + unsliced.strip("https://www.youtube.com/watch?v=") + ".txt")
        with path as file:
            for line in file:
                a, b = line.split(",")
                result[float(a)] = float(b.strip("\n"))
    else:
        ask = messagebox.askyesno("Reeves","No local file found. Check the GitHub Repository?")
        if ask == True:
            req = requests.get("https://raw.githubusercontent.com/nsenecal/Reeves/master/VideoCollection/"+ unsliced.strip("https://www.youtube.com/watch?v=") + ".txt")
            if req.status_code == 200:
                filename = os.path.join(os.getcwd()+"/Censcript/", unsliced.strip("https://www.youtube.com/watch?v=") + ".txt")
                f = open(filename, 'w')
                f.write(req.text)
                f = open(filename, 'r')
                with f as file:
                    for line in file:
                        a, b = line.split(",")
                        result[float(a)] = float(b.strip("\n"))
            else:
                censorState = False
                ask = messagebox.askyesno("Reeves","No File Found. Play Anyway?")
                if ask == False:
                    userDecision = False
                else:
                    userDecision = True

        else:
            messagebox.askyesno("Reeves", "Censoring Disabled. Play Anyway?")
            censorState = False
            if ask == True:
                userDecision = True
            else:
                userDecision = False

#Initialize identifier variables
currentVideo = None
state = False
moment = None
endGame = None
iteration = 0

#When button is pressed
def playBack():
    global state
    global media
    global userDecision
    if state == False:
        global currentVideo
        if urlInput.get().find("https://www.youtube.com/watch?v=") or urlInput.get().find("https://youtu.be/"):
            if currentVideo == urlInput.get():
                global moment
                global endGame
                global censorState
                if enforcedMute == True:
                    moment = media.get_time()/1000
                media.play()
                state = True
            elif currentVideo != urlInput.get():
                media.stop()
                dict.clear(result)
                video = pafy.new(urlInput.get())
                best = video.getbest()
                media = vlc.MediaPlayer(best.url)
                currentVideo = urlInput.get()
                state = True
                global iteration
                iteration = 0
                moment = None
                loadFile(urlInput.get())
                if userDecision == True:
                    media.play()
                    media.set_fullscreen(screenSize)
                    start.config(image = pauseImage)
                else:
                    currentVideo = None
                    urlInput.delete(0,tkinter.END)
        else:
            print("Unable to open link")
            urlInput.delete(0,tkinter.END)
    elif state == True and media.is_playing():
        if enforcedMute == True:
            endGame -= ((media.get_time()/1000)-moment)
        media.pause()
        start.config(image = startImage)
        state = False

#change screen size
screenSize = False
def alterSize():
    global screenSize
    if screenSize == False:
        screenSize = True
        screenButton.config(image = fullImage)
    else:
        screenSize = False
        screenButton.config(image = windowImage)
    if state == True:
        media.set_fullscreen(screenSize)

#Stop button function
def stop():
    global state
    global currentVideo
    start.config(image = startImage)
    media.stop()
    urlInput.delete(0,tkinter.END)
    mediaSlider.set(0)
    currentVideo = None
    state = False

#Adjust sound when slider is changed
enforcedMute = False
def sound(self):
    if enforcedMute != True:
        media.audio_set_volume(volumeSlider.get())

#Scrubbing
scrubbing = False
videoLength = 0
def scrub(self):
    if media.get_length() > 0:
        media.set_time(int(videoLength*(mediaSlider.get())/root.winfo_width()))

def startScrub(self):
    if media.is_playing():
        scrubbing = True
        mediaSlider.config(command=scrub)

def stopScrub(self):
    if media.is_playing():
        mediaSlider.config(command=focusOff)
        scrubbing = False
        for i in range(0, len(result)+1):
            if list(result)[i] > (media.get_time()/1000):
                global iteration
                iteration = i
                moment = None
                break

def focusOff(self):
    return

censorState = True
from tkinter import messagebox
def censor():
    global censorState
    if censorState == True:
        confirm = messagebox.askyesno("Reeves","Disable Censoring?")
        if confirm == True:
            censorState = False
    else:
            censorState = True

#Start button
start = tkinter.Button(root, image = startImage, command = playBack)
start.place(x=380,y=0,height = 20,width = 20)
stop = tkinter.Button(root, image = stopImage, command = stop)
stop.place(x=400,y=0,height = 20,width = 20)
volumeLabel = tkinter.Label(root, image = soundImage)
volumeLabel.place(x=550, y=0, width=20, height=20)

#Fullscreen buttons
screenButton = tkinter.Button(root, image = windowImage, command = alterSize)
screenButton.place(x=780, y=0,height = 20,width = 20)

#Toggles censor system
delet = tkinter.Button(root, command = censor)
delet.place(x=460, y=0, height = 20, width = 70)

#Volume slider
volumeSlider = tkinter.Scale(root, showvalue = 0, length=200, from_=0, to=100, orient=tkinter.HORIZONTAL, command = sound)
volumeSlider.place(x=570, y=0)
volumeSlider.set(50) #Set position to half so it matches initial volume
media.audio_set_volume(50) #Set volume to half

#scrubber
mediaSlider = tkinter.Scale(root, bd = 0, showvalue = 0, length=795, from_=0, to=795, orient=tkinter.HORIZONTAL, command = focusOff)
mediaSlider.place(x=0, y=20)
mediaSlider.set(0)
mediaSlider.bind("<Button-1>", startScrub)
mediaSlider.bind("<ButtonRelease-1>", stopScrub)

previousVolume = None
#Oh boy, a loop
while True:
    #Checks if media is playing
    if len(result) > 0:
        if media.is_playing() == 1 and censorState == True:
            currentTime = media.get_time()/1000
            if scrubbing == False and len(result) != iteration:
                if (currentTime >= (list(result)[iteration])):
                    if moment == None:
                        previousVolume = media.audio_get_volume()
                        media.audio_set_volume(0)
                        enforcedMute = True
                        moment = currentTime
                        endGame = result[list(result)[iteration]]
                    elif moment != None and (currentTime - moment) >= endGame:
                        enforcedMute = False
                        iteration += 1
                        moment = None
                        endGame = None
                        media.audio_set_volume(previousVolume)

    #Check Mouse Position
    x, y = pyautogui.position()
    if y >= root.winfo_y()-20 and y <= root.winfo_y()+root.winfo_height()+40 and x >= root.winfo_x()-20 and x <= root.winfo_x()+root.winfo_width()+20:
        root.attributes('-alpha', 1)
        root.update()
    elif y > root.winfo_y()-20 or y < root.winfo_y()+root.winfo_height()+40:
        root.attributes('-alpha', 0)
        root.update()

    if censorState == True:
        delet.config(text = "Censoring", bg = "Green")
    else:
        delet.config(text = "Uncensored", bg = "Red")

    #Stream takes time to send the length over, so we wait until it's not a nil value
    if media.get_length() > 0:
        videoLength = media.get_length()
        if scrubbing == False:
            mediaSlider.set((media.get_time()/videoLength)*root.winfo_width())
    #prevents loop from imploding
    time.sleep(0.01)

root.mainloop()
