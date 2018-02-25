from urllib.request import urlopen
import os

url = "https://s3.amazonaws.com/tcmg476/http_access_log"
fileName = "http.log"

def getDataFile(): 
    with open(fileName, 'wb') as logFile:
        with urlopen(url) as stream:
            fileSize = stream.length

            # https://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python
            print("Downloading \"%s\" (%s KB)..." % (fileName, fileSize / 1000))

            currentFileSize = 0
            blockSize = 8192
            while currentFileSize < fileSize:
                buffer = stream.read(blockSize)
                if not buffer:
                    break

                currentFileSize += len(buffer)
                logFile.write(buffer)
                status = r"%10d [%3.2f%%]" % (currentFileSize, currentFileSize*100. / fileSize)
                status = status + chr(8)*(len(status) + 1)

                print(status, end="")
            
            print("", end="\n") # reset print trailing char


def main():
    # check if file exists before re-downloading
    if not os.path.exists(fileName):
        print("No cached " + fileName + " found.\nDownloading from: " + url)
        getDataFile()
    else:
        print("Using cached " + fileName + " file.")
    
    with open(fileName, 'rb') as logFile:
        print("parse")
        
     

if __name__ == "__main__":
    main()