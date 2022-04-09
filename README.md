# Gesture_volume_control


a python project that detects hand gesture and adjust the system volume acocrdingly.

It analyse the distance between thumb tip and index fingure tip and adjust the system volume accordingly

libraries used :

mediapipe :for hand /gesture detection

pycaw : for accesing the system audio

open cv: for image processing

volume ranges are adjested as follow:

   system vol=0 is equivalent to MasterVolume =-65 
   system vol=max is equivalent to MasterVolume=0
   distance between thumb tip  and index fingure tip renge  50 to 300 ==> volrange= -65 to 0
