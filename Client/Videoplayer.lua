
SoundBufferSize = 6
-- dont change this value here change below
UseDevMode = false
DevModeWaitTime = 5
IpToConnectTo = "http://localhost:8080/"
SizeOfSoundBuffer = 12000
LastSpeakerUpdate = 0
SpeakersToUse = {"left"}


--chanelog 
--made value moniter size
--made moniter use find instead of wrap

--resulstion of the moniter when it is using complex image formula
UseComplexImage = false

if UseComplexImage then
MoniterX = 308
MoniterY = 243
else
MoniterX = 164
MoniterY = 81
end


local dfpwm = require("cc.audio.dfpwm")
local decoder = dfpwm.make_decoder()
--UseComplexImage = false



--haff moniter size
-- MoniterX = 80
-- MoniterY = 45

--start drawing on moniter

local function HandleMusicStuff()
    if math.floor(LastSpeakerUpdate) == math.floor(os.clock() * (SoundBufferSize / 6)) then
    else   
        LastSpeakerUpdate = math.floor(os.clock() / (SoundBufferSize / 6))
        --term.clear()
        --get sound data from the file
        soundData = ""
        NumberUpto = 1
        while true do
            soundData = soundData .. string.sub(contents, ((MoniterX - 1) * (MoniterY - 1)) + 128 + NumberUpto, ((MoniterX - 1) * (MoniterY - 1)) + 128 + NumberUpto)
            NumberUpto = NumberUpto + 1
            if string.sub(contents, ((MoniterX - 1) * (MoniterY - 1)) + 128 + NumberUpto, ((MoniterX - 1) * (MoniterY - 1)) + 128 + NumberUpto) == "" then break end
        end




        term.setTextColor(colors.white)
        crypto = peripheral.find("cryptographic_accelerator")
        for i=1, #SpeakersToUse do
            speaker = peripheral.wrap(SpeakersToUse[i])

            --speaker.stop()
            --print("soundData : " .. "start:" .. soundData .. ":end")
            speaker.playAudio(decoder(crypto.decodeBase64(soundData)))
        end

    end
end

while true do

    local request = http.get(IpToConnectTo)
    if request == nil then
        break
    end
    contents = request.readAll()
    request.close()
    
    HandleMusicStuff()


    --get data from web
    pallete = {}

    ColorToDec = {}
    ColorToDec[1] = 1
    ColorToDec[2] = 2
    ColorToDec[3] = 4
    ColorToDec[4] = 8
    ColorToDec[5] = 16
    ColorToDec[6] = 32
    ColorToDec[7] = 64
    ColorToDec[8] = 128
    ColorToDec[9] = 256
    ColorToDec[10] = 512
    ColorToDec[11] = 1024
    ColorToDec[12] = 2048
    ColorToDec[13] = 4096
    ColorToDec[14] = 8192
    ColorToDec[15] = 16384
    ColorToDec[16] = 32768


    moniter = peripheral.find("monitor")
    moniter.setTextScale(0.5)
    term.redirect(moniter)




    --extract colors from data
    for i = 1, 16 do
      pallete[i] = tonumber(string.sub(contents, i * 8 - 7, i * 8)) - 10000000
    --convert to rgb
        --Get Blue Value
        RepeatNumberUpto = 0
        while true do
            RepeatNumberUpto = RepeatNumberUpto + 1
            if (pallete[i] - 65535) > 65536 then
                pallete[i] = pallete[i] - 65536
            else
                pallete[i] = pallete[i] - 65536
                break
            end
        end
        blue = RepeatNumberUpto
        --Get Green Value
        RepeatNumberUpto = 0
        while true do
            RepeatNumberUpto = RepeatNumberUpto + 1
            if (pallete[i] - 256) > 257 then
                pallete[i] = pallete[i] - 256
            else
                pallete[i] = pallete[i] - 256
                break
            end
        end
        Green = RepeatNumberUpto
        --Get Red Value
        Red = pallete[i]


      --set the pallte to the colors

        --Set the moniter color pallete
        term.setPaletteColor(ColorToDec[i], colors.packRGB(Red / 255, Green / 255, blue / 255))

    end


    --all of these are references to the colors in the pallete

    CharactorToDec = {}
    CharactorToDec["*"] = 1
    CharactorToDec["+"] = 2
    CharactorToDec[","] = 4
    CharactorToDec["-"] = 8
    CharactorToDec["."] = 16
    CharactorToDec["/"] = 32
    CharactorToDec["0"] = 64
    CharactorToDec["1"] = 128
    CharactorToDec["2"] = 256
    CharactorToDec["3"] = 512
    CharactorToDec["4"] = 1024
    CharactorToDec["5"] = 2048
    CharactorToDec["6"] = 4096
    CharactorToDec["7"] = 8192
    CharactorToDec["8"] = 16384
    CharactorToDec["9"] = 32768

    CharactorToBlit = {}

    CharactorToBlit["*"] = "0"
    CharactorToBlit["+"] = "1"
    CharactorToBlit[","] = "2"
    CharactorToBlit["-"] = "3"
    CharactorToBlit["."] = "4"
    CharactorToBlit["/"] = "5"
    CharactorToBlit["0"] = "6"
    CharactorToBlit["1"] = "7"
    CharactorToBlit["2"] = "8"
    CharactorToBlit["3"] = "9"
    CharactorToBlit["4"] = "a"
    CharactorToBlit["5"] = "b"
    CharactorToBlit["6"] = "c"
    CharactorToBlit["7"] = "d"
    CharactorToBlit["8"] = "e"
    CharactorToBlit["9"] = "f"

    CharactorToBinary = {}
    CharactorToBinary["*"] = "000000"
    CharactorToBinary["+"] = "000001"
    CharactorToBinary[","] = "000010"
    CharactorToBinary["-"] = "000011"
    CharactorToBinary["."] = "000100"
    CharactorToBinary["/"] = "000101"
    CharactorToBinary["0"] = "000110"
    CharactorToBinary["1"] = "000111"
    CharactorToBinary["2"] = "001000"
    CharactorToBinary["3"] = "001001"
    CharactorToBinary["4"] = "001010"
    CharactorToBinary["5"] = "001011"
    CharactorToBinary["6"] = "001100"
    CharactorToBinary["7"] = "001101"
    CharactorToBinary["8"] = "001110"
    CharactorToBinary["9"] = "001111"
    CharactorToBinary[":"] = "010000"
    CharactorToBinary[";"] = "010001"
    CharactorToBinary["<"] = "010010"
    CharactorToBinary["="] = "010011"
    CharactorToBinary[">"] = "010100"
    CharactorToBinary["?"] = "010101"
    CharactorToBinary["@"] = "010110"
    CharactorToBinary["A"] = "010111"
    CharactorToBinary["B"] = "011000"
    CharactorToBinary["C"] = "011001"
    CharactorToBinary["D"] = "011010"
    CharactorToBinary["E"] = "011011"
    CharactorToBinary["F"] = "011100"
    CharactorToBinary["G"] = "011101"
    CharactorToBinary["H"] = "011110"
    CharactorToBinary["I"] = "011111"
    CharactorToBinary["J"] = "100000"
    CharactorToBinary["K"] = "100001"
    CharactorToBinary["L"] = "100010"
    CharactorToBinary["M"] = "100011"
    CharactorToBinary["N"] = "100100"
    CharactorToBinary["O"] = "100101"
    CharactorToBinary["P"] = "100110"
    CharactorToBinary["Q"] = "100111"
    CharactorToBinary["R"] = "101000"
    CharactorToBinary["S"] = "101001"
    CharactorToBinary["T"] = "101010"
    CharactorToBinary["U"] = "101011"
    CharactorToBinary["V"] = "101100"
    CharactorToBinary["W"] = "101101"
    CharactorToBinary["X"] = "101110"
    CharactorToBinary["Y"] = "101111"
    CharactorToBinary["Z"] = "110000"
    CharactorToBinary["["] = "110001"
    CharactorToBinary["\\"] = "110010"
    CharactorToBinary["]"] = "110011"
    CharactorToBinary["^"] = "110100"
    CharactorToBinary["_"] = "110101"
    CharactorToBinary["`"] = "110110"
    CharactorToBinary["a"] = "110111"
    CharactorToBinary["b"] = "111000"
    CharactorToBinary["c"] = "111001"
    CharactorToBinary["d"] = "111010"
    CharactorToBinary["e"] = "111011"
    CharactorToBinary["f"] = "111100"
    CharactorToBinary["g"] = "111101"
    CharactorToBinary["h"] = "111110"
    CharactorToBinary["i"] = "111111"



    term.setCursorPos(1,1)

    --used in case you wanna see the buffer in action
    --term.clear()

    if ScreenBuffer == nil then
    ScreenBuffer = {}
    end

    --tests if its using the newer render method
    if UseComplexImage == false then
            --repeat for every line
            for y=0, (MoniterY - 1) do
                --these values are used for what it should right and what colors it should use
                Row = ""
                RowLeagth = ""
                --runs through the line and gets the color and the char
                for x=0, (MoniterX - 2) do
                    --get the char
                    ChractorNumber = y + (x * (MoniterY - 1)) + 128
                    Charactor = string.sub(contents, ChractorNumber, ChractorNumber)
                    --looks if its the end of the line
                    if Charactor == "" then break end
                    --adds the char to the row
                    --print(x,":",y)
                    --print(Charactor)
                    Row = Row .. CharactorToBlit[Charactor]
                    RowLeagth = RowLeagth .. " "
                end 

                -- draws the line
                --loots at if its in the buffer already
                if UseBuffer == false then ScreenBuffer[y] = nil end
                if ScreenBuffer[y] == Row then
                else
                    --draws the line
                    term.setCursorPos(1,y)
                    term.blit(RowLeagth,Row,Row)
                    --again in case you wanna see it draw in slow mo
                    --os.sleep(0.1)
                    --adds to buffer
                    ScreenBuffer[y] = Row
                end
            end
    else
            --repeat for every line
            for y=0, (MoniterY / 3) - 1 do
                --these values are used for what it should right and what colors it should use
                FristColor = ""
                secandColor = ""
                Letters = ""
                --runs through the line and gets the color and the char
                for x=0, (MoniterX / 2) do
                    --get the frist color
                    ChractorNumber = ((x + (y * ((MoniterX / 2) - 1))) * 3) + 129
                    -- print(ChractorNumber)
                    FristCharactor = string.sub(contents, ChractorNumber + 1, ChractorNumber + 1)
                    --get the secand color

                    -- print(ChractorNumber)
                    SecandCharactor = string.sub(contents, ChractorNumber + 2, ChractorNumber + 2)

                    -- get chactor to draw

                    -- print(ChractorNumber)
                    Charactor = string.sub(contents, ChractorNumber, ChractorNumber)
                    

                    --looks if its the end of the line
                    if Charactor == "" then break end
                    -- print("Charactor : " .. Charactor)
                    BinToConvert = CharactorToBinary[Charactor]
                    --convert the binary to the not but is unicode?
                    BinValue = 0x80
                    AltBinValue = 0x80
                    -- value : 0x80 
                    -- frist value : 0x1 
                    -- secand value : 0x2
                    -- third value : 0x4
                    -- fourth value : 0x8
                    -- fifth value : 0x10
                    -- in order to change 6th we enable all and then flip the colors
                
                    -- print("BinToConvert : " .. BinToConvert)
                    if string.sub(BinToConvert,0,0) == "1" then
                        BinValue = BinValue + 0x1
                    else
                        AltBinValue = AltBinValue + 0x1
                    end

                    if string.sub(BinToConvert,1,1) == "1" then
                        BinValue = BinValue + 0x2
                    else
                        AltBinValue = AltBinValue + 0x2
                    end

                    if string.sub(BinToConvert,2,2) == "1" then
                        BinValue = BinValue + 0x4
                    else
                        AltBinValue = AltBinValue + 0x4
                    end

                    if string.sub(BinToConvert,3,3) == "1" then
                        BinValue = BinValue + 0x8
                    else
                        AltBinValue = AltBinValue + 0x8
                    end

                    if string.sub(BinToConvert,4,4) == "1" then
                        BinValue = BinValue + 0x10
                    else
                        AltBinValue = AltBinValue + 0x10
                    end
                    -- print("BinValue : " .. BinValue)


                    --adds the char to the row
                    if string.sub(BinToConvert,5,5) == "1" then
                        Letters = Letters .. string.char(BinValue)
                    else
                        Letters = Letters .. string.char(AltBinValue)
                    end
                    -- print("Letters : " .. Letters)
                    -- print(FristCharactor)
                    -- print (SecandCharactor)
                    -- print(CharactorToBlit[tostring(FristCharactor)])
                    -- print(CharactorToBlit[tostring(SecandCharactor)])

                    FristColor = FristColor .. CharactorToBlit[tostring(FristCharactor)]
                    secandColor = secandColor .. CharactorToBlit[tostring(SecandCharactor)]
                    -- print("FristColor : " .. FristColor)
                    -- print("secandColor : " .. secandColor)
                    -- print("Letters : " .. Letters)
                    -- print(" --- ")

                end 


                --draws the line
                term.setCursorPos(1,y )
                --print("Ehsyh5ys45yhrse5yh5reyh")
                term.blit(Letters,FristColor,secandColor)
                --again in case you wanna see it draw in slow mo
                --os.sleep(0.1)
                --adds to buffer
                ScreenBuffer[y] = Row

            end
    end

    term.setCursorPos(1,1)


end
