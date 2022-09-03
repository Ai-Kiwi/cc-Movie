local ws = http.websocket("ws://localhost:8080/")

local monitor = peripheral.find("monitor")

monitor.setTextScale(0.5)


--client and server side settings
local ImageWidth = 164
local ImageHeight = 81


local startTime = os.epoch("utc")
local StartOffset = 1




local function DrawScreen()
    while true do

        local time = os.epoch("utc") - startTime
        time = time / 1000
        time = time * 20
        time = math.floor(time)

        ws.send("F" .. time + 1)
        Message = ws.receive(1)
        while Message:len() == 6000 do
            Message = ws.receive(1)

        end

        local HighResMode = false
        if Message:sub(1,1) == "H" then
            HighResMode = true
        end

        for i=0, 15 do 

            
            ColorData =  Message:sub(StartOffset + (i*8) + 1, StartOffset + (i*8) + 8)

            --convert to rgb
            local RGBData = tonumber(ColorData) - 10000000
            local r = math.floor(RGBData / 65536)
            RGBData = RGBData - (r * 65536)
            local g = math.floor(RGBData / 256)
            RGBData = RGBData - (g * 256)
            local b = RGBData





            local Hex = colors.packRGB(r / 255, g / 255, b / 255) 


            monitor.setPaletteColour(math.pow(2,i) / 1, Hex)
        end

        --loop throw image data and draw
        --times by 3 because each pixel is 3 bytes
        for y=1, ImageHeight do
            CurrentText = ""
            CurrentColor = ""
            CurrentSecondColor = ""

            ValueSize = 1
            if HighResMode then
                ValueSize = 3
            end

            for x=1, ImageWidth do
                ValueReading = (((y-1)*ImageWidth) + (x-1))*ValueSize
                ValueReading = ValueReading + 129 + StartOffset

                CurrentText = CurrentText .. Message:sub(ValueReading,ValueReading)
                CurrentColor = CurrentColor .. Message:sub(ValueReading + 1,ValueReading + 1)
                CurrentSecondColor = CurrentSecondColor .. Message:sub(ValueReading + 2,ValueReading + 2)
            end
            monitor.setCursorPos(1,y)
            monitor.blit(CurrentText,CurrentColor,CurrentSecondColor)


        end



        os.sleep(0)
    end
end

local dfpwm = require("cc.audio.dfpwm")
local decoder = dfpwm.make_decoder()

local function GetSoundData(OffsetForSound)

    ws.send("S" .. math.floor((os.epoch("utc")-startTime)/1000*20) + 1 + OffsetForSound)
    local SoundDataCaught = ws.receive(1)



    while SoundDataCaught:len() ~= 6000 do
        SoundDataCaught = ws.receive(1)

    end
    SoundDataCaught = decoder(SoundDataCaught)
    return SoundDataCaught
end

local function PlaySound()
    local speaker = peripheral.find("speaker")
    SoundDataCaught = GetSoundData(0)
    while true do

       while not speaker.playAudio(SoundDataCaught) do os.sleep(0) end
       SoundDataCaught = GetSoundData(20)

    end
end
    

    

parallel.waitForAny(DrawScreen, PlaySound)

ws.close()
