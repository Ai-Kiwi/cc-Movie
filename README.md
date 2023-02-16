# cc-Movie
a program i made for playing movies or videos in cc tweaked

this is currently very easrly in release and the version here is the 3rd remake. when i have time to update this i will write a propper desc. for now this is kinda just a code dump.


**demo picture from ages ago (need to update as whole code base been recodes alot of times since then)**
![image](https://user-images.githubusercontent.com/66819523/147517423-4d920f6a-35ef-493f-be69-312fffdc404b.png)


**making image files**
```
best for tall videos  
ffmpeg -i video.mp4 -vf scale=-1:81 -r 24 frame%04d.png  

best for norm (pick low res if high not needed for speed)  
ffmpeg -i video.mp4 -vf scale=164:81 -r 24 frame%04d.png #supports low res mode  
ffmpeg -i video.mp4 -vf scale=328:243 -r 24 frame%04d.png #support high res mode  
```



