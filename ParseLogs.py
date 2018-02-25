from urllib.request import urlopen
import os

def main():
    url = "https://s3.amazonaws.com/tcmg476/http_access_log"
    fileName = url.split('/')[-1]
    logFile = open(fileName, 'wb')

    # Download Log File (with progress bar)
    # https://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python
    with urlopen(url) as stream:
        metaData = dict(stream.getheaders())
        fileSize = int(metaData["Content-Length"])


        print(fileSize)
        print("Downloading \"%s\" (%s KB)" % (fileName, fileSize / 1000))

        currentFileSize = 0
        blockSize = 8192
        while currentFileSize/1000 < 10000:
            buffer = stream.read(blockSize)
            if not buffer:
                break

            currentFileSize += len(buffer)
            logFile.write(buffer)
            status = r"%10d [%3.2f%%]" % (currentFileSize, currentFileSize*100. / fileSize)
            status = status + chr(8)*(len(status) + 1)

            print(status, end="")

    logFile.close()

if __name__ == "__main__":
    main()