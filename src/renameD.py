import argparse
import time
import inotify.adapters
import inotify.constants
import os
import re
import shutil

def parseArguments():
    parser = argparse.ArgumentParser(description='Main Argument Parser')
    parser.add_argument('--src', dest='directorySrc', nargs=1, required=True,
            help='The source directory where to search for files to rename')
    parser.add_argument('--dst', dest='directoryDst', nargs=1, required=False,
            help='The destination directory where to move files that have ' +
            'renamed')
    parser.add_argument('--dry', dest='dryRun', action='store_true',
            help='Dry run, do not rename, or move anything. Print each rename' +
            'and move that would occur')
    parser.add_argument('--poll', dest='pollOnly', action='store_true',
            help='Use polling instead of inotify')
    parsed_args = parser.parse_args()
    parsed_args.directorySrc = os.path.abspath(parsed_args.directorySrc[0])
    parsed_args.directoryDst = os.path.abspath(parsed_args.directoryDst[0])
    return parsed_args

def checkSanityDir(dirSrc, dirDst):
    # Check src existence
    if os.path.isdir(dirSrc) is not True:
        print ('Source directory: ' + dirSrc + ' does not exist')
        return False;

    # Check dst existence
    if os.path.isdir(dirDst) is not True:
        print ('Destination directory: ' + dirDst + ' does not exist')
        return False;

    # Check src permission existence
    if not os.access(dirSrc, os.W_OK):
        print ('Source directory: ' + dirSrc + ' does not exist')
        return False;

    # Check dest permission existence
    if not os.access(dirDst, os.W_OK):
        print ('Destination directory: ' + dirDst + ' does not exist')
        return False;

    # All set
    return True

def notificationLoop(directorySrc, directoryDst, dryRun):
    i = inotify.adapters.Inotify()
    i.add_watch(directorySrc, mask=inotify.constants.IN_MOVED_TO)

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event
        sourceFilePath = os.path.join(path, filename)
        renamedFilePath = renameFile(directorySrc, directoryDst, sourceFilePath)
        if renamedFilePath == None:
            continue
        if not checkSanityDir(directorySrc, directoryDst):
            print ('Failed sanity check, skipping this file..')
            continue
        print ('Moved: '  + sourceFilePath + ' to: ' + renamedFilePath)
        if (dryRun == True):
            continue
        shutil.move(sourceFilePath, renamedFilePath)
#        print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(path, filename, type_names))
    print ('Exit')

def pollLoop(directorySrc, directoryDst, dryRun):
    while(True):
        print ("Sleeping..")
        time.sleep(5)
        if not checkSanityDir(directorySrc, directoryDst):
            print ("Sanity not confirmed..")
            continue
        singleRun(directorySrc, directoryDst, dryRun)

def renameFile(directorySrc, directoryDst, path):
    fileName = os.path.basename(path)
    fileExt  = os.path.splitext(fileName)[1]
    renamedFile = ""

    if not fileName.startswith("IMG_20") and not fileName.startswith("VID_20"):
        print ('Skipping unintelligible file name: ' + path)
        return None

    if len(fileName) < 18:
        print ('Skipping irrationally short file name: ' + path)
        return None

    renamedFile = removePrefixAndInsertPeriods(fileName)
    renamedFilePath = ''
    if fileExt.lower() == ".jpeg" or fileExt.lower() == ".jpg" or fileExt.lower() == ".dng":
        # Rename image files but keep them in the source directory
        renamedFilePath = os.path.join(directorySrc, renamedFile)

    elif fileExt.lower() == ".mp4":
        # Rename video files but move them in the destination directory
        renamedFilePath = os.path.join(directoryDst, renamedFile)
    else:
        print ('Skipping unintelligible file extension: ' + path)
        return None

    return renamedFilePath

def removePrefixAndInsertPeriods(fileName):
    noPrefix = fileName[6:]
    noPrefix = re.sub(r'([0-9][0-9])([0-9][0-9])([0-9][0-9])(.*)', r'\1.\2.\3\4', noPrefix.rstrip())
    return noPrefix

def singleRun(directorySrc, directoryDst, dryRun):
    for fileName in os.listdir(directorySrc):
        fileName = os.path.join(directorySrc, fileName)
        newName = renameFile(directorySrc, directoryDst, fileName)
        if newName == None:
            continue
        if (dryRun == False):
            shutil.move(fileName, newName)
        print ('Moved: '  + fileName + ' to: ' + newName)

def main():
  print('Hello, world!')
  args = parseArguments()
  while (checkSanityDir(args.directorySrc, args.directoryDst) == False):
        print ('Failed sanity check, looping..')
        time.sleep(5)

  singleRun(args.directorySrc, args.directoryDst, args.dryRun)
  if args.pollOnly:
      pollLoop(args.directorySrc, args.directoryDst, args.dryRun)
  else:
      notificationLoop(args.directorySrc, args.directoryDst, args.dryRun)

if __name__ == '__main__':
  main()
