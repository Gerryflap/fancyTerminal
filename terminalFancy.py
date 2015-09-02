import os
import time
import requests

strings = {
    "all":[1,1,1, 1,1,1, 1,1,1, 1,1,1, 1,1,1],
    "0":[1,1,1, 1,0,1, 1,0,1, 1,0,1, 1,1,1],
    "1":[0,1,0, 1,1,0, 0,1,0, 0,1,0, 0,1,0],
    "2":[1,1,1, 0,0,1, 1,1,1, 1,0,0, 1,1,1],
    "3":[1,1,1, 0,0,1, 0,1,1, 0,0,1, 1,1,1],
    "4":[1,0,1, 1,0,1, 1,1,1, 0,0,1, 0,0,1],
    "5":[1,1,1, 1,0,0, 1,1,1, 0,0,1, 1,1,1],
    "6":[1,1,1, 1,0,0, 1,1,1, 1,0,1, 1,1,1],
    "7":[1,1,1, 0,0,1, 0,0,1, 0,0,1, 0,0,1],
    "8":[1,1,1, 1,0,1, 1,1,1, 1,0,1, 1,1,1],
    "9":[1,1,1, 1,0,1, 1,1,1, 0,0,1, 1,1,1],
    ":":[0,0,0, 0,1,0, 0,0,0, 0,1,0, 0,0,0],
    "-":[0,0,0, 0,0,0, 1,1,1, 0,0,0, 0,0,0]
    }


def getPrintString(string, scale):
    total = "\n"
    sign = "#"
    space = " "
    for i in range(5):
        row = ""
        for char in string:
            if char in strings:
                row += space * scale
                for j in range(3):
                    if strings[char][i*3 + j]:
                        row += sign * scale
                    else:
                        row += space * scale
        row += "\n"
        row *= scale
        total += row
    return total
  
def fetchWeather(height = 5):
    r = requests.get('http://gps.buienradar.nl/getrr.php?#lat=52.2167&lon=6.9000')#lat=52.81&lon=5.98')
    text = r.text
    moments = text.split("\r\n")   
    sign = "#"
    space = " "
    none = " "
    out = "\n"
    for i in range(height + 1):
        row = space + "|"
        for moment in moments:
            if moment != '':
                rainfall = int(moment.split("|")[0])
                if i == height:
                    row += "-" * 2
                elif rainfall > 255-i*(255/height):
                    row += sign + space
                else:
                    row += none + space
        out += row + "\n"
    return out
        
                

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

clearScreen()
input("If this displayed a seperate terminal, please kill the program now! otherwise press enter to continue...")
clearScreen()
tScale = int(input("Time display scale: "))
dScale = int(input("Date display scale: "))
lastUpdate = -1
outWeather = fetchWeather(10)
while True:
    
    t = time.localtime()

    outTime = "{:0= 3}:{:0= 3}:{:0= 3}".format(t.tm_hour, t.tm_min, t.tm_sec)
    outDate = "{:0= 5}-{:0= 3}-{:0= 3}".format(t.tm_year, t.tm_mon, t.tm_mday)

    if lastUpdate != t.tm_min:
        outWeather = fetchWeather(10)
    
    clearScreen()
	
    print(getPrintString(outTime, tScale))
    print(getPrintString(outDate, dScale))
    print(outWeather)

    time.sleep(1)
    
