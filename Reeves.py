#test Link: https://youtu.be/f0j--Y6G4Fg https://www.youtube.com/watch?v=f0j--Y6G4Fg
#Customs
import pafy
import vlc
import tkinter
import pyautogui
import sys
import os
import time

#Build the root
root = tkinter.Tk()
root.overrideredirect(1)
width  = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry('1120x40')
root.geometry(f"+400+{height-150}")
root.config(background="gray")
root.wm_attributes("-topmost", 1)
root.attributes('-alpha', 0.4)

#Program Label
name = tkinter.Label(root, text = "Reeves [BETA]")
name.place(x=0, y=0, width= 1120, height=20)

#Url label
linkLabel = tkinter.Label(root, text = "Link:")
linkLabel.place(x=0, y=20, width= 50, height=20)

#Url input field
urlInput = tkinter.Entry(root, bd = 0)
urlInput.place(x=50, y=20, width = 490, height = 20)

#Initialize vlc
media = vlc.MediaPlayer()

#load images for buttons
startImage = tkinter.PhotoImage(file = "play.png")
pauseImage = tkinter.PhotoImage(file = "pause.png")
stopImage = tkinter.PhotoImage(file = "stop.png")

#Initialize array containing values from text file
iteration = 0
result = dict()
def loadFile(unsliced):
    with open(os.getcwd()+"/Censcript/" + unsliced.strip("https://www.youtube.com/watch?v=") + ".txt") as file:
        for line in file:
            a, b = line.split(",")
            result[float(a)] = float(b.strip("\n"))

#Initialize identifier variables
currentVideo = ""
state = False
moment = None
endGame = None

#When button is pressed
def playBack():
    global state
    global media
    if state == False:
        global currentVideo
        if urlInput.get().find("https://www.youtube.com/watch?v=") or urlInput.get().find("https://youtu.be/"):
            if currentVideo == urlInput.get():
                global moment
                global endGame
                if mute == True:
                    moment = media.get_time()/1000
                media.play()
                state = True
            elif currentVideo != urlInput.get():
                if media.is_playing() == 1:
                    media.stop()
                video = pafy.new(urlInput.get())
                best = video.getbest()
                media = vlc.MediaPlayer(best.url)
                currentVideo = urlInput.get()
                state = True
                global iteration
                iteration = 0
                moment = None
                loadFile(urlInput.get())
                media.play()
                media.set_fullscreen(screenSize)
            start.config(image = pauseImage)
        else:
            print("Unable to open link")
            urlInput.delete(0,tkinter.END)
    elif state == True:
        if mute == True:
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
        screenButton.config(text = "F")
    else:
        screenSize = False
        screenButton.config(text = "S")
    if state == True:
        media.set_fullscreen(screenSize)

#Exit button function
def exit():
    root.destroy()
    sys.exit("Program was terminated")

#Stop button function
def stop():
    start.config(image = startImage)
    media.stop()
    global iteration
    iteration = 0
    dict.clear(result)
    urlInput.delete(0,tkinter.END)
    mediaSlider.set(0)

#Adjust sound when slider is changed
mute = False
def sound(self):
    if mute != True:
        media.audio_set_volume(volumeSlider.get())

#Scrubbing
scrubbing = False
videoLength = 0
def scrub(self):
    if media.get_length() > 0:
        media.set_time(int(videoLength*(mediaSlider.get())/200))

def startScrub(self):
    scrubbing = True
    mediaSlider.config(command=scrub)

def stopScrub(self):
    mediaSlider.config(command=focusOff)
    scrubbing = False
    for i in range(0, len(result)+1):
        if list(result)[i] > (media.get_time()/1000):
            global iteration
            iteration = i
            moment = None
            break

def focusOff(self):
    print()

#Start button
start = tkinter.Button(root, image = startImage, command = playBack)
start.place(x=540,y=20,height = 20,width = 20)
stop = tkinter.Button(root, image = stopImage, command = stop)
stop.place(x=560,y=20,height = 20,width = 20)

#Exit button
terminate = tkinter.Button(root, text = "X", bg = "red", command = exit)
terminate.place(x=1100,y=0,height = 20,width = 20)

#Fullscreen buttons
screenButton = tkinter.Button(root, text = "S", bg = "purple", command = alterSize)
screenButton.place(x=1100,y=20,height = 20,width = 20)

#Volume slider
volumeLabel = tkinter.Label(root, text = "Volume:")
volumeLabel.place(x=580, y=20, width= 50, height=20)
volumeSlider = tkinter.Scale(root, showvalue = 0, length=100, from_=0, to=100, orient=tkinter.HORIZONTAL, command = sound)
volumeSlider.place(x=630, y=20)
volumeSlider.set(50) #Set position to half so it matches initial volume
media.audio_set_volume(50) #Set volume to half

#scrubber
mediaSlider = tkinter.Scale(root, showvalue = 0, length=200, from_=0, to=200, orient=tkinter.HORIZONTAL, command = focusOff)
mediaSlider.place(x=730, y=20)
mediaSlider.set(0)
mediaSlider.bind("<Button-1>", startScrub)
mediaSlider.bind("<ButtonRelease-1>", stopScrub)

previousVolume = None
#Oh boy, a loop
while True:
    #Checks if media is playing
    if media.is_playing() == 1:
        currentTime = media.get_time()/1000
        if scrubbing == False:
            if len(result) != iteration:
                if (currentTime >= (list(result)[iteration])):
                    if moment == None:
                        previousVolume = media.audio_get_volume()
                        media.audio_set_volume(0)
                        mute = True
                        moment = currentTime
                        endGame = result[list(result)[iteration]]
                    elif moment != None and (currentTime - moment) >= endGame:
                        mute = False
                        iteration += 1
                        moment = None
                        endGame = None
                        media.audio_set_volume(previousVolume)

    #Check Mouse Position
    x, y = pyautogui.position()
    if y >= (height-190) and y <= (height-90) and x >= 0 and x <= width:
        root.deiconify()
        root.update()
    elif y > (height-190) or y < (height-90):
        root.withdraw()
        root.update()
    #prevents loop from imploding
    if media.get_length() > 0: #Stream takes time to send the length over, so we wait until it's not a nil value
        videoLength = media.get_length()
        if scrubbing == False:
            mediaSlider.set((media.get_time()/videoLength)*200)
    time.sleep(0.01)

root.mainloop()
