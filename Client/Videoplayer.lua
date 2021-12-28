-- trys to remove unneeded redraw calls
-- works alot better without UseTermBlit on.
-- due to the fact that blit draws it all in 1 call it kinda makes this irrelevant
UseBuffer = true
-- this is a remade video player that is alot faster and doesnt have any where as much screen tear
UseTermBlit = true
--restarts program every screen update.
--makes program crash for some reason.
UseDevMode = false
DevModeWaitTime = 5
IpToConnectTo = "http://localhost:8080/"


MoniterX = 164
MoniterY = 81

while UseDevMode == false do

    local request = http.get(IpToConnectTo)
    contents = request.readAll()
    request.close()

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


    --start drawing on moniter
    moniter = peripheral.wrap("top")
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


    term.setCursorPos(1,1)

    --used in case you wanna see the buffer in action
    --term.clear()

    if ScreenBuffer == nil then
    ScreenBuffer = {}
    end

    --tests if its using the newer render method or the old crappy one
    if UseTermBlit == false then
        --term.clear()
        --repeat for every char in the file
        for y=0, MoniterY do
            for x=0, MoniterX do
                --get the char
                ChractorNumber = y + (x * (MoniterY - 1)) + 128
                Charactor = string.sub(contents, ChractorNumber, ChractorNumber)
                --get the color
                if UseBuffer == false then ScreenBuffer[x .. ":" .. y] = nil end
                -- looks if its already in the buffer (meaning its that color already)
                if ScreenBuffer[x .. ":" .. y] == Charactor then
                else
                    --draw the pixel
                    if Charactor == "" then break end
                    --sets the pos and the color of the pixel
                    moniter.setBackgroundColor(CharactorToDec[Charactor])
                    moniter.setCursorPos(x + 1, y)
                    --draws the pixel
                    moniter.write(" ")
                    --used in case you wanna see it draw in slow mo
                    --os.sleep(0.1)
                    ScreenBuffer[x .. ":" .. y] = Charactor
                end
            end 
        end
    else
        --repeat for every line
        for y=0, (MoniterY - 1) do
            --these values are used for what it should right and what colors it should use
            Row = ""
            RowLeagth = ""
            --runs through the line and gets the color and the char
            for x=0, 163 do
                --get the char
                ChractorNumber = y + (x * (MoniterY - 1)) + 128
                Charactor = string.sub(contents, ChractorNumber, ChractorNumber)
                --looks if its the end of the line
                if Charactor == "" then break end
                --adds the char to the row
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
    end


    term.setCursorPos(1,1)
end

if UseDevMode == true then
    os.sleep(DevModeWaitTime)
    shell.run("VideoPlayer.lua")
end
