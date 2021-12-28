UseComplexImage = False


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

import asyncio
from asyncio.windows_events import NULL
import threading
from types import FrameType
import websockets
import os
import sys
import argparse
from colormap import rgb2hex
import math
import time
from threading import Thread
import cv2

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

SoundInPutFile = ("C:\\Users\\Ai Kiwi\\Desktop\\video-1.dfpwm")
InPutFile = ("C:\\Users\\Ai Kiwi\\Desktop\\video-1.mp4")
OutPutFile = ("C:\\Users\\Ai Kiwi\\Desktop\\image-2.png")

vidcap = cv2.VideoCapture(InPutFile)

ProgramStartTime = time.time()

def main():
    global start
    #print("starting main")

    
    end = time.time()
    LastFrame = (end - start)
    start = time.time()
    
    print("FPS : " + str(1 / LastFrame))



    #print("Input file: " + InPutFile)
    #print("Output file: " + OutPutFile)
    if True:

        FrameToRead = time.time()
        FrameToRead = math.floor((FrameToRead - ProgramStartTime) * 30)
        #print(FrameToRead)

        vidcap.set(1, FrameToRead)
        success,cv2_image = vidcap.read()
        #print(success)
        img = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(img)
        #image = Image.open(InPutFile)
        #image.seek(2)
    else:
        image = ImageGrab.grab()
        #bbox = (0, 0, 2560 , 1440 )
        #image = ImageGrab.grab(bbox)
    



    
    #max size of moniters
    image = image.resize((MoniterX, MoniterY))
    #max size of moniters with complex fomula stuff
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
    

    
print("started")
main()
print("ended")

# server example
from http.server import BaseHTTPRequestHandler, HTTPServer






def HostVideoServer():
    hostName = "localhost"
    serverPort = 8080

    class MyServer(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(main(), "utf-8"))

    if __name__ == "__main__":        
        webServer = HTTPServer((hostName, serverPort), MyServer)
        print("Server started http://%s:%s" % (hostName, serverPort))

        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()
        print("Server stopped.")


#idea below is a sketch btw

# the clinet is ganna know what to play by this will update every so often ahead of the video playing
# when the clinet sees this update or it says it updates int he video? it will start playing new music

def HostSoundServer():
    hostName = "localhost"
    serverPort = 8000

    class MyServer(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            f = open(SoundInPutFile,'rb')
            #self.wfile.write(bytes(f.read(), "utf-8"))
            self.wfile.write(f.read())
            f.close()


    if __name__ == "__main__":        
        webServer = HTTPServer((hostName, serverPort), MyServer)
        print("Server started http://%s:%s" % (hostName, serverPort))

        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()
        print("Server stopped.")






#create a thread to run both servers at once
threading.Thread(target=HostVideoServer).start()
#threading.Thread(target=HostSoundServer).start()

