# -*- coding: utf-8 -*-
#目标：实现组播的第一步，弄清楚如何用SOCKET
#现状：只能实现客户端与服务器的通信

#通常服务器在启动的时候都会绑定一个众所周知的地址（如ip地址+端口号），
# 用于提供服务，客户就可以通过它来接连服务器；而客户端就不用指定，
# 有系统自动分配一个端口号和自身的ip地址组合。这就是为什么通常服务器端在listen之前会调用bind()，
# 而客户端就不会调用，而是在connect()时由系统随机生成一个。

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtCore import QTextCodec
import sys
import socket
import thread
import time


reload(sys)                         #为了解决编码问题
sys.setdefaultencoding('utf-8')

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 734)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.toolButton = QtGui.QToolButton(self.centralwidget)
        self.toolButton.setGeometry(QtCore.QRect(360, 620, 141, 25))
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(70, 30, 151, 31))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 40, 66, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(280, 40, 66, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.lineEdit_2 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(330, 30, 151, 31))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 100, 66, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.lineEdit_3 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(70, 90, 151, 31))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.toolButton_2 = QtGui.QToolButton(self.centralwidget)
        self.toolButton_2.setGeometry(QtCore.QRect(280, 90, 101, 31))
        self.toolButton_2.setObjectName(_fromUtf8("toolButton_2"))
        self.toolButton_3 = QtGui.QToolButton(self.centralwidget)
        self.toolButton_3.setGeometry(QtCore.QRect(400, 90, 91, 31))
        self.toolButton_3.setObjectName(_fromUtf8("toolButton_3"))
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(50, 370, 431, 161))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 160, 81, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 350, 81, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.toolButton_4 = QtGui.QToolButton(self.centralwidget)
        self.toolButton_4.setGeometry(QtCore.QRect(310, 570, 81, 25))
        self.toolButton_4.setObjectName(_fromUtf8("toolButton_4"))
        self.toolButton_5 = QtGui.QToolButton(self.centralwidget)
        self.toolButton_5.setGeometry(QtCore.QRect(420, 570, 81, 25))
        self.toolButton_5.setObjectName(_fromUtf8("toolButton_5"))
        self.ComboBox = QtGui.QFontComboBox(self.centralwidget)
        self.ComboBox.setGeometry(QtCore.QRect(100, 570, 161, 27))
        self.ComboBox.setObjectName(_fromUtf8("fontComboBox"))
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(30, 570, 66, 17))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.textBrowser = QtGui.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(50, 180, 431, 161))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.radioButton = QtGui.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(70, 0, 116, 22))
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.radioButton_2 = QtGui.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(340, 0, 116, 22))
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.toolButton, self.lineEdit)
        MainWindow.setTabOrder(self.lineEdit, self.lineEdit_2)
        MainWindow.setTabOrder(self.lineEdit_2, self.lineEdit_3)
        MainWindow.setTabOrder(self.lineEdit_3, self.toolButton_2)
        MainWindow.setTabOrder(self.toolButton_2, self.toolButton_3)
        MainWindow.setTabOrder(self.toolButton_3, self.textEdit)
        MainWindow.setTabOrder(self.textEdit, self.toolButton_4)
        MainWindow.setTabOrder(self.toolButton_4, self.toolButton_5)
        MainWindow.setTabOrder(self.toolButton_5, self.ComboBox)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "客户端", None))
        self.toolButton.setText(_translate("MainWindow", "退出", None))
        self.label.setText(_translate("MainWindow", "对方IP", None))
        self.label_2.setText(_translate("MainWindow", "端口号", None))
        self.label_3.setText(_translate("MainWindow", "组播地址", None))
        self.toolButton_2.setText(_translate("MainWindow", "开始聊天", None))
        self.toolButton_3.setText(_translate("MainWindow", "断开", None))
        self.label_4.setText(_translate("MainWindow", "接收发信息", None))
        self.label_5.setText(_translate("MainWindow", "输入信息", None))
        self.toolButton_4.setText(_translate("MainWindow", "清屏", None))
        self.toolButton_5.setText(_translate("MainWindow", "发送", None))
        self.label_6.setText(_translate("MainWindow", "私聊对象", None))
        self.radioButton.setText(_translate("MainWindow", "单播", None))
        self.radioButton_2.setText(_translate("MainWindow", "组播", None))

#单播的线程类，重新写run函数
class Thread2(QtCore.QThread):
    pressed=QtCore.pyqtSignal()
    def __init__(self, s):
        super(Thread2, self).__init__()
        self.s=s
        self.message=""
        self.ip =""

    def run(self):
        while 1:

            msg = self.s.recv(1024)
            if msg !="":
                self.message=msg
                self.pressed.emit()
            else:
                self.message=self.message

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    global sock;
    global th;
    global ip
    global Host
    global ANY
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        super(MyApp, self).__init__(self)
        self.setupUi(self)
        self.msg = ""
        self.ANY = "0.0.0.0"
        self.SENDERIP = '127.0.0.1'
        self.SENDERPORT = 1502
        self.radioButton_2.toggled.connect(lambda:self.multicast(self.radioButton_2))
        self.radioButton.toggled.connect(lambda:self.unicast(self.radioButton))

        QtCore.QObject.connect(self.toolButton_5, QtCore.SIGNAL(_fromUtf8("clicked()")), self.sendMessage)
        QtCore.QObject.connect(self.toolButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.closeclient)
        QtCore.QObject.connect(self.toolButton_4, QtCore.SIGNAL(_fromUtf8("clicked()")), self.clr)

        QtCore.QObject.connect(self.toolButton_3, QtCore.SIGNAL(_fromUtf8("clicked()")), self.closesock)
    
    def closesock(self):
    	self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        self.toolButton_2.setEnabled(1)
        #清屏的功能的实现

    def clr(self):
        self.textBrowser.clear()

    def receiveMessage(self):
        ch =str(self.th.message).decode('utf-8')
        nowtime = time.strftime('%H：%M：%S')
        header = '服务器' + nowtime + "  说 :" + '\n'
        self.msg = header + ch
        self.textBrowser.append(self.msg)

    def sendMessage(self):
        text = self.textEdit.toPlainText()
        ch =str(text).decode('utf-8') #如果不进行"str()"这一步字符转换，则接收端只能显示第一个字符
        self.sock.send(ch)
        nowtime = time.strftime('%H：%M：%S')
        header = '客户端  ' + nowtime + "  说 :" + '\n' 
        text = header + ch
        self.textBrowser.append(text)
        self.textEdit.setText("")

    def startUniChat(self):
        self.ip = self.lineEdit.text()
        self.ip = [int(x) for x in self.ip.split('.')]
        self.ip = '.'.join([str(self.ip[0]),str(self.ip[1]),str(self.ip[2]),str(self.ip[3])])  
        self.Host = self.ip
        self.Port = int(self.lineEdit_2.text())        
        #self.textBrowser.append(self.ip.decode('utf-8'))
        self.toolButton_2.setEnabled(0)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        #新建socket
        self.sock.connect((self.Host,self.Port))
        self.th = Thread2(self.sock)
        QtCore.QObject.connect(self.th, QtCore.SIGNAL("pressed()"), self.receiveMessage)
        self.th.start()    	

    def startMulChat(self):
        #从lineEdit中输入多播地址和端口，并转化为程序里面可以用的形式
        self.ip = self.lineEdit_3.text()
        self.ip = [int(x) for x in self.ip.split('.')]
        self.ip = '.'.join([str(self.ip[0]),str(self.ip[1]),str(self.ip[2]),str(self.ip[3])])  
        self.Host = self.ip
        self.Port = int(self.lineEdit_2.text())        
        self.toolButton_2.setEnabled(0)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) 
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)       
        self.sock.bind((self.SENDERIP,self.Port))
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
        self.status = self.sock.setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP,socket.inet_aton(self.Host) + socket.inet_aton(self.SENDERIP));
        #self.sock.setblocking(0)
        self.th = Thread2(self.sock)
        QtCore.QObject.connect(self.th, QtCore.SIGNAL("pressed()"), self.receiveMessage)
        self.th.start()    

    def unicast(self,b):
        if b.isChecked() == True:
            self.textBrowser.append(("请输入单播IP和Port！").decode('utf-8'))
            QtCore.QObject.connect(self.toolButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.startUniChat)

    def multicast(self,b):
        if b.isChecked() == True:
            self.textBrowser.append(("请输入组播IP和Port！").decode('utf-8'))
            QtCore.QObject.connect(self.toolButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.startMulChat)


    def closeclient(self):
         exit(0) 

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

