


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
import websockets
import os
import sys
import argparse
from colormap import rgb2hex

from PIL import Image
from PIL import ImageGrab

def main():
    InPutFile = ("C:\\Users\\Ai Kiwi\\Desktop\\image-1.png")
    OutPutFile = ("C:\\Users\\Ai Kiwi\\Desktop\\image-2.png")





    #print("Input file: " + InPutFile)
    #print("Output file: " + OutPutFile)
    if False:
        image = Image.open(InPutFile)
    else:
        bbox = (0, 0, 2560 , 1440 )
        image = ImageGrab.grab(bbox)

    




    #max size of moniters
    image = image.resize((164, 81))
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
    #run through every pixel in the image and give a int for which item on the list hex_codes_list it is.
    for x in range(1, width):
        for y in range(1, height):
            #get pixel
            output = image.getpixel((x, y))
            #convert to chactor
            ScreenCode = (ScreenCode + chr(output + 42))


            
    #print(ScreenCode)
    
    #combine the hex codes with the screen code
    ScreenCode = "".join(hex_codes_list) + ScreenCode

    #print(ScreenCode)

    #image.save(OutPutFile, "PNG")

    return ScreenCode
    

    

#print(main())


# server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

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
