from urllib.request import urlopen
import os
import re
import datetime

# Helper Funcs
def genDictionaryList(length): # return new list of empty dictionaries  #TODO make data just a list
    l = []
    for x in range(1, length + 1):
        l.append({})
    
    return l

def invert(d): # returns new dictionary of inverted key/value pairs in dictionary d
    return {v: k for k, v in d.items()}

# Global Vars
url = "https://s3.amazonaws.com/tcmg476/http_access_log"
fileName = "http.log"
data = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}, 10: {}, 11: {}, 12:{}} # represents the year of data, key = monthNum, value = dictionary of events on each day
monthInt = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec':12} # TODO: make 0-11
monthName = invert(monthInt)

# Downloads http log to "http.log"
def getDataFile(): 
    with open(fileName, 'wb') as logFile: # creates a new http.log file
        with urlopen(url) as stream: # connect to server
            fileSize = stream.length

            # https://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python
            print("Downloading \"%s\" (%s KB)..." % (fileName, fileSize / 1000))

            currentFileSize = 0
            blockSize = 8192
            while True: # loop through download (blockSize at a time), and write bytes to file
                buffer = stream.read(blockSize)
                if not buffer: # if at end of file
                    break

                currentFileSize += len(buffer) # track how many bytes downloaded so far
                logFile.write(buffer)
                status = r"%10d [%3.2f%%]" % (currentFileSize, currentFileSize*100. / fileSize) # displays percentage downloaded
                status = status + chr(8)*(len(status) + 1)

                print(status, end="") # prints without appended "\n"
            
            print("", end="\n") # reset print appended char

# Sorts logs by date in the "data" dictionary.  
def parseLog():
    with open(fileName, 'r') as logFile: #opens http.log file
        print("Parsing Data File...")

        currline = 0
        badParses = [] # list of all failed parses
        for line in logFile: # iterate through entire log file
            currline += 1 
            splitData = re.split('.*\[(.*?):.*\] \".* (.*) .*\" (\d{3})', line)

            if len(splitData) == 5: # If regex worked:
                dateSplit = splitData[1].split('/') # splits up day/month/year string
                date = datetime.date(int(dateSplit[2]), monthInt[dateSplit[1]], int(dateSplit[0]))
                logData = {'date': date, 'name':splitData[2], 'code':splitData[3]} #TODO: Add key for all data

                if date.day in data[date.month]: # if logs list has already been created for that day
                    data[date.month][date.day].append(logData) # append dictionary containing log data
                else:
                    data[date.month][date.day] = [logData] # otherwise add to month dictionary, key = day, value = logData
            else: # If regex didn't work:
                badParses.append(splitData) # add to list of failures

        print(str(len(badParses)) + " lines couldn't be parsed.") #TODO: save bad parses to file

            

def main():
    if not os.path.exists(fileName):  # check if file exists before re-downloading
        print("No cached " + fileName + " found.\nDownloading from: " + url)
        getDataFile() # Saves file as http.log
    else:
        print("Using cached " + fileName + " file.")
       
        parseLog() # sorts logs by date in data dictionary

        # Main loop - goes through data dictionary, keeping track of stats
        print("Events Per Month/Day/Week:")
        for monthNum, month in data.items(): # for each dictionary in data
            print(monthName[monthNum] + ":") # prints name of month
            for dayNum, logs in month.items(): # for each dictionary in month
                print("\t" + str(dayNum) + ": " + str(len(logs)) + " events ocurred.")


if __name__ == "__main__":
    main()