from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QByteArray
from PyQt5.QtGui import QPixmap
import sys, os, random, DragFrame, collections, io, PIL
from mutagen.id3 import ID3
from PIL import Image
import pygame.mixer as mx



class Kyouko_(QtWidgets.QWidget):
    def __init__(self, stylesheet):
        #initialize
        app = QApplication(sys.argv)
        super().__init__()
        mx.init(frequency=44100, size=-16, channels=2, buffer=512, devicename=None)
        self.setStyleSheet(stylesheet)
        self.bareboneSetUp(app)
        self.panelSetUp()
        self.show()
        sys.exit(app.exec_())

#-------------------------------------------Initialization-------------------------------------#
    #window setup----------------------------------------------------------
    def bareboneSetUp(self, app):
            #window size, posiition
        screen = app.primaryScreen()
        self.setGeometry(screen.size().width()//2-400, screen.size().height()//2-400, 800, 800)
            #layout
        self.__layout = QtWidgets.QGridLayout()
        self.setLayout(self.__layout)
        self.__layout.setContentsMargins(0,0,0,0)
        self.__layout.setSpacing(0)
            #scroll list
        self.__scrollList = QtWidgets.QScrollArea()
        self.__layout.addWidget(self.__scrollList, 0, 0, 10, 3)
            #Cover display
        self.__album = QtWidgets.QLabel()
        self.__layout.addWidget(self.__album, 0, 3, 7, 7)
            #Control panel
        self.__panel = QtWidgets.QWidget()
        self.__panel.setObjectName("panel")
        self.__layout.addWidget(self.__panel, 7, 3, 3, 7)
            #Other
        self.DragFrame = DragFrame.DragFrame()
        self.DragFrame.songPath.connect(self.loadSong)
        self.DragFrame.dicChange.connect(self.changeSongList)



    #Panel setup-----------------------------------------------------------
    def panelSetUp(self):
            #Panel layout
        self.__panelLayout = QtWidgets.QHBoxLayout()
        self.__panel.setLayout(self.__panelLayout)

            #load songlist
        self.__buttonLoad = QtWidgets.QPushButton("Load")
        self.__buttonLoad.clicked.connect(self.scrollListSetUP)
        self.__panelLayout.addWidget(self.__buttonLoad)

    
    #Scroll List setup-----------------------------------------------------
    def scrollListSetUP(self):
        songs = self.openFileNamesDialog()
        self.songList = collections.OrderedDict()
        if songs:
            for song in songs:
                self.songList[ID3(song).get("TIT2").__str__()] = song
            self.__scrollList.setWidget(self.DragFrame.generate(self.songList))
        


#-------------------------------------------User Functions-------------------------------------#
    #Set album image-------------------------------------------------------
    def setAlbum(self):
        size = self.__album.size()
        self.__album.setPixmap(QPixmap(r"C:\Users\203379015\OneDrive - Fulton County Schools\Desktop\New_Kyouko\pre\cache\cover.png").scaled(size.width(), size.height(), Qt.KeepAspectRatio))
        self.__album.setAlignment(Qt.AlignCenter)


#-----------------------------------------Program Functions------------------------------------#
    #Resize----------------------------------------------------------------
    def resizeEvent(self, event) -> None:
        self.__album.clear()

    #Open Mp3 folder-------------------------------------------------------
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","MP3 Files (*.mp3)", options=options)
        if files:
            return files
        
    #Song load-------------------------------------------------------------
    def loadSong(self, path):
        self.loadAlbum(path)
        mx.music.load(path)
        mx.music.play()

    #Set album-------------------------------------------------------------
    def loadAlbum(self, path):
        '''Load the cover of gaven mp3 file in self.__album'''
            #Get cover image bytearray
        coverstream = ID3(path).get("APIC:").data
        print(io.BytesIO(coverstream))
        album = QPixmap()
        if not album.loadFromData(coverstream, "JPEG"):
            album.loadFromData(coverstream, "PNG")

        size = self.__album.size()
        self.__album.setPixmap(album.scaled(size.width(), size.height(), Qt.KeepAspectRatio))
        self.__album.setAlignment(Qt.AlignCenter)

    #SongList change-------------------------------------------------------
    def changeSongList(self, dic):
        self.songList = dic
        print(dic)




if __name__ == "__main__":
    if not os.path.exists(os.getcwd()+"/pre/cache"):
            os.makedirs(os.getcwd()+"/pre/cache")

    stylesheet = '''
        QScrollArea {
            background-color: black;
        }
        QLabel {
            background-color: blue;
        }
        QWidget#panel {
            background-color: orange
        }
    '''
    x = Kyouko_(stylesheet)
    
