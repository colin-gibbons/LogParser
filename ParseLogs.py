from urllib.request import urlopen
import os
import re
import datetime

url = "https://s3.amazonaws.com/tcmg476/http_access_log"
fileName = "http.log"

def getDataFile(): 
    with open(fileName, 'wb') as logFile: # creates a new http.log file
        with urlopen(url) as stream: # connect to server
            fileSize = stream.length

            # https://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python
            print("Downloading \"%s\" (%s KB)..." % (fileName, fileSize / 1000))

            currentFileSize = 0
            blockSize = 8192
            while currentFileSize < fileSize: # loop through download (blockSize at a time), and write bytes to file
                buffer = stream.read(blockSize)
                if not buffer:
                    break

                currentFileSize += len(buffer)
                logFile.write(buffer)
                status = r"%10d [%3.2f%%]" % (currentFileSize, currentFileSize*100. / fileSize) # displays percentage downloaded
                status = status + chr(8)*(len(status) + 1)

                print(status, end="") # prints without appended "\n"
            
            print("", end="\n") # reset print appended char


def main():
    if not os.path.exists(fileName):  # check if file exists before re-downloading
        print("No cached " + fileName + " found.\nDownloading from: " + url)
        getDataFile() # Saves file as http.log
    else:
        print("Using cached " + fileName + " file.")
    
    with open(fileName, 'r') as logFile: #opens http.log file
        print("starting parser")

        dictMonth = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}, 10: {}, 11: {}, 12:{}}
        monthToInt = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec':12}

        maxlines=100
        curline=0
        for line in logFile:
            curline+=1 
            splitData = re.split('.*\[(.*?):.*\] \".* (.*) .*\" (\d{3})', line)
            print(splitData)
            dateSplit = splitData[1].split('/')
            dateVar = datetime.date(int(dateSplit[2]), monthToInt[dateSplit[1]], int(dateSplit[0]))

            print(dateVar)
            if dateVar.day in dictMonth[dateVar.month]:
                dictMonth[dateVar.month][dateVar.day].append({'date': dateVar, 'name':splitData[2], 'code':splitData[3]})
            else:
                dictMonth[dateVar.month][dateVar.day] = [{'date': dateVar, 'name':splitData[2], 'code':splitData[3]}]

            #dictMonth[date[1]]

            if curline>maxlines: 
                break

        print (dictMonth)
            
        
     

if __name__ == "__main__":
    main()