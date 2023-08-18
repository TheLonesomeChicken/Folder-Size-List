import os, threading

# Folder class

class Folder:
    path = ""
    size = 0
    lock = threading.Lock()

    def __init__(self, path):
        self.path = path

    def getFolderSize(self):
        fileThreads = []
        for path, dirs, files in os.walk(self.path):
            fileThreads.append(threading.Thread(target=self.addFilesToSize, args=(path, files,)))
            fileThreads[fileThreads.__len__() - 1].start()

        for fileThread in fileThreads:
            fileThread.join()

    def addFilesToSize(self, path, files):
        for file in files:
            self.lock.acquire()
            self.size += os.path.getsize(os.path.join(path, file))
            self.lock.release()

# folder defs

def subfolderAdd(subfolders, newSubfolder):
    newSubfolder.getFolderSize()

    if (subfolders.__len__() == 0):
        subfolders.append(newSubfolder)
        return

    if (newSubfolder.size <= subfolders[subfolders.__len__() - 1].size):
        subfolders.append(newSubfolder)
        return
            
    for i, subfolder in enumerate(subfolders):
        if (newSubfolder.size > subfolder.size):
            subfolders.insert(i, newSubfolder)
            break

def getAllFolderSizes(filePath):
    subfolders = []
    searchThreads = []

    for dir in os.listdir(filePath):
        if os.path.isfile(os.path.join(filePath, dir)):
            continue

        newSubfolder = Folder(os.path.join(filePath, dir))
        searchThreads.append(threading.Thread(target=subfolderAdd, args=(subfolders, newSubfolder,)))
        searchThreads[searchThreads.__len__() - 1].start()

    for searchThread in searchThreads:
        searchThread.join()

    return subfolders

# main

allFolderSizes = getAllFolderSizes(os.getcwd())

for subfolder in allFolderSizes:
    print(f"{subfolder.path.removeprefix(os.getcwd())} ({subfolder.size} bytes / {subfolder.size / 1000000000} GB)")