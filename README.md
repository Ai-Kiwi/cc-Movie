# cc-Movie
a program i made for playing movies or videos in cc tweaked

What this program can do  
upto over 30fps video! (keep in mind this is localhost (will fix later when i make really high levels of buffering))  
play video from a file  
play video from your screen  

Todo :  
add more stuff to server gui like a display and maybe put settings onto that?  
clean up code.  
make it perform compression.  
add gui into moniter.  
make it so pixels can use the sub pixel thing (allows me to doubble screen width resulastion and triple hight resolution).  
make python server not constently changeing stuff breaking buffer by changing colors.  
change to websockets for files online.  
patch how glitchy the sound is  
add huge ammounits of buffering to server and client  




**demo picture**
![image](https://user-images.githubusercontent.com/66819523/147517423-4d920f6a-35ef-493f-be69-312fffdc404b.png)

please keep in mind this needs the Cryptographic Accelerator from bperipherals  
also make sure to go in and set everything up in the settings as right now there is no gui for it  

settings notes  
the biggestest settings to change is  
1 speakers  
2 sound file and input file  
3 SoundBufferSize (the higher this the better frame rates but worse audio quality (ill fix this bug later) )
4 also make sure that you have the right framerate set
