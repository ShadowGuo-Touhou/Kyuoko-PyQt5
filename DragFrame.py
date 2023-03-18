from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSize, QMimeData, pyqtSignal
from PyQt5.QtGui import QDrag, QPixmap
import collections


class DragButton(QtWidgets.QPushButton):
    signal = pyqtSignal(str, name="path")
    def __init__(self, text=str, content=str, parent=None) -> None:
        super().__init__(text=text, parent=parent)
        self.setAcceptDrops(True)
        self.setObjectName("DragButtons")
        self.path = content
        self.name = text

    def mousePressEvent(self, event):
        if event.button() != Qt.RightButton:
            return
        #Creat drag object and button's mime data
        drag = QDrag(self)
        mime = QMimeData()
        drag.setMimeData(mime)

        #Generate a pixmap while draging
        Pixmap = QPixmap(self.size())
        self.render(Pixmap)
        drag.setPixmap(Pixmap)

        drag.exec_(Qt.MoveAction)
        
        
    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        self.signal.emit(self.path)
        
    @property
    def getSong(self):
        return self.name
    @property
    def getPath(self):
        return self.path


class DragFrame(QWidget):
    songPath = pyqtSignal(str)
    dicChange = pyqtSignal(dict)

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(Qt.AlignVCenter)
        self.setLayout(self.layout)



    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        sourceWidget = event.source()
        position = event.pos()
        dic = collections.OrderedDict()
        
        for n in range(self.layout.count()):
            #Get the widget at each index
            widgetAt = self.layout.itemAt(n).widget()
            #Switch the position of two button if cursor is on one
            print(widgetAt.pos().x(), widgetAt.pos().y(), position.x(), position.y())
            if widgetAt.pos().x() < position.x() <widgetAt.pos().x()+widgetAt.size().width() and widgetAt.pos().y()<position.y()<widgetAt.pos().y()+widgetAt.size().height():
                self.layout.insertWidget(n, sourceWidget)
                break

        for n in range(self.layout.count()):
            widgetAt = self.layout.itemAt(n).widget()
            dic[widgetAt.getSong] = widgetAt.getPath
        
        self.dicChange.emit(dic)
        event.accept()
    
    def songClicked(self, value):
        self.songPath.emit(value)
        

    def generate(self, dic) -> QWidget:
        '''
        This function takes in a dictionary and generate a Qwidgets corresponding content
        '''
        self.clear()
        for n in dic:
            temp = DragButton(n, dic[n])
            temp.setMinimumWidth(150)
            #temp.setMaximumWidth(250)
            temp.signal.connect(self.songClicked)
            self.layout.addWidget(temp)
        return self
    
    def clear(self):
        for n in range(self.layout.count()):
            self.layout.removeWidget(self.layout.itemAt(0).widget())