#Snake Alarm
import tkinter
import time
import datetime
import threading
import winsound

main = tkinter.Tk()
main.title("Snake Alarm")
main.geometry('400x350')
main.wm_withdraw

LoopBoolean = True

#Title widgets
title = tkinter.Label(main, text='Snake Alarm', font=(None, 36, 'bold'))
clockFrame = tkinter.Frame(main)
timeLabel = tkinter.Label(clockFrame, text='HH:MM', font=(None, 24), pady = 20)
timeSecondLabel = tkinter.Label(clockFrame, text = 'SS', font = (None, 12))
meridiemLabel = tkinter.Label(clockFrame, text = 'AM/PM', font = (None, 15))

#Canvas widget
snakeCanvas = tkinter.Canvas(main, width = 300, height = 100, bg = 'white')
snakeCanvas.create_polygon(0, 20, 0, 50, 70, 50, 80, 20, 50, 0)

# --- Time area frame ---
timeFrame = tkinter.Frame(main)

userTimeEntryFrame = tkinter.Frame(timeFrame)

# Time User Input Frame
timeEntryFrame = tkinter.Frame(userTimeEntryFrame)
startLabel = tkinter.Label(timeEntryFrame, text = "Start Time (HH:MM)", padx = 5)
timeEntry = tkinter.Entry(timeEntryFrame, bd = 1, width = 5)
startLabel.pack(side = 'left')
timeEntry.pack(side = 'left')

#Interval User Input Frame
intervalEntryFrame = tkinter.Frame(userTimeEntryFrame)
intervalLabel = tkinter.Label(intervalEntryFrame, text = "Interval Time (MM)", padx = 5)
intervalEntry = tkinter.Entry(intervalEntryFrame, bd = 1, width = 4)
intervalLabel.pack(side = 'left')
intervalEntry.pack(side = 'left')

#Number of intervals User Input
intervalFreqEntryFrame = tkinter.Frame(userTimeEntryFrame)
intervalFreqLabel = tkinter.Label(intervalFreqEntryFrame, text = "Frequency of Interval: ")
intervalVar = tkinter.StringVar(intervalFreqEntryFrame)
intervalVar.set('0') #default value
intervalFreq = tkinter.OptionMenu(intervalFreqEntryFrame, intervalVar, '0', '1', '2', '3', '4', '5')
intervalFreqLabel.pack(side = 'left')
intervalFreq.pack(side = 'left')


timeEntryFrame.pack(side = 'top')
intervalEntryFrame.pack(side = 'top')
intervalFreqEntryFrame.pack(side = 'top')
setTimeLabel = tkinter.Label(main, text = "Alarm at : HH:MM | Interval: 0 Minutes 0 times")

startBtn = tkinter.Button(timeFrame, text = "Start", activeforeground = "green")

#Radio Button AM/PM
meridiemFrame = tkinter.Frame(timeFrame)
meridiem = tkinter.StringVar() 
amRB = tkinter.Radiobutton(meridiemFrame, text = 'PM', variable = meridiem,
                           value = 'PM')
pmRB = tkinter.Radiobutton(meridiemFrame, text = 'AM', variable = meridiem,
                           value = 'AM')
pmRB.pack()
amRB.pack()


#Packing time area
userTimeEntryFrame.pack(side = 'left')
meridiemFrame.pack(side = 'left')
startBtn.pack(side = 'left')

title.pack()
timeLabel.pack(side = 'left')
timeSecondLabel.pack(side = 'left')
meridiemLabel.pack(side = 'left')
clockFrame.pack()
snakeCanvas.pack()
setTimeLabel.pack()
timeFrame.pack()


currentTime = ""
#Function to loops clock indefinitely
def timeLoop():
    global currentTime
    global currentMeridiem
    currentTime = ""
    while (LoopBoolean):
        hour = datetime.datetime.now().hour % 12
        if (hour == 0):
            hour = 12
        minute = datetime.datetime.now().minute

        #Changes AM/PM
        if (datetime.datetime.now().hour <= 12):
            meridiemLabel.config(text = 'AM')
            currentMeridiem = 'AM'
        else:
            meridiemLabel.config(text = 'PM')
            currentMeridiem = 'PM'
        
        #Hours
        strHour = str(hour)
        if ((hour is not 12) ^ (hour is not 11) ^ (hour is not 10)):
            strHour = "0" + str(hour)

        #Minutes    
        strMinute = str(minute)
        if(minute == 0 or minute == 1 or minute == 2 or minute == 3 or minute == 4 or
           minute == 5 or minute == 6 or minute == 7 or minute == 8 or minute == 9):
            strMinute = "0" + str(minute)
        #Seconds
        second = datetime.datetime.now().second
        strSecond = str(second)
        if(second == 0 or second == 1 or second == 2 or second == 3 or second == 4 or
           second == 5 or second == 6 or second == 7 or second == 8 or second == 9):
            strSecond = "0" + str(second)
        
        
        currentTime = strHour +":"+ strMinute
        
        timeLabel.config(text = currentTime)
        timeSecondLabel.config(text = strSecond)
        main.update()
# Thread to run timeLoop function        
timeThread = threading.Thread(target=timeLoop)
timeThread.start()



#TODO: Start the time
# Starts alarm
def startAlarm():
    global startTime
    global intervalTime
    global checkAlarm
    global intervalFreqNum
    global intervalBool
    intervalBool = False
    intervalFreqNum = 0
    startTime = timeEntry.get()
    intervalTime = intervalEntry.get()
    if((':' not in startTime[2:3]) or startTime.isalpha() or len(startTime) > 5):
        print("Enter a valid time")
    else:
        if(('12' in startTime[0:2] or '11' in startTime[0:2] or '10' in startTime[0:2] or
           '0' in startTime[0:1]) and '00' not in startTime[0:2]):
            if (int(startTime [0:2]) <=12):
                if (intervalTime == ""):                    
                    setTimeLabel.config(text = "Alarm at : "+ startTime +" | Interval: 0 Minutes 0 times")
                    intervalBool = False
                    startBtn.config(command = stopAlarm, text = 'Stop')
                else:
                    intervalFreqNum = intervalVar.get()
                    setTimeLabel.config(text = "Alarm at : "+ startTime +" | Interval: " + intervalTime + " Minutes " + intervalVar.get() + " times")
                    intervalBool = True
                    startBtn.config(command = stopAlarm, text = 'Stop')
                    
                try:
                    alarmThread.start()
                except RuntimeError as err:
                    print('No new thread created')
            else:
                # TODO: Make a warning label
                print("Enter a valid time following the format, HH:MM")
        else:
            # TODO: Make a warning label
            print("Enter a valid time following the format, HH:MM")
    print(startTime)     
startBtn.config(command = startAlarm)

#TODO: Stop alarm SOUND
def stopAlarm():
    global alarmCheck
    global startTime
    global intervalBool
    intervalBool = False
    startTime = '00:00'
    print('\nAlarm has been stopped')
    startBtn.config(command = startAlarm, text = 'Start')

def playSound():
    winsound.PlaySound('watchsound.wav', winsound.SND_FILENAME)

# Function to check clock continuously
def checkClock():
    global startTime
    global alarmCheck
    global intervalTime
    global intervalFreqNum
    global intervalBool
    intervalHour = 0
    alarmHourTemp = 0
    alarmMinTemp = 0
    intervalTemp = 0
    hourCnt = 0
    intervalList = ['00:00', '00:00', '00:00', '00:00', '00:00']
    alarmCheck = True
    while(alarmCheck):
        intervalList = ['00:00', '00:00', '00:00', '00:00', '00:00'] #Resets interval list
        if (intervalBool):
            hourCnt = 0
            print(startTime[3:5] + " Look Here")
            try: #Gets double digit interval
                intervalTemp = int(intervalTime[0:2])
            except: #Get single digit interval
                intervalTemp = int(intervalTime[1:2])
            #Loops to get next alarm times
            for i in range(int(intervalFreqNum)):
                try: #Try to get double digits minutes
                    alarmMinTemp = (int(startTime[3:5])+intervalTemp*i)%60
                    if (int(startTime[3:5])+intervalTemp*i >= (60*(1+hourCnt))):
                        hourCnt += 1
                except: #Except get single digit minutes
                    alarmMinTemp = (int(startTime[4:5])+intervalTemp*i)%60
                    if (int(startTime[4:5])+intervalTemp*i >= (60*(1+hourCnt))):
                        hourCnt += 1                
                try:
                    alarmHourTemp = int(startTime[0:2]) + hourCnt
                except:
                    alarmHourTemp = int(startTime[1:2]) + hourCnt
                alarmHourTemp = alarmHourTemp % 12
                if (alarmHourTemp == 0):
                    alarmHourTemp = 12
                intervalList[i] = '0'+str(alarmHourTemp) + ':' + str(alarmMinTemp)+'0'                

        #Todo: Use modulus to get corrent hours and minutes
            intervalBool = False
            print(intervalList)
        if (startTime == currentTime and currentMeridiem == meridiem.get()):
            print("Ring ring")
            playSound()
        time.sleep(0.01);
alarmThread = threading.Thread(target = checkClock)


# Animation threading
def animation():
    atEnd = False
    loopForever = True
    x = 0
    while(loopForever):
        x += 1
        if (not atEnd):    
            snakeCanvas.move(1, 5, 0)
            if (x == 38):
                atEnd = True
                x = 0
        elif(atEnd):
            snakeCanvas.move(1,-5,0)
            if (x == 38):
                atEnd = False
                x = 0
        main.update()
        time.sleep(0.05)
animationThread = threading.Thread(target = animation)
animationThread.start()




main.mainloop()
