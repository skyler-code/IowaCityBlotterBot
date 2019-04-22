import os
import time
from datetime import datetime, timedelta

LOG_DIRECTORY = "logs/"
CACHE_DIRECTORY = "cache/"
SETTINGS_FILE = "settings.txt"
IC_ROOT_URL = 'https://www.iowa-city.org/icgovapps/police/'
DATE_STAMP_HOUR_DELAY = 5


class settings:
    def __init__(self):
        pass

    def getDispatchFileName(self) -> str:
        return "%s/%s.txt" % (CACHE_DIRECTORY, self.getDateStamp())

    def fetchOldDispatchIds(self) -> list:
        returnIds = []
        dispatchFileName = self.getDispatchFileName()
        self.deleteOldDispatchIds()
        try:
            if not os.path.exists(CACHE_DIRECTORY):
                os.makedirs(CACHE_DIRECTORY)
            f = open(dispatchFileName, "r")
            if f.readable():
                text: str = f.read()
                if(len(text) > 0):
                    returnIds = text.split(',')
            f.close()
        except:
            pass
        return returnIds

    def saveDispatchId(self, dispatchId: str):
        f = open(self.getDispatchFileName(), "a")
        if f.writable():
            f.write("%s," % (dispatchId))
        f.close()

    def deleteOldDispatchIds(self):
        current_time = time.time()
        for f in os.listdir(CACHE_DIRECTORY):
            fileName = "%s%s" % (CACHE_DIRECTORY, f)
            creation_time = os.path.getctime(fileName)
            if (current_time - creation_time) // (24 * 3600) >= 2:
                os.unlink(fileName)
                print('{} removed'.format(fileName))

    def getSettings(self):
        f = open(SETTINGS_FILE, "r")
        if f.readable():
            return eval(f.read())
        f.close()

    def getListUrl(self, date: str) -> str:
        return "%sactivitylog?activityDate=%s" % (IC_ROOT_URL, date)

    def getDispatchUrl(self, dispatchId: str) -> str:
        return "%sdetails?dispatchNumber=%s" % (IC_ROOT_URL, dispatchId)

    def printWithStamp(self, inputStr: str):
        st = datetime.now().strftime('%H:%M:%S')
        outputStr = "[%s]: %s" % (st, inputStr)
        self.addToLog(outputStr)
        print(outputStr)

    def addToLog(self, logMessage: str):
        logDirectory = self.getLogDirectory()
        if not os.path.exists(logDirectory):
            os.makedirs(logDirectory)
        today = self.getDate().day
        if(today < 10):
            today = "0%s" % (today)
        f = open("%s%s.txt" % (logDirectory, today), "a")
        if f.writable():
            f.write(logMessage + "\n")
        f.close()

    def getDate(self) -> datetime:
        return (datetime.now() - timedelta(hours=DATE_STAMP_HOUR_DELAY))

    def getDateStamp(self) -> str:
        return self.getDate().strftime('%m-%d-%Y')

    def getLogDirectory(self) -> str:
        date = self.getDate()
        month = date.month
        if(month < 10):
            month = "0%s" % (month)
        return '%s%s/%s/' % (LOG_DIRECTORY, date.year, month)
