import cv2
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
volrange= volume.GetVolumeRange()
minVol=volrange[0]
maxVol=volrange[1]

#volume.GetMasterVolumeLevel()
volrange= volume.GetVolumeRange()
#volume.SetMasterVolumeLevel(-20.0, None)


cap= cv2.VideoCapture(0)
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands=mp_hands.Hands()

while True:
    success,img= cap.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    print(results.multi_hand_landmarks)
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList=[]
            for id,lm in enumerate(handLms.landmark):
                #print(id,lm)
                h,w,c=img.shape
                cx ,cy =int(lm.x*w),int(lm.y*w)
                #print(id,cx,cy)
                lmList.append([id ,cx ,cy])
                #print(lmList)

            if lmList :
                x1 ,y1 =lmList[4][1],lmList[4][2]
                x2 ,y2=lmList[8][1],lmList[8][2]   
                cv2.circle(img,(x1,y1),10,(200,0,110),cv2.FILLED)
                cv2.circle(img,(x2,y2),10,(200,0,110),cv2.FILLED)
                length=math.hypot(x2-x1,y2-y1)
                #print(length)
                if length<50:
                    z1 =(x1+x2)//2
                    z2 =(y1+y2)//2
                    cv2.circle(img,(z1,z2),30,(200,0,110),cv2.FILLED)
            vol = np.interp(length, [50,200] , [minVol,maxVol])
            volbar=np.interp(length,[50,300],[400,150])
            volume.SetMasterVolumeLevel(vol , None)

            cv2.rectangle(img, (50,int(volbar)),(85,400),(135,205,250) ,cv2.FILLED)
                
            mp_drawing.draw_landmarks(img,handLms,mp_hands.HAND_CONNECTIONS)
    cv2.imshow("image",img)
    cv2.waitKey(15)


#vol=0==> MasterVolume =-65   
#length 50 to 300 ==> volrange= -65 to 0
