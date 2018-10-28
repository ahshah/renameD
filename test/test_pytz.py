import pytz
import datetime
from pyfakefs import fake_filesystem_unittest
import pytest
import sys, os, mock
import pytest
from collections import namedtuple
from pyfakefs import fake_filesystem_unittest
import CommonUtils
import pytz

SRC_PATH = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(SRC_PATH, '../src/')
sys.path.append(SRC_PATH)
from renameD import checkSanityDir
from renameD import removePrefixAndInsertPeriods
from renameD import renameFile
from renameD import singleRun
from renameD import notificationLoop
from renameD import pollLoop
from renameD import main

class TestExample(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        self.dirSrc = '/mnt/src'
        self.dirDst = '/mnt/dst'
        self.fileListImage =['IMG_20180923_185307.jpg', 'IMG_20180923_185308.jpg', 'IMG_20180923_185400.dng', 'IMG_20180923_185400.jpg', 'IMG_20180923_185402.dng', 'IMG_20180923_185402.jpg', 'IMG_20180923_185601.jpg', 'IMG_20180923_185620.jpg', 'IMG_20180923_185635.jpg', 'IMG_20180923_185638.jpg', 'IMG_20180923_185835.jpg', 'IMG_20180923_185836.jpg', 'IMG_20180924_212923.jpg', 'IMG_20180924_212927.jpg', 'IMG_20180925_100542.jpg', 'IMG_20180925_101918.jpg', 'IMG_20180925_131351.jpg', 'IMG_20180925_205314.jpg', 'IMG_20180925_205319.jpg', 'IMG_20180925_210045.jpg', 'IMG_20180925_210047.jpg', 'IMG_20180925_210109.jpg', 'IMG_20180925_210113.jpg', 'IMG_20180926_151419.jpg', 'IMG_20180926_151428.jpg', 'IMG_20180926_151431.jpg', 'IMG_20180926_151435.jpg', 'IMG_20180926_151438.jpg', 'IMG_20180929_224250.jpg', 'IMG_20180929_224255.jpg', 'IMG_20180930_000320.jpg', 'IMG_20181009_005657.jpg', 'IMG_20181011_161955.jpg', 'IMG_20181011_194852.jpg', 'IMG_20181011_194853.jpg']
        self.fileListImageResult = sorted(['18.09.23_185307.jpg', '18.09.23_185308.jpg', '18.09.23_185400.dng', '18.09.23_185400.jpg', '18.09.23_185402.dng', '18.09.23_185402.jpg', '18.09.23_185601.jpg', '18.09.23_185620.jpg', '18.09.23_185635.jpg', '18.09.23_185638.jpg', '18.09.23_185835.jpg', '18.09.23_185836.jpg', '18.09.24_212923.jpg', '18.09.24_212927.jpg', '18.09.25_100542.jpg', '18.09.25_101918.jpg', '18.09.25_131351.jpg', '18.09.25_205314.jpg', '18.09.25_205319.jpg', '18.09.25_210045.jpg', '18.09.25_210047.jpg', '18.09.25_210109.jpg', '18.09.25_210113.jpg', '18.09.26_151419.jpg', '18.09.26_151428.jpg', '18.09.26_151431.jpg', '18.09.26_151435.jpg', '18.09.26_151438.jpg', '18.09.29_224250.jpg', '18.09.29_224255.jpg', '18.09.30_000320.jpg', '18.10.09_005657.jpg', '18.10.11_161955.jpg', '18.10.11_194852.jpg', '18.10.11_194853.jpg'])
        self.fileListVideo =['VID_20180923_185307.mp4', 'VID_20180923_185308.mp4', 'VID_20180923_185400.MP4', 'VID_20180923_185400.mp4', 'VID_20180923_185402.MP4', 'VID_20180923_185402.mp4', 'VID_20180923_185601.mp4', 'VID_20180923_185620.mp4', 'VID_20180923_185635.mp4', 'VID_20180923_185638.mp4', 'VID_20180923_185835.mp4', 'VID_20180923_185836.mp4', 'VID_20180924_212923.mp4', 'VID_20180924_212927.mp4', 'VID_20180925_100542.mp4', 'VID_20180925_101918.mp4', 'VID_20180925_131351.mp4', 'VID_20180925_205314.mp4', 'VID_20180925_205319.mp4', 'VID_20180925_210045.mp4', 'VID_20180925_210047.mp4', 'VID_20180925_210109.mp4', 'VID_20180925_210113.mp4', 'VID_20180926_151419.mp4', 'VID_20180926_151428.mp4', 'VID_20180926_151431.mp4', 'VID_20180926_151435.mp4', 'VID_20180926_151438.mp4', 'VID_20180929_224250.mp4', 'VID_20180929_224255.mp4', 'VID_20180930_000320.mp4', 'VID_20181009_005657.mp4', 'VID_20181011_161955.mp4', 'VID_20181011_194852.mp4', 'VID_20181011_194853.mp4']
        self.fileListVideoResult= sorted(['18.09.23_185307.mp4', '18.09.23_185308.mp4', '18.09.23_185400.MP4', '18.09.23_185400.mp4', '18.09.23_185402.MP4', '18.09.23_185402.mp4', '18.09.23_185601.mp4', '18.09.23_185620.mp4', '18.09.23_185635.mp4', '18.09.23_185638.mp4', '18.09.23_185835.mp4', '18.09.23_185836.mp4', '18.09.24_212923.mp4', '18.09.24_212927.mp4', '18.09.25_100542.mp4', '18.09.25_101918.mp4', '18.09.25_131351.mp4', '18.09.25_205314.mp4', '18.09.25_205319.mp4', '18.09.25_210045.mp4', '18.09.25_210047.mp4', '18.09.25_210109.mp4', '18.09.25_210113.mp4', '18.09.26_151419.mp4', '18.09.26_151428.mp4', '18.09.26_151431.mp4', '18.09.26_151435.mp4', '18.09.26_151438.mp4', '18.09.29_224250.mp4', '18.09.29_224255.mp4', '18.09.30_000320.mp4', '18.10.09_005657.mp4', '18.10.11_161955.mp4', '18.10.11_194852.mp4', '18.10.11_194853.mp4'])

        pass

    def test_sanity(self):
        try:
            tz = pytz.timezone('America/New_York')
        except pytz.exceptions.UnknownTimeZoneError:
            tz = pytz.timezone('UTC')

        return datetime.datetime.now().astimezone(tz).strftime("%a, %b %d, %Y %I:%M:%S %p")
        print(eastern)
