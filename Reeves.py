#test Link: https://youtu.be/f0j--Y6G4Fg
#test Link: https://www.youtube.com/watch?v=f0j--Y6G4Fg
#Customs
import pafy
import vlc
import tkinter
import pyautogui
import os
import time
import requests
import pynput
from pynput.keyboard import Key, Listener
import urllib.request
from bs4 import BeautifulSoup

#Build the root
root = tkinter.Tk()
width  = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.title("Reeves [Beta]")
root.geometry('600x60')
root.geometry("+%d+%d" % ((width/2)-400, (height-150)))
root.wm_attributes("-topmost", 1)
root.resizable(False, False)

newWindow = tkinter.Toplevel(root)
newWindow.title("Reeves Player")
canvas = tkinter.Canvas(newWindow,bg="black")
canvas.pack(fill=tkinter.BOTH, expand=1)

#Url label
linkLabel = tkinter.Label(root, text = "Link:")
linkLabel.place(x=0, y=0, width= 40, height=20)

#Url input field
urlInput = tkinter.Entry(root, bd = 3)
urlInput.place(x=40, y=0, width = 220, height = 20)

#Initialize vlc
media = vlc.MediaPlayer()

#load images for buttons
startImage = tkinter.PhotoImage(file = os.getcwd()+"/Images/play.png")
pauseImage = tkinter.PhotoImage(file = os.getcwd()+"/Images/pause.png")
stopImage = tkinter.PhotoImage(file = os.getcwd()+"/Images/stop.png")
soundImage = tkinter.PhotoImage(file = os.getcwd()+"/Images/sound.png")
fullImage = tkinter.PhotoImage(file = os.getcwd()+"/Images/full.png")
windowImage = tkinter.PhotoImage(file = os.getcwd()+"/Images/windowed.png")

frame = tkinter.Frame(root)
frame.place(x = 340, y = 0, width = 300, height = 40)
lb = tkinter.Listbox(frame, width=40, height=1)
lb.pack(side = 'left',fill = 'y' )
scrollbar = tkinter.Scrollbar(frame, orient="vertical",command=lb.yview)
scrollbar.pack(side = "left",fill="y")

def click(self):
    del que[lb.get("active")]
    idx = lb.get(0, tkinter.END).index(lb.get("active"))
    lb.delete(idx)
    print(que)
lb.bind("<Double-1>", click)

que = {}
def search():
    query = urllib.parse.quote(urlInput.get())
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    code = soup.find(attrs={'class':'yt-uix-tile-link'})['href']
    lb.insert(tkinter.END, pafy.new('https://www.youtube.com' +code).title)
    que[pafy.new('https://www.youtube.com' + code).title] = 'https://www.youtube.com' + code
    urlInput.delete(0,tkinter.END)

def playVideo(data):
    global media
    global state
    global iteration
    global currentVideo
    video = pafy.new(data)
    best = video.getbest()
    media = vlc.MediaPlayer(best.url)
    currentVideo = data
    iteration = 0
    moment = None
    h = canvas.winfo_id()
    media.set_hwnd(h)
    media.play()
    newWindow.title(video.title)
    startButton.config(image = pauseImage)
    while media.is_playing() == 0:
        state = False
    state = True

#Initialize array containing values from text file
autoPlay = True
currentVideo = None
result = dict()
def loadFile(unsliced):
    global state
    global currentVideo
    global censorState
    dict.clear(result)
    if censorState == True:
        if os.path.exists(os.getcwd()+"/Censcript/" + unsliced.strip("https://www.youtube.com/watch?v=") + ".txt"):
            path = open(os.getcwd()+"/Censcript/" + unsliced.strip("https://www.youtube.com/watch?v=") + ".txt")
            with path as file:
                for line in file:
                    a, b = line.split(",")
                    result[float(a)] = float(b.strip("\n"))
            playVideo(urlInput.get())
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
                    playVideo(unsliced)
                else:
                    ask = messagebox.askyesno("Reeves","No File Found. Play Anyway?")
                    if ask == True:
                        censorState = False
                        playVideo(unsliced)
                    else:
                        currentVideo = None
            else:
                ask = messagebox.askyesno("Reeves", "Censoring Disabled. Play Anyway?")
                if ask == True:
                    censorState = False
                    playVideo(unsliced)
                else:
                    currentVideo = None

    else:
        playVideo(unsliced)
    urlInput.delete(0,tkinter.END)
#Initialize identifier variables
state = False
moment = None
endGame = None
iteration = 0

#When button is pressed
def playBack():
    global state
    global media
    global currentVideo
    global moment
    global endGame
    if state == False:
        if currentVideo == None:
            if urlInput.get().find("https://www.youtube.com/watch?v=") > -1 or urlInput.get().find("https://youtu.be/") > -1:
                loadFile(urlInput.get())
            elif urlInput.get() != "":
                search()
            elif len(que) > 0:
                loadFile(que[list(que.keys())[0]])
                lb.delete(0)
                del que[list(que.keys())[0]]
        else:
            if urlInput.get() != "":
                search()
            else:
                if enforcedMute == True:
                    moment = media.get_time()/1000
                media.play()
                startButton.config(image = pauseImage)
                state = True
    elif state == True and media.is_playing():
        if urlInput.get() != "":
            search()
        else:
            if enforcedMute == True:
                endGame -= ((media.get_time()/1000)-moment)
            media.pause()
            startButton.config(image = startImage)
            state = False

#Stop button function
def stop():
    global state
    global currentVideo
    global censorState
    global media
    newWindow.title("Reeves Player")
    startButton.config(image = startImage)
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
    print("")

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
startButton = tkinter.Button(root, image = startImage, command = playBack)
startButton.place(x=280,y=0,height = 20,width = 20)
stopButton = tkinter.Button(root, image = stopImage, command = stop)
stopButton.place(x=300,y=0,height = 20,width = 20)
volumeLabel = tkinter.Label(root, image = soundImage)
volumeLabel.place(x=0, y=20, width=40, height=20)

#Toggles censor system
delet = tkinter.Button(root, command = censor)
delet.place(x=280, y=20, height = 20, width = 20)

#Volume slider
volumeSlider = tkinter.Scale(root, showvalue = 0, length=220, from_=0, to=100, orient=tkinter.HORIZONTAL, command = sound)
volumeSlider.place(x=37, y=20)
volumeSlider.set(50) #Set position to half so it matches initial volume
media.audio_set_volume(50) #Set volume to half

#scrubber
mediaSlider = tkinter.Scale(root, bd = 0, showvalue = 0, length=595, from_=0, to=595, orient=tkinter.HORIZONTAL, command = focusOff)
mediaSlider.place(x=0, y=40)
mediaSlider.set(0)
mediaSlider.bind("<Button-1>", startScrub)
mediaSlider.bind("<ButtonRelease-1>", stopScrub)

previousVolume = None

enabled = True
def on_release(key):
    global enabled
    if key == pynput.keyboard.Key.alt_l:
        if enabled == False:
            enabled = True
        else:
            enabled = False
        print(enabled)
listener = pynput.keyboard.Listener(on_release=on_release)
listener.start()

newWindow.protocol('WM_DELETE_WINDOW', focusOff)

def exit():
    os._exit(True)
root.protocol('WM_DELETE_WINDOW', exit)

print("Running")
#Oh boy, a loop
while True:
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
    if (y >= root.winfo_y()-20 and y <= root.winfo_y()+root.winfo_height()+40 and x >= root.winfo_x()-20 and x <= root.winfo_x()+root.winfo_width()+20) and enabled == True:
        root.attributes('-alpha', 1)
        root.lift()
        root.update()
    elif (y > root.winfo_y()-20 or y < root.winfo_y()+root.winfo_height()+40) or enabled == False:
        root.attributes('-alpha', 0)
        root.update()

    if censorState == True:
        delet.config(text = "C", bg = "Green")
    else:
        delet.config(text = "R", bg = "Red")
    #Stream takes time to send the length over, so we wait until it's not a nil value
    if media.get_length() > 0:
        videoLength = media.get_length()
        if scrubbing == False:
            mediaSlider.set((media.get_time()/videoLength)*root.winfo_width())
    if media.is_playing() == 0 and state == True:
        stop()
        if len(que) > 0 and autoPlay == True:
            loadFile(que[list(que.keys())[0]])
            lb.delete(0)
            del que[list(que.keys())[0]]
    #prevents loop from imploding
    time.sleep(0.1)

root.mainloop()
