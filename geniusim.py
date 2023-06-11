import numpy as np
import pyautogui as pa
import time
import cv2 as cv

def getSimID():
    with open("simID.txt", 'r') as file:
        simID = int(file.readline())
        file.close()
    return simID

def updateSimID():
    global simulationID; simulationID += 1
    with open("simID.txt", 'w') as file:
        file.write('0'*(3-len(str(simulationID))) + str(simulationID))

global iteration; iteration = 0
global increment; increment = 0.00122
global itsPerSim; itsPerSim = 10 #iterations per simulation
global fileNumber; fileNumber = 0
global simulationID; simulationID = getSimID()

updateSimID()
#the location of the "stop simulation" button
global stopSimButton; stopSimButton = (670,109) 

def imageToNP(im):
    image = np.array(im)
    imageCopy = image.copy()
    image[:,:,2] = imageCopy[:,:,0]
    image[:,:,0] = imageCopy[:,:,2]
    return image

def tuneWindow(x,y):
    while True:
        screen = imageToNP(pa.screenshot())
        screen[:,x,:] = (0,255,0)
        screen[y,:,:] = (0,255,0)
        cv.imshow('',np.array(screen, 'uint8'))
        cv.moveWindow('',0,0)
        cv.setWindowProperty('', cv.WND_PROP_TOPMOST, 1)
        cv.waitKey(1000)
        cv.destroyWindow('')
        cv.waitKey(2000)
        
        

def setStartValue():
    start = 0 + iteration * increment
    for i in str(start)[:7]:
        pa.press(i, interval = 0.1)

def setStopValue():
    stop = (iteration + itsPerSim) * increment
    for i in str(stop)[:7]:
        pa.press(i, interval = 0.1)
  
def setup():
    #   --simulate--
    pa.leftClick(221,45)
    time.sleep(0.5)
    #   --analysis and simulation--
    pa.leftClick(300,166)
    time.sleep(2)

    #wait for the window to open
    while True:
        windowColor = pa.screenshot().getpixel((963,179))
        if sum(abs(np.array(windowColor) - np.array((153,180,209)))) < 50:   #it's open
            time.sleep(3)
            break

    #   --start value--
    pa.leftClick(1090,460)
    time.sleep(0.1)
    pa.leftClick(1090,460)
    time.sleep(0.1)    
    setStartValue()

    #   --stop value--    
    pa.leftClick(1090,490)
    time.sleep(0.1)
    pa.leftClick(1090,490)
    time.sleep(0.1)
    setStopValue()

    #   --Run--
    pa.leftClick(1071,878)

    global iteration; iteration += itsPerSim
    
def spectateSimulation():
    global stopSimButton
    
    #waits for the button to turn red
    while True:
        stopButtonColor = pa.screenshot().getpixel(stopSimButton)
        if sum(abs(np.array(stopButtonColor) - np.array((255,0,0)))) < 50:   #it's red
            time.sleep(0.5)
            break
        time.sleep(2)
    
    #waits for the button to turn grey
    while True:
        stopButtonColor = pa.screenshot().getpixel(stopSimButton)
        if sum(abs(np.array(stopButtonColor) - np.array((160,160,160)))) < 50:   #it's grey
            time.sleep(3)
            return
        time.sleep(2)
        
def saveSimulation():
    global simulationID; global fileNumber;
    time.sleep(2)

    #   --save to measurement file--
    pa.leftClick(932,244)
    time.sleep(5)
    
    # name the file
    fileName = ('0'*(3-len(str(simulationID)))) + str(simulationID) + ' '
    fileName += ('0'*(5-len(str(fileNumber)))) + str(fileNumber)
    for i in fileName:
        pa.press(i)
        time.sleep(0.1)

    #   --save--
    time.sleep(2)
    pa.leftClick(1014,718)

    #   --ok--
    time.sleep(1)
    pa.leftClick(675,691)

def cleanup():
    time.sleep(5)

    #   --Delete--
    for i in range(4):
        pa.leftClick(304,243)
        time.sleep(0.1)

    #   --Close--
    time.sleep(2)
    pa.leftClick(1066,179)

for i in range(410):    
    setup()
    spectateSimulation()
    saveSimulation()
    cleanup()
    fileNumber += 1
    time.sleep(2)
    print("iteration:", iteration, "\t", "time:", time.perf_counter())

