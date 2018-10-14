import sys, os, mock
import pytest
from pyfakefs import fake_filesystem_unittest

SRC_PATH = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(SRC_PATH, '../src/')
sys.path.append(SRC_PATH)
from rename import checkSanityDir
from rename import removePrefixAndInsertPeriods
from rename import renameFile
from rename import singleRun
from rename import notificationLoop

# Seen on drusus
# PATH=[/home/user/mount] FILENAME=[IMG-20181012-WA0007.jpg] EVENT_TYPES=['IN_MOVED_TO']

def func(x):
    return x + 1

class TestExample(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        self.dirSrc = '/mnt/src'
        self.dirDst = '/mnt/dst'
        self.fileListImage =['IMG_20180923_185307.jpg', 'IMG_20180923_185308.jpg', 'IMG_20180923_185400.dng', 'IMG_20180923_185400.jpg', 'IMG_20180923_185402.dng', 'IMG_20180923_185402.jpg', 'IMG_20180923_185601.jpg', 'IMG_20180923_185620.jpg', 'IMG_20180923_185635.jpg', 'IMG_20180923_185638.jpg', 'IMG_20180923_185835.jpg', 'IMG_20180923_185836.jpg', 'IMG_20180924_212923.jpg', 'IMG_20180924_212927.jpg', 'IMG_20180925_100542.jpg', 'IMG_20180925_101918.jpg', 'IMG_20180925_131351.jpg', 'IMG_20180925_205314.jpg', 'IMG_20180925_205319.jpg', 'IMG_20180925_210045.jpg', 'IMG_20180925_210047.jpg', 'IMG_20180925_210109.jpg', 'IMG_20180925_210113.jpg', 'IMG_20180926_151419.jpg', 'IMG_20180926_151428.jpg', 'IMG_20180926_151431.jpg', 'IMG_20180926_151435.jpg', 'IMG_20180926_151438.jpg', 'IMG_20180929_224250.jpg', 'IMG_20180929_224255.jpg', 'IMG_20180930_000320.jpg', 'IMG_20181009_005657.jpg', 'IMG_20181011_161955.jpg', 'IMG_20181011_194852.jpg', 'IMG_20181011_194853.jpg']
        self.fileListImageResult = sorted(['18.09.23_185307.jpg', '18.09.23_185308.jpg', '18.09.23_185400.dng', '18.09.23_185400.jpg', '18.09.23_185402.dng', '18.09.23_185402.jpg', '18.09.23_185601.jpg', '18.09.23_185620.jpg', '18.09.23_185635.jpg', '18.09.23_185638.jpg', '18.09.23_185835.jpg', '18.09.23_185836.jpg', '18.09.24_212923.jpg', '18.09.24_212927.jpg', '18.09.25_100542.jpg', '18.09.25_101918.jpg', '18.09.25_131351.jpg', '18.09.25_205314.jpg', '18.09.25_205319.jpg', '18.09.25_210045.jpg', '18.09.25_210047.jpg', '18.09.25_210109.jpg', '18.09.25_210113.jpg', '18.09.26_151419.jpg', '18.09.26_151428.jpg', '18.09.26_151431.jpg', '18.09.26_151435.jpg', '18.09.26_151438.jpg', '18.09.29_224250.jpg', '18.09.29_224255.jpg', '18.09.30_000320.jpg', '18.10.09_005657.jpg', '18.10.11_161955.jpg', '18.10.11_194852.jpg', '18.10.11_194853.jpg'])
        self.fileListVideo =['VID_20180923_185307.mp4', 'VID_20180923_185308.mp4', 'VID_20180923_185400.MP4', 'VID_20180923_185400.mp4', 'VID_20180923_185402.MP4', 'VID_20180923_185402.mp4', 'VID_20180923_185601.mp4', 'VID_20180923_185620.mp4', 'VID_20180923_185635.mp4', 'VID_20180923_185638.mp4', 'VID_20180923_185835.mp4', 'VID_20180923_185836.mp4', 'VID_20180924_212923.mp4', 'VID_20180924_212927.mp4', 'VID_20180925_100542.mp4', 'VID_20180925_101918.mp4', 'VID_20180925_131351.mp4', 'VID_20180925_205314.mp4', 'VID_20180925_205319.mp4', 'VID_20180925_210045.mp4', 'VID_20180925_210047.mp4', 'VID_20180925_210109.mp4', 'VID_20180925_210113.mp4', 'VID_20180926_151419.mp4', 'VID_20180926_151428.mp4', 'VID_20180926_151431.mp4', 'VID_20180926_151435.mp4', 'VID_20180926_151438.mp4', 'VID_20180929_224250.mp4', 'VID_20180929_224255.mp4', 'VID_20180930_000320.mp4', 'VID_20181009_005657.mp4', 'VID_20181011_161955.mp4', 'VID_20181011_194852.mp4', 'VID_20181011_194853.mp4']
        self.fileListVideoResult= sorted(['18.09.23_185307.mp4', '18.09.23_185308.mp4', '18.09.23_185400.MP4', '18.09.23_185400.mp4', '18.09.23_185402.MP4', '18.09.23_185402.mp4', '18.09.23_185601.mp4', '18.09.23_185620.mp4', '18.09.23_185635.mp4', '18.09.23_185638.mp4', '18.09.23_185835.mp4', '18.09.23_185836.mp4', '18.09.24_212923.mp4', '18.09.24_212927.mp4', '18.09.25_100542.mp4', '18.09.25_101918.mp4', '18.09.25_131351.mp4', '18.09.25_205314.mp4', '18.09.25_205319.mp4', '18.09.25_210045.mp4', '18.09.25_210047.mp4', '18.09.25_210109.mp4', '18.09.25_210113.mp4', '18.09.26_151419.mp4', '18.09.26_151428.mp4', '18.09.26_151431.mp4', '18.09.26_151435.mp4', '18.09.26_151438.mp4', '18.09.29_224250.mp4', '18.09.29_224255.mp4', '18.09.30_000320.mp4', '18.10.09_005657.mp4', '18.10.11_161955.mp4', '18.10.11_194852.mp4', '18.10.11_194853.mp4'])
    def cleanUp(self, objectList):
        for o in objectList:
            self.fs.remove_object(o)

    def test_sanity(self):
        self.assertFalse(checkSanityDir('/mnt/src', '/mnt/dst'))
        self.fs.create_dir(self.dirSrc)
        self.fs.create_dir(self.dirDst)
        self.assertTrue(checkSanityDir('/mnt/src', '/mnt/dst'))

    def test_sanity_one_param_is_file(self):
        self.fs.create_file(self.dirSrc)
        self.fs.create_dir(self.dirDst)
        self.assertFalse(checkSanityDir('/mnt/src', '/mnt/dst'))
        self.cleanUp(('/mnt/src', '/mnt/dst'))

        self.fs.create_dir(self.dirSrc)
        self.fs.create_file(self.dirDst)
        self.assertFalse(checkSanityDir('/mnt/src', '/mnt/dst'))
        self.cleanUp(('/mnt/src', '/mnt/dst'))

    def test_sanity_one_dir_has_bad_perm(self):
        self.fs.create_dir('/mnt/')

        self.fs.create_dir(self.dirSrc, 000)
        self.fs.create_dir(self.dirDst)
        self.assertFalse(checkSanityDir('/mnt/src', '/mnt/dst'))
        self.cleanUp(('/mnt/src', '/mnt/dst'))

        self.fs.create_dir(self.dirSrc)
        self.fs.create_dir(self.dirDst, 000)
        self.assertFalse(checkSanityDir('/mnt/src', '/mnt/dst'))
        self.cleanUp(('/mnt/src', '/mnt/dst'))

        self.fs.create_dir(self.dirSrc, 222)
        self.fs.create_dir(self.dirDst, 222)
        self.assertTrue(checkSanityDir('/mnt/src', '/mnt/dst'))

    def test_RemovePrefixAndInsertPetartiods(self):
        noPrefix = removePrefixAndInsertPeriods('IMG_20181011_194852.jpg') 
        self.assertEqual(noPrefix, '18.10.11_194852.jpg')

        noPrefix = removePrefixAndInsertPeriods('VID_20181011_194852.mp4') 
        self.assertEqual(noPrefix, '18.10.11_194852.mp4')


    def test_RenameFile_fileDoesNotStartWithCorrectPrefix(self):
        ret = renameFile('/mnt/src/', '/mnt/dst', '/mnt/src/NMG_20181011_194852.jpg')
        self.assertEqual(ret, None)

    def test_RenameFile_fileDoesNotEndWithCorrectExtension(self):
        ret = renameFile('/mnt/src/', '/mnt/dst', '/mnt/src/IMG_20181011_194852.avi')
        self.assertEqual(ret, None)

    def test_RenameFile_fileNameIsTooShort(self):
        ret = renameFile('/mnt/src/', '/mnt/dst', '/mnt/src/IMG_20181011_.mp4')
        self.assertEqual(ret, None)

    def test_RenameFile_fileNameExtension_JPG(self):
        extension = '.JPG'
        expected = '/mnt/src/18.10.11_194852' + extension
        ret = renameFile('/mnt/src/', '/mnt/dst', '/mnt/src/IMG_20181011_194852' + extension)
        self.assertEqual(ret, expected)

    def test_RenameFile_fileNameExtension_JPEG(self):
        extension = '.JPEG'
        expected = '/mnt/src/18.10.11_194852' + extension
        ret = renameFile('/mnt/src/', '/mnt/dst', '/mnt/src/IMG_20181011_194852' + extension)
        self.assertEqual(ret, expected)

    def test_RenameFile_fileNameExtension_Jpg(self):
        extension = '.Jpg'
        expected = '/mnt/src/18.10.11_194852' + extension
        ret = renameFile('/mnt/src/', '/mnt/dst', '/mnt/src/IMG_20181011_194852' + extension)
        self.assertEqual(ret, expected)


    def test_RenameFile_fileNameExtension_jpg(self):
        extension = '.jpg'
        expected = '/mnt/src/18.10.11_194852' + extension
        ret = renameFile('/mnt/src/', '/mnt/dst', '/mnt/src/IMG_20181011_194852' + extension)
        self.assertEqual(ret, expected)

    def test_RenameFile_fileNameExtension_MP4(self):
        extension = '.MP4'
        expected = '/mnt/dst/18.10.11_194852' + extension
        ret = renameFile('/mnt/src/', '/mnt/dst', '/mnt/src/IMG_20181011_194852' + extension)
        self.assertEqual(ret, expected)

    def test_RenameFile_fileNameExtension_Mp4(self):
        extension = '.Mp4'
        expected = '/mnt/dst/18.10.11_194852' + extension
        ret = renameFile('/mnt/src/', '/mnt/dst', '/mnt/src/IMG_20181011_194852' + extension)
        self.assertEqual(ret, expected)

    def test_RenameFile_fileNameExtension_MP4(self):
        extension = '.mp4'
        expected = '/mnt/dst/18.10.11_194852' + extension
        ret = renameFile('/mnt/src/', '/mnt/dst', '/mnt/src/IMG_20181011_194852' + extension)
        self.assertEqual(ret, expected)

    def test_singleRun_dryRun(self):
        self.fs.create_dir(self.dirSrc)
        self.fs.create_dir(self.dirDst)
        for f in self.fileListImage:
            self.fs.create_file(os.path.join(self.dirSrc, f))

        singleRun(self.dirSrc, self.dirDst, dryRun=True)

        files = sorted([ f for f in os.listdir(self.dirSrc)])
        self.assertEqual(files, self.fileListImage)


    def test_singleRun(self):
        self.fs.create_dir(self.dirSrc)
        self.fs.create_dir(self.dirDst)
        for f in self.fileListImage:
            self.fs.create_file(os.path.join(self.dirSrc, f))

        singleRun(self.dirSrc, self.dirDst, dryRun=False)

        files = sorted([ f for f in os.listdir(self.dirSrc)])
        self.assertEqual(files, self.fileListImageResult)

    @mock.patch('rename.inotify.adapters.Inotify')
    def test_NotificationLoopWithImage(self, inotify):
        inotify.return_value.add_watch.return_value = None
        return_list = list()
        for f in self.fileListImage:
            x = ('a', 'b', self.dirSrc, f)
            return_list.append(x)
        inotify.return_value.event_gen.return_value = return_list
        self.fs.create_dir(self.dirDst)
        self.fs.create_dir(self.dirSrc)
        for f in self.fileListImage:
            self.fs.create_file(os.path.join(self.dirSrc, f))

        notificationLoop(self.dirSrc, self.dirDst, False)

        files = sorted([ f for f in os.listdir(self.dirSrc)])
        self.assertEqual(files, self.fileListImageResult)
        print('All done')

    @mock.patch('rename.inotify.adapters.Inotify')
    def test_NotificationLoopWithImageDryRun(self, inotify):
        inotify.return_value.add_watch.return_value = None
        return_list = list()
        for f in self.fileListImage:
            x = ('a', 'b', self.dirSrc, f)
            return_list.append(x)
        inotify.return_value.event_gen.return_value = return_list
        self.fs.create_dir(self.dirDst)
        self.fs.create_dir(self.dirSrc)
        for f in self.fileListImage:
            self.fs.create_file(os.path.join(self.dirSrc, f))

        notificationLoop(self.dirSrc, self.dirDst, True)

        files = sorted([ f for f in os.listdir(self.dirSrc)])
        self.assertEqual(files, self.fileListImage)
        print('All done')

    @mock.patch('rename.inotify.adapters.Inotify')
    def test_NotificationLoopWithVideo(self, inotify):
        inotify.return_value.add_watch.return_value = None
        return_list = list()
        for f in self.fileListVideo:
            x = ('a', 'b', self.dirSrc, f)
            return_list.append(x)
        inotify.return_value.event_gen.return_value = return_list
        self.fs.create_dir(self.dirDst)
        self.fs.create_dir(self.dirSrc)
        for f in self.fileListVideo:
            self.fs.create_file(os.path.join(self.dirSrc, f))

        notificationLoop(self.dirSrc, self.dirDst, False)

        files = sorted([ f for f in os.listdir(self.dirDst)])
        self.assertEqual(files, self.fileListVideoResult)
        print('All done')
