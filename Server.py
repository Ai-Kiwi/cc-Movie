from PIL import Image
from collections import Counter

#changes to make
#add gui into app.
#add error cheeking so it crashs less.
#make it so pixels can use the sub pixel thing (allows me to doubble screen width resulastion and triple hight resolution).
#convert websockets to binary and compress them
#patch how glitchy the sound is
#add huge ammounits of buffering to server and client
#make pre render for images to make it faster
#make code cleaner and easier to read
#make propper github report system

DirForFrame = "./Frames/"

HighResChars = False

def GetSound(Frame):

    SoundFile = DirForFrame + "/sound.dfpwm"
    file = open(SoundFile, "rb")
    PosToRead = float(Frame) / 20
    PosToRead = PosToRead * 6000
    PosToRead = int(PosToRead)
    file.seek(PosToRead)

    print("reading sound at " + str(file.tell()))
    Data = file.read(6000)

    file.read()
    return Data

def GetFrame(Frame):
    FileToOpen = ""
    #create blank binary string
    FileToSend = ""

    if HighResChars == True:
        FileToSend = "H" + FileToSend
    else:
        FileToSend = "L" + FileToSend



    MoniterXRes = 164
    MoniterYRes = 81

    if HighResChars == True:
        MoniterXRes = MoniterXRes * 2
        MoniterYRes = MoniterYRes * 3


    print("image proccessing")
    #finds frame name
    
    FileToOpen = Frame
    #for some reason ffmpeg makes sure its always atlest 4 number long 
    #so we add a 0 to the front of the number
    for i in range(1,4):
        if len(FileToOpen) < 4:
            FileToOpen = "0" + FileToOpen
    FileToOpen = "frame" + FileToOpen + ".png"
    FileToOpen = DirForFrame + FileToOpen


   

    im = Image.open(FileToOpen)
    if not (im.size[0] < MoniterXRes or im.size[1] < MoniterYRes):
        im = im.resize((MoniterXRes, MoniterYRes), Image.ANTIALIAS)
    im = im.convert("P", palette=Image.ADAPTIVE, colors=16)
    
    palette = im.getpalette()

    print("getting colors")
    ListOfColors = []
    #convert list to hex codes
    for i in range(0, 16):
        #convert rgb into decimal
        Value = (palette[(i * 3) + 2] + (palette[(i * 3) + 1] * 256) + (palette[(i * 3) + 0] * 65536) + 10000000)
        ListOfColors.append(Value)
        
        # r g b
        #binary = bin(Value)[2:].zfill(25)


        FileToSend = FileToSend + str(Value)

    IntToChr = ["0" ,"1" ,"2" ,"3" ,"4" ,"5" ,"6" ,"7" ,"8" ,"9" ,"a" ,"b" ,"c" ,"d" ,"e" ,"f"]
    FileToSend = FileToSend + " : "
    
    print("doing loop")
    #loop through all the pixels and find the corasponding hex code in the list then convert that code to binary
    for y in range(0, MoniterYRes):
        for x in range(0, MoniterXRes):
            RunLoop = True

            if HighResChars == True:
                if x % 2 != 0:
                    #print("skipping because x:" + str(x % 2) + " :" + str(x))
                    RunLoop = False
                if y % 3 != 0:
                    #print("skiping because y:" + str(y % 3) + ":" + str(y))
                    RunLoop = False
            #print("not skipping")
                
                



            if RunLoop == True:
                PixelCode = 0
                if x > im.size[0] - 1 or y > im.size[1] - 1:
                    PixelCode = 1
                else:
                    PixelCode = im.getpixel((x, y))

                if HighResChars:
                    #scans in a 2x3 row and gets the 2 most used colors then makes test using that

                    #get list of colors
                    colors = []
                    for ys in range(0, 3):
                        for xs in range(0, 2):
                            item = im.getpixel((x + xs, y + ys))
                            colors.append(IntToChr[item])
                            
                    MostUsedColor = None
                    SecondMostUsedColor = None

                    data = Counter(colors)
                    #find the most used colors in the list
                    #print(colors)

                    MostUsedColor = data.most_common(1)[0][0]
                    if len(data.most_common(2)) > 1:
                        SecondMostUsedColor = data.most_common(2)[1][0]
                    else:
                        SecondMostUsedColor = MostUsedColor
                    
                    TextCode = "."




                    
                    FileToSend = FileToSend + TextCode + MostUsedColor + SecondMostUsedColor
                else:   
                    FileToSend = FileToSend + IntToChr[PixelCode]
    print("sending data")
    return FileToSend
    #convert string that is 0 and 1s to proper binary
    #print(FileToSend)
    
    

#start the websocket server using aiohttp
from aiohttp import web
import aiohttp

async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
                print("closed connection")
            else:
                if msg.data[0] == "F":
                    #remove f from the front of the string
                    Frame = msg.data[1:]
                    print("sending video data " + str(Frame))
                    FileToSend = GetFrame(Frame)
                    await ws.send_str(FileToSend)
                elif msg.data[0] == "S":
                    
                    #remove s from the front of the string
                    Sound = msg.data[1:]
                    print("sending sound data " + str(Sound))
                    FileToSend = GetSound(Sound)
                    await ws.send_bytes(FileToSend)

                
                
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws

app = web.Application()
app.add_routes([web.get('/', websocket_handler)])
web.run_app(app)


