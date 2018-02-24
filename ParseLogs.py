import urllib2
import os

def main():
    url = "https://s3.amazonaws.com/tcmg476/http_access_log"

    fileName = url.split('/')[-1]
    logFile = open(fileName, 'wb')
    u = urllib2.urlopen(url)
    metaData = u.info()
    fileSizeKB = int(metaData.getheaders("Content-Length")[0]) / 1000

    print("Downloading \"%s\" (%s KB)" % (fileName, fileSizeKB))



if __name__ == "__main__":
    main()