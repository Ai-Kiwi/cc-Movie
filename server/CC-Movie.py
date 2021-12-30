UseComplexImage = False
SoundBufferSize = 6
SoundOffset = 0
multiplySound = 1
# please keep in mind sound file must be in dfpwm file format for a converter link cheek out the link below
# music.madefor.cc
SoundInPutFile = ("C:\\Users\\Ai Kiwi\\Desktop\\video-2.dfpwm")
InPutFile = ("C:\\Users\\Ai Kiwi\\Desktop\\video-2.mp4")

SoundInPutFile = ("C:\\Users\\Ai Kiwi\\Desktop\\shrek2.3.dfpwm")
InPutFile = ("C:\\Users\\Ai Kiwi\\Desktop\\shrek2.3.mp4")

SoundInPutFile = ("C:\\Users\\Ai Kiwi\\Desktop\\harry potter audio file\\Harry_Potter_and_the_Philosophers_Stone_2001.dfpwm")
InPutFile = ("C:\\Users\\Ai Kiwi\\Desktop\\formated harry potter\\Harry_Potter_and_the_Philosophers_Stone_2001.mp4")

#multiplySound = multiplySound * (30 / FrameRate)

#open a iamge
#read the image
#convert the image to limited resolution
#find best 4bit colors for the image
#convert the image to 4bit
#save the image



#open the image
#read the image
#convert the image to limited resolution
#find best 4bit colors for the image
#convert the image to 4bit
#save the image

from http import server
from asyncio.windows_events import NULL
import threading
import math
import time
from threading import Thread
import cv2
import base64
import tkinter
import os

from PIL import Image
from PIL import ImageGrab


# resulstion of the moniter when it is using complex image formula



if UseComplexImage:
    MoniterX = 308
    MoniterY = 243
else:
    MoniterX = 164
    MoniterY = 81

#UseComplexImage = False



#haff moniter size
# MoniterX = 80
# MoniterY = 45

LastFrame = 0
start = 0
FrameToRead = 0
LastFrameThatWasBeingPlayed = 0
ProgramOffset = 0

NewThread = 0
vidcap = cv2.VideoCapture(InPutFile)
ProgramStartTime = 0
HasBeenRun = 0
Result = {}
MovieIsPaused = False

NumberOfFrames =  int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))




FrameRate = vidcap.get(cv2.CAP_PROP_FPS)
print(FrameRate)

#creates a window that contains all the stuff for changing what frame is being drawn






def main():
    global MovieIsPaused
    global ProgramOffset
    global Frame_scale
    global FrameRate
    global Result
    global NewThread
    global HasBeenRun
    global FrameToRead
    global ProgramStartTime
    global start
    #print("starting main")
    if ProgramStartTime == 0:
        ProgramStartTime = time.time()
    
    end = time.time()
    LastFrame = (end - start)
    start = time.time()
    
    print("FPS : " + str(1 / LastFrame))

    def GetFrameData(Result,vidcap,FrameToRead):
        
        #print(FrameToRead)
        vidcap.set(1, FrameToRead)
        
        success,cv2_image = vidcap.read()
        #print(success)
        img = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        Result[1] = Image.fromarray(img)

    #print("Input file: " + InPutFile)
    #print("Output file: " + OutPutFile)
    if True:
        
        if HasBeenRun == 1:
            NewThread.join()
            #print("Thread joined")
            print(Result[1])
            image = Result[1]
        else:
            GetFrameData(Result,vidcap,FrameToRead)
            image = Result[1]

        Result = {}
        #looks if the person has moved the slider
        OldFrameToRead = FrameToRead
        FrameToRead = Frame_scale.get()

        if OldFrameToRead != FrameToRead:
            ProgramOffset = ProgramOffset + (FrameToRead - OldFrameToRead)

        NewFrameToRead = time.time()
        NewFrameToRead = math.floor((NewFrameToRead - ProgramStartTime) * FrameRate)

        if not MovieIsPaused: 
            FrameToRead = NewFrameToRead
            FrameToRead = FrameToRead + ProgramOffset

        Frame_scale.set(FrameToRead)

        #ProgramOffset = 
        
        #print(FrameToRead)
        #update image that is being displayed
        #DisplayImage = image
        

        NewThread = Thread(target=GetFrameData, args=([Result,vidcap,FrameToRead]))
        NewThread.start()
        HasBeenRun = 1

    else:
        image = ImageGrab.grab()
        #bbox = (0, 0, 2560 , 1440 )
        #image = ImageGrab.grab(bbox)
    



    
    #max size of moniters
    image = image.resize((MoniterX, MoniterY))
    #image = image.resize((328, 243))

    #convert the image to limited resolution and only use 16 colors
    image = image.convert("P", palette=Image.ADAPTIVE, colors=16)

    #get the palette of the image
    palette = image.getpalette()
    #print(palette)





    
    hex_codes_list = []
    #convert list to hex codes
    for i in range(0, 16):
        #convert rgb into decimal
        hex_codes_list.append(str(palette[i * 3] + (palette[(i * 3) + 1] * 256) + (palette[(i * 3) + 2] * 65536) + 10000000))
      
    #print(hex_codes_list)

    
    ScreenCode = ""
    width, height = image.size
    
    if UseComplexImage == False:

        
    
    

        #run through every pixel in the image and give a int for which item on the list hex_codes_list it is.
        for x in range(1, width):
            for y in range(1, height):
                #get pixel
                output = image.getpixel((x, y))
                #convert to chactor
                ScreenCode = (ScreenCode + chr(output + 42))

       

    else:
                #run through every pixel in the image and give a int for which item on the list hex_codes_list it is.
        
        def RunXLayer(y,ThreadReturn,width,height):
            ThreadReturn[y] = ""
            for x in range(1, math.floor(width / 2)):

                def GetPixel(x, y):
                    #get pixel
                    output = image.getpixel((x, y))
                    #convert to chactor
                    return chr(output + 42)

                PixelData = ""
                PixelData = PixelData + GetPixel((x * 2), (y * 3))
                PixelData = PixelData + GetPixel((x * 2), (y * 3) + 1)
                PixelData = PixelData + GetPixel((x * 2), (y * 3) + 2)

                PixelData = PixelData + GetPixel((x * 2) + 1, (y * 3))
                PixelData = PixelData + GetPixel((x * 2) + 1, (y * 3) + 1)
                PixelData = PixelData + GetPixel((x * 2) + 1, (y * 3) + 2)

                
                #function to find 2 most used chactors in a string
                def MostUsed(string):
                    #create a list of the string
                    list = []
                    #add all the chactors to the list
                    for i in string:
                        list.append(i)
                    #make a list of the number of times each chactor is used
                    list2 = []
                    for i in range(0, len(list)):
                        list2.append(list.count(list[i]))
                    #find the 2 most used chactors
                    list3 = []
                    for i in range(0, 2):
                        list3.append(list[list2.index(max(list2))])
                        list2[list2.index(max(list2))] = 0
                    return list3
                    
                MostUsedColors = MostUsed(PixelData)

                #print(PixelData)
                #print( " ")

                #this is stupidly bad but it works
                #im 100% fixing this crap later

                #use the 2 most commen chactors and set every color to if its color one or color two
                #if the chactors are the same then it is color one
                #if the chactors are different then it is color two
                
                LimitedColors = 0

                if PixelData[0] == MostUsedColors[0]:
                    LimitedColors = LimitedColors + 1
                
                if PixelData[1] == MostUsedColors[0]:
                    LimitedColors = LimitedColors + 2

                if PixelData[2] == MostUsedColors[0]:
                    LimitedColors = LimitedColors + 4

                if PixelData[3] == MostUsedColors[0]:
                    LimitedColors = LimitedColors + 8

                if PixelData[4] == MostUsedColors[0]:
                    LimitedColors = LimitedColors + 16
                
                if PixelData[5] == MostUsedColors[0]:
                    LimitedColors = LimitedColors + 32

                #convert the int to chactor
                UniCodeCharacter = chr(LimitedColors + 42)
                ThreadReturn[y] = ThreadReturn[y] + UniCodeCharacter + MostUsedColors[0] + MostUsedColors[1]

        ThreadReturn = {}
        Threads = {}
        #start threads
        for y in range(1, math.floor(height / 3)):
            Threads[y] = Thread(target=RunXLayer, args=([y,ThreadReturn,width,height]))
            Threads[y].start()
            #print("started thread " + str(y))

        #get output from threads
        for y in range(1, math.floor(height / 3)):
            Threads[y].join()
            ScreenCode = ScreenCode + ThreadReturn[y]
            #print("joined thread " + str(y))
        #print(ThreadReturn)
        #print(ScreenCode)
  




            
    #print(ScreenCode)
    
    #combine the hex codes with the screen code
    ScreenCode = "".join(hex_codes_list) + ScreenCode

    #print(ScreenCode)

    #image.save(OutPutFile, "PNG")
    #print("finished main")
    return ScreenCode
    

    

# server example




def StartUpServer():
    hostName = "localhost"
    serverPort = 8080

    class MyServer(server.BaseHTTPRequestHandler):
        global FrameRate
        def do_GET(self):
            #print(FrameRate)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(main(), "utf-8"))
            SoundDataObject = open(SoundInPutFile, "rb")
            #the amt of data a secand is 6000 bytes
            #this will jump to the data that we are upto
            #print("Sound Time" + str(FrameToRead / FrameRate))
            SoundDataObject.read(math.floor((((FrameToRead / FrameRate) * 6000) * multiplySound) + SoundOffset))
            #this will read the next 6000 bytes
            SoundData = SoundDataObject.read(SoundBufferSize * 1000)
            tostring = base64.b64encode(SoundData)

            tostring = tostring.decode("utf-8")
            #print(tostring)
            self.wfile.write(bytes(str(tostring), "utf-8"))


            SoundDataObject.close()
    
    if __name__ == "__main__":        
        #webServer = server.HTTPServer((hostName, serverPort), MyServer)
        webServer = server.ThreadingHTTPServer((hostName, serverPort), MyServer)
        print("Server started http://%s:%s" % (hostName, serverPort))

        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()
        print("Server stopped.")



#StartUpServer()

def Pause():
    global MovieIsPaused
    MovieIsPaused = not MovieIsPaused

threading.Thread(target=StartUpServer).start()

tinkWindow = tkinter.Tk()
tinkWindow.geometry("800x450") 
tinkWindow.focus()
tinkWindow.title("CC Movie Control panel")
l1=tkinter.Label(tinkWindow,text="Progress Bar (measurement in frame)") 
l1.grid(row=1,column=2)

b1 = tkinter.Button(tinkWindow, text="Pause", command=Pause,fg="black",bg="orange")
b1.grid(row=2,column=1)

Frame_scale = tkinter.Scale(tinkWindow, from_=1, to=NumberOfFrames, orient='horizontal',length=650,background='orange',foreground='black',highlightcolor='orange',troughcolor='black')
Frame_scale.grid(row=2,column=2) 

tinkWindow.mainloop()

#
#
#starts a thread for the main gui
os._exit(1)



