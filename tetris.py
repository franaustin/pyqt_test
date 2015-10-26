# -*- coding: utf-8 -*-
'''
Created on 2015-8-19
@author: 
@subject: tetris
'''
"""
ZetCode PyQt4 tutorial 
This is a Tetris game clone.
author: Jan Bodnar
website: zetcode.com 
last edited: October 2013
"""
import os
import sys, random
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QTextCodec
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))  

class Tetris(QtGui.QMainWindow):
    
    def __init__(self):
        super(Tetris, self).__init__()
        
        self.initGame()
        
    def initUI(self):
        ''''''
        
    def initGame(self):    
        ''''''
        self.tboard = Board(self)
        self.setCentralWidget(self.tboard)

        self.statusbar = self.statusBar()        
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)
#        
        self.tboard.start()
#        
        self.resize(180, 380)
        self.center()
        self.createMenus()
        self.setWindowTitle('Tetris')        
        self.show()
        self.tboard.pause()
#        

    def center(self):
        
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, 
            (screen.height()-size.height())/2)
        
    def createMenus(self):  
        self.aboutAction=QtGui.QAction(self.tr("&About"),self)  
        self.connect(self.aboutAction,QtCore.SIGNAL("triggered()"),self.slotAbout)  
        self.keysAction=QtGui.QAction(self.tr("&Keys"),self)  
        self.connect(self.keysAction,QtCore.SIGNAL("triggered()"),self.slotKeys) 
        self.updateAction=QtGui.QAction(self.tr("&Check for updates"),self)  
        self.connect(self.updateAction,QtCore.SIGNAL("triggered()"),self.slotupdate) 
                 
        aboutMenu=self.menuBar().addMenu(self.tr("&help"))  
        aboutMenu.addAction(self.aboutAction) 
        aboutMenu.addAction(self.keysAction) 
        aboutMenu.addAction(self.updateAction)       

    def slotAbout(self):  
        version = getFileVersion(getSelfPath())
        version_block = '''***** Version: %s *****'''%version
        QtGui.QMessageBox.about(self,"about me",self.tr('''A neurologist, don't know where to get a gun. 
He went to a dark alley, soon, a young man, he walked in, 
and without a gun to his head on the ground, asked: "1 + 1 =?" 
Young people think for a long time, 
said: "2" mental derangement not hesitate shot and killed him, 
and dragged into the gun, cold and said: "you know too much."
%s'''%version_block))
                     
    def slotKeys(self): 
        QtGui.QMessageBox.about(self,"keys",self.tr('''p - pause|start 
↑ - Switch
↓ - Switch 
← - left 
→ - right
        '''))   
    
    def slotupdate(self):
        ''' check for updates '''
        RAddress = 'http://10.118.13.41:6678' 
        customMsgBox=QtGui.QMessageBox(self)  
        customMsgBox.setWindowTitle("check for updates")  
        customMsgBox.setText(self.tr("Checks if newer version is available.")) 
        customMsgBox.setInformativeText('RemoteAddress:%s'%RAddress)
        #customMsgBox.setDetailedText('Remote Address:')
        lockButton=customMsgBox.addButton(self.tr("更新"),QtGui.QMessageBox.ActionRole)  
        customMsgBox.exec_()  
  
        remoteaddress = None
        button=customMsgBox.clickedButton()  
        if button==lockButton:  
            infotext = customMsgBox.informativeText()
            if not infotext.contains('//'):
                name,ok=QtGui.QInputDialog.getText(self,self.tr("setting"),
                                             self.tr("RemoteAddress:"),
                                             QtGui.QLineEdit.Normal,
                                             '')
                  
                if ok and name.contains('//'):  
                    customMsgBox.setInformativeText('RemoteAddress:%s'%name)
                    self.tboard.msg2Statusbar[str].emit("updating...")
                    remoteaddress = unicode(customMsgBox.informativeText().toUtf8(), 'utf-8', 'ignore')
                    remoteaddress = remoteaddress.split('RemoteAddress:')[-1]
                else:
                    self.tboard.msg2Statusbar[str].emit("RemoteAddress is illegal")
            else:
                self.tboard.msg2Statusbar[str].emit("updating...")
                remoteaddress = unicode(customMsgBox.informativeText().toUtf8(), 'utf-8', 'ignore')
                remoteaddress = remoteaddress.split('RemoteAddress:')[-1] 

            
            if remoteaddress:
                results = checkupdates(remoteaddress)
                newfn = results.get('file_name','')
                old_fp = getSelfPath() 
                if newfn:
                    QtCore.QCoreApplication.instance().quit()
                    command = '"%s"'%newfn 
                    QtCore.QFile.remove(old_fp)
                    process = QtCore.QProcess()
                    process.startDetached(command)

            #QtCore.QCoreApplication.instance().quit()     
            #QtGui.qApp.quit
            
#        #*********记录测试点，及时删除***********
#        import sys
#        import datetime
#        sys.stdout=open('E:/tetris_log.log','a')
#        print 'test point(%s): '%str(datetime.datetime.now()),"测试1:"
#        import os
#        if hasattr(sys, 'frozen'):
#            me = sys.executable
#        else:
#            me = __file__
#        mydir = os.path.dirname(me)
#        version = getFileVersion(me)  
#        print me
#        print mydir 
#        print version
#        print '========='
#        sys.stdout.close()
#        sys.stdout = sys.__stdout__    
        #*********记录测试点，及时删除*********** 

        
class Board(QtGui.QFrame):
    
    msg2Statusbar = QtCore.pyqtSignal(str)
    
    BoardWidth = 10
    BoardHeight = 22
    Speed = 300

    def __init__(self, parent):
        super(Board, self).__init__(parent)
        self.isover = False
        self.initBoard()
        
        
    def initBoard(self):     

        self.timer = QtCore.QBasicTimer()
        self.isWaitingAfterLine = False
        
        self.curX = 0
        self.curY = 0
        self.numLinesRemoved = 0
        self.board = []

        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.clearBoard()
        
        
    def shapeAt(self, x, y):
        return self.board[(y * Board.BoardWidth) + x]

        
    def setShapeAt(self, x, y, shape):
        self.board[(y * Board.BoardWidth) + x] = shape
        

    def squareWidth(self):
        return self.contentsRect().width() / Board.BoardWidth
        

    def squareHeight(self):
        return self.contentsRect().height() / Board.BoardHeight
        

    def start(self):
        
        if self.isPaused:
            return

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.clearBoard()

        self.msg2Statusbar.emit(str(self.numLinesRemoved))

        self.newPiece()
        self.timer.start(Board.Speed, self)

        
    def pause(self):
        
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused
        
        if self.isPaused:
            self.timer.stop()
            self.msg2Statusbar.emit("paused")
            
        else:
            self.timer.start(Board.Speed, self)
            self.msg2Statusbar.emit(str(self.numLinesRemoved))

        self.update()

                
    def restart(self):
        ''''''
        self.pause()
        #self.clearBoard()
        self.isover # 当前未完成确认是否重新开始
        
        numFullLines = 0
        rowsToRemove = []

        for i in range(Board.BoardHeight):
            rowsToRemove.append(i)
        rowsToRemove.reverse()
        
        for m in rowsToRemove:
            for k in range(m, Board.BoardHeight):
                for l in range(Board.BoardWidth):
                        self.setShapeAt(l, k, self.shapeAt(l, k + 1))

        numFullLines += len(rowsToRemove)

        if numFullLines > 0:
            
            self.numLinesRemoved = self.numLinesRemoved + numFullLines
            self.msg2Statusbar.emit(str(self.numLinesRemoved))
                
            self.isWaitingAfterLine = True
            #self.curPiece.setShape(Tetrominoe.NoShape)
            
        self.newPiece(self.curPiece.shape())
        self.isStarted=True
        #print 'now piece1:%s'%self.curPiece.shape()
        self.update()
        #print 'now piece2:%s'%self.curPiece.shape()
        
    def paintEvent(self, event):
        
        painter = QtGui.QPainter(self)
        rect = self.contentsRect()

        boardTop = rect.bottom() - Board.BoardHeight * self.squareHeight()

        for i in range(Board.BoardHeight):
            for j in range(Board.BoardWidth):
                shape = self.shapeAt(j, Board.BoardHeight - i - 1)
                
                if shape != Tetrominoe.NoShape:
                    pass
                    self.drawSquare(painter,rect.left() + j * self.squareWidth(),boardTop + i * self.squareHeight(), shape) 

        if self.curPiece.shape() != Tetrominoe.NoShape:
            
            for i in range(4):
                
                x = self.curX + self.curPiece.x(i)
                y = self.curY - self.curPiece.y(i)
                self.drawSquare(painter, rect.left() + x * self.squareWidth(),boardTop + (Board.BoardHeight - y - 1) * self.squareHeight(),self.curPiece.shape()) 

                    
    def keyPressEvent(self, event):
        key = event.key()
        #print 'presss',self.isStarted,self.curPiece.shape(),event.key(),'|',QtCore.Qt.Key_R,QtCore.Qt.Key_P
        if key == QtCore.Qt.Key_R:
            self.restart()
        if not self.isStarted or self.curPiece.shape() == Tetrominoe.NoShape:
            super(Board, self).keyPressEvent(event)
            return

        if key == QtCore.Qt.Key_P:
            self.pause()
            return
            
        if self.isPaused:
            return
                
        elif key == QtCore.Qt.Key_Left:
            self.tryMove(self.curPiece, self.curX - 1, self.curY)
            
        elif key == QtCore.Qt.Key_Right:
            self.tryMove(self.curPiece, self.curX + 1, self.curY)
            
        elif key == QtCore.Qt.Key_Down:
            self.tryMove(self.curPiece.rotateRight(), self.curX, self.curY)
            
        elif key == QtCore.Qt.Key_Up:
            self.tryMove(self.curPiece.rotateLeft(), self.curX, self.curY)
            
        elif key == QtCore.Qt.Key_Space:
            self.dropDown()
            
        elif key == QtCore.Qt.Key_D:
            self.oneLineDown()
            
        else:
            super(Board, self).keyPressEvent(event)

    def timerEvent(self, event):
        
        if event.timerId() == self.timer.timerId():
            
            if self.isWaitingAfterLine:
                self.isWaitingAfterLine = False
                self.newPiece()
            else:
                self.oneLineDown()
                
        else:
            super(Board, self).timerEvent(event)

            
    def clearBoard(self):
        
        for i in range(Board.BoardHeight * Board.BoardWidth):
            self.board.append(Tetrominoe.NoShape)

        
    def dropDown(self):
        
        newY = self.curY
        
        while newY > 0:
            
            if not self.tryMove(self.curPiece, self.curX, newY - 1):
                break
                
            newY -= 1

        self.pieceDropped()
        

    def oneLineDown(self):
        
        if not self.tryMove(self.curPiece, self.curX, self.curY - 1):
            self.pieceDropped()
            

    def pieceDropped(self):
        
        for i in range(4):
            
            x = self.curX + self.curPiece.x(i)
            y = self.curY - self.curPiece.y(i)
            self.setShapeAt(x, y, self.curPiece.shape())

        self.removeFullLines()

        if not self.isWaitingAfterLine:
            self.newPiece()
            
    # 方格满行消除
    def removeFullLines(self):
        numFullLines = 0
        rowsToRemove = []
        for i in range(Board.BoardHeight):
            n = 0
            for j in range(Board.BoardWidth):
                if not self.shapeAt(j, i) == Tetrominoe.NoShape:
                    n = n + 1
            if n == 10:
                rowsToRemove.append(i)
        rowsToRemove.reverse()
        for m in rowsToRemove:
            for k in range(m, Board.BoardHeight):
                for l in range(Board.BoardWidth):
                        self.setShapeAt(l, k, self.shapeAt(l, k + 1))

        numFullLines = numFullLines + len(rowsToRemove)
        if numFullLines > 0:
            
            self.numLinesRemoved = self.numLinesRemoved + numFullLines
            self.msg2Statusbar.emit(str(self.numLinesRemoved))
                
            self.isWaitingAfterLine = True
            self.curPiece.setShape(Tetrominoe.NoShape)
            self.update()
            
    # 新魔方块
    def newPiece(self,currentPiece=None):
        self.curPiece = Shape()
        if not currentPiece:
            self.curPiece.setRandomShape()
        else:
            self.curPiece.setShape(currentPiece)
        self.curX = Board.BoardWidth / 2 + 1
        self.curY = Board.BoardHeight - 1 + self.curPiece.minY()
        
        #print self.curY
        if not self.tryMove(self.curPiece, self.curX, self.curY):
            
            self.curPiece.setShape(Tetrominoe.NoShape)
            self.timer.stop()
            #self.isStarted = False
            self.msg2Statusbar.emit("Game over")
            self.isover = True
            #self.clearBoard()

    # 判断是否可以继续
    def tryMove(self, newPiece, newX, newY):
        
        for i in range(4):
            
            x = newX + newPiece.x(i)
            y = newY - newPiece.y(i)
            
            if x < 0 or x >= Board.BoardWidth or y < 0 or y >= Board.BoardHeight:
                return False
                
            if self.shapeAt(x, y) != Tetrominoe.NoShape:
                return False

        self.curPiece = newPiece
        self.curX = newX
        self.curY = newY
        self.update()
        
        return True
        
    # 画魔方块
    def drawSquare(self, painter, x, y, shape):
        
        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        color = QtGui.QColor(colorTable[shape])
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2, 
            self.squareHeight() - 2, color)

        painter.setPen(color.light())
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)

        painter.setPen(color.dark())
        painter.drawLine(x + 1, y + self.squareHeight() - 1,
            x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1, 
            y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)


class Tetrominoe(object):
    
    NoShape = 0
    ZShape = 1
    SShape = 2
    LineShape = 3
    TShape = 4
    SquareShape = 5
    LShape = 6
    MirroredLShape = 7


class Shape(object):
    
    coordsTable = (
        ((0, 0),     (0, 0),     (0, 0),     (0, 0)),
        ((0, -1),    (0, 0),     (-1, 0),    (-1, 1)),
        ((0, -1),    (0, 0),     (1, 0),     (1, 1)),
        ((0, -1),    (0, 0),     (0, 1),     (0, 2)),
        ((-1, 0),    (0, 0),     (1, 0),     (0, 1)),
        ((0, 0),     (1, 0),     (0, 1),     (1, 1)),
        ((-1, -1),   (0, -1),    (0, 0),     (0, 1)),
        ((1, -1),    (0, -1),    (0, 0),     (0, 1))
    )

    def __init__(self):
        self.coords = [[0,0] for i in xrange(4)]
        self.pieceShape = Tetrominoe.NoShape
        self.setShape(Tetrominoe.NoShape)
        

    def shape(self):
        return self.pieceShape
        

    def setShape(self, shape):
        table = Shape.coordsTable[shape]
        for i in xrange(4):
            for j in xrange(2):
                self.coords[i][j] = table[i][j]

        self.pieceShape = shape
        

    def setRandomShape(self):
        self.setShape(random.randint(1, 7))

        
    def x(self, index):
        return self.coords[index][0]

        
    def y(self, index):
        return self.coords[index][1]

        
    def setX(self, index, x):
        self.coords[index][0] = x

        
    def setY(self, index, y):
        self.coords[index][1] = y

        
    def minX(self):
        m = self.coords[0][0]
        for i in range(4):
            m = min(m, self.coords[i][0])
        return m

        
    def maxX(self):
        m = self.coords[0][0]
        for i in range(4):
            m = max(m, self.coords[i][0])

        return m

        
    def minY(self):
        
        m = self.coords[0][1]
        for i in range(4):
            m = min(m, self.coords[i][1])

        return m

        
    def maxY(self):
        
        m = self.coords[0][1]
        for i in range(4):
            m = max(m, self.coords[i][1])

        return m

        
    def rotateLeft(self):
        
        if self.pieceShape == Tetrominoe.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape
        
        for i in range(4):
            
            result.setX(i, self.y(i))
            result.setY(i, -self.x(i))

        return result

        
    def rotateRight(self):
        
        if self.pieceShape == Tetrominoe.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape
        
        for i in range(4):
            
            result.setX(i, -self.y(i))
            result.setY(i, self.x(i))

        return result


def main():
    app = QtGui.QApplication([])
    tetris = Tetris()    
    sys.exit(app.exec_())


def getFileVersion(file_name):  
    import win32api 
    info = win32api.GetFileVersionInfo(file_name, "\\")  
    ms = info['FileVersionMS']  
    ls = info['FileVersionLS']  
    version = '%d.%d.%d.%04d' % (win32api.HIWORD(ms), win32api.LOWORD(ms), win32api.HIWORD(ls), win32api.LOWORD(ls))  
    return version

def getSelfPath():
    if hasattr(sys, 'frozen'):
        selfpath = sys.executable
    else:
        selfpath = __file__ 
        #selfpath = u'd:\\tetris.exe'
    return selfpath

def checkupdates(remoteAddress):
    '''Compared with the server files'''
    import xmlrpclib
    response_results = {}
    s = xmlrpclib.ServerProxy(remoteAddress)
    if hasattr(sys, 'frozen'):
        selfpath = sys.executable
    else:
        selfpath = __file__   
    selfdir = os.path.dirname(selfpath)
    basename = os.path.basename(selfpath)
    version =''
    try:
        version = getFileVersion(selfpath)
    except Exception,e:    
        print e
    #version = '1.0.0.0001'    
    if version:
        result = s.updating(version)  # Returns [] or [version,'To be update file path']
        if not result:
            response_results['info'] = 'Is the latest file.'
            return response_results
        else:
            #print s.fetch(result[-1])
            newfp = os.path.join(selfdir,basename[:6]+'(%s).exe'%result[0])
            newfile = open(newfp, "wb")
            newfile.write(s.fetch(result[-1]).data)
            newfile.close()
            newfn = os.path.split(newfp.replace('\\','/'))[-1]

            response_results['info'] = 'UPDATE SUCCESS!'
            response_results['file_path'] = newfp.replace('\\','/')
            response_results['file_name'] = newfn
            return response_results
    else:
        response_results['info'] = 'Can not get version.'
        return response_results
        
#    import urllib
#    import urllib2
#    url = remoteAddress
#    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
#    values = {'name' : 'Michael Foord',
#    'location' : 'Northampton',
#    'language' : 'Python' }
#    headers = { 'User-Agent' : user_agent }
#    
#    data = urllib.urlencode(values)
#    req = urllib2.Request(url, data, headers)
#    response = urllib2.urlopen(req)
#    the_page = response.read()    


    

if __name__ == '__main__':
    main()