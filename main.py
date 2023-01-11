# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os
import cv2
from cvzone.HandTrackingModule import  HandDetector

#variables
width,height = 1280, 720
folder_path = "slides"

# camara setup
cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(3,height)

def takeNumber(elem):
    return elem.split('.')[0]

# get the list of presentation images
#pathImages = sorted(os.listdir(folder_path),key=len,reverse=True)
pathImages = sorted(os.listdir(folder_path))
print(pathImages)

#variables
imageNumber = 0
hs, ws = int(120*1), int(213*1)
gestureThreshold = 300
buttonPressed = False
buttonCounter = 0
buttonDelay = 30

#hand detector

detector = HandDetector(0.8,maxHands=1)


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImages = os.path.join(folder_path, pathImages[imageNumber])
    imgCurrent = cv2.imread(pathFullImages)
    hands, img = detector.findHands(img)
    cv2.line(img, (0, gestureThreshold), (width,gestureThreshold),(0,255,0), 10)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx,cy = hand['center']
        lmList = hand['lmList']
        indexFinger = lmList[8][0],lmList[8][1]

        if cy <= gestureThreshold:

            # gesture 1
            if imageNumber > 0:
                if fingers == [1,0,0,0,0]:
                    print("left")

                    if imageNumber > 0 :
                        buttonPressed = True
                        imageNumber -= 1

            # gesture 2
            if imageNumber < len(pathImages):
                if fingers == [0,1,0,0,0]:
                    print("right")

                    if imageNumber < len(pathImages) - 1:
                        buttonPressed = True
                        imageNumber += 1
           # gesture 2
            if imageNumber < len(pathImages):
                if fingers == [0,1,1,0,0]:

                    cv2.circle(imgCurrent, indexFinger,12,(0,0,255), cv2.FILLED )
                    print("pinter")
    if buttonPressed:
        buttonCounter +=1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False



    #Webcam to image
    imgSmall = cv2.resize(img, (ws,hs))
    h, w, _ =  imgCurrent.shape
    imgCurrent[0:hs, w - ws:w] = imgSmall
    hands, img = detector.findHands(img)


    #print(pathFullImages)

    cv2.imshow("Image", img)
    cv2.imshow("Slides", imgCurrent)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break


