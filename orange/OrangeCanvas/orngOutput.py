# Author: Gregor Leban (gregor.leban@fri.uni-lj.si)
# Description:

#
from qt import *
import sys
import os
import string
import time
import traceback
import os.path
import orngResources

TRUE  = 1
FALSE = 0 

class OutputWindow(QMainWindow):
	def __init__(self, canvasDlg, *args):
		apply(QMainWindow.__init__,(self,) + args)
		self.resize(700,500)
		self.showNormal()
		self.canvasDlg = canvasDlg

		#self.textOutput = QTextBrowser(self)
		self.textOutput = QTextView(self)
		self.textOutput.setFont(QFont('Courier New',10, QFont.Normal))
		self.textOutput.setHScrollBarMode(QScrollView.AlwaysOn )
		self.setCentralWidget(self.textOutput)
		self.setCaption("Output Window")
		self.setIcon(QPixmap(orngResources.output))

		self.defaultExceptionHandler = sys.excepthook
		self.defaultSysOutHandler = sys.stdout
		
		#sys.excepthook = self.exceptionHandler
		#sys.stdout = self
		#self.textOutput.setText("")
		self.setFocusPolicy(QWidget.NoFocus)

	def catchException(self, catch):
		if catch: sys.excepthook = self.exceptionHandler
		else:     sys.excepthook = self.defaultExceptionHandler

	def catchOutput(self, catch):
		if catch:	sys.stdout = self
		else: 		sys.stdout = self.defaultSysOutHandler

	def setFocusOnException(self, focusOnCatchException):
		self.focusOnCatchException = focusOnCatchException
		
	def setFocusOnOutput(self, focusOnCatchOutput):
		self.focusOnCatchOutput = focusOnCatchOutput

	def clear(self):
		self.textOutput.setText("")
	
	def write(self, text):
		if self.focusOnCatchOutput:
			self.canvasDlg.menuItemShowOutputWindow()
		self.textOutput.append(text)
		self.textOutput.ensureVisible(0, self.textOutput.contentsHeight())
		self.canvasDlg.setStatusBarEvent(text)

	def keyReleaseEvent (self, event):
		if event.state() & Qt.ControlButton != 0 and event.ascii() == 3:	# user pressed CTRL+"C"
			self.textOutput.copy()

	def exceptionHandler(self, type, value, tracebackInfo):
		if self.focusOnCatchException:
			self.canvasDlg.menuItemShowOutputWindow()
			
		t = time.localtime()
		self.textOutput.append("<nobr>Unhandled exception of type <b>%s </b> occured at %d:%d:%d:</nobr>" % ( str(type) , t[3],t[4],t[5]))
		self.textOutput.append("<nobr>Traceback:</nobr>")
		self.canvasDlg.setStatusBarEvent("Unhandled exception of type %s occured at %d:%d:%d" % ( str(type) , t[3],t[4],t[5]))

		# TO DO:repair this code to shown full traceback. when 2 same errors occur, only the first one gets full traceback, the second one gets only 1 item
		
		list = traceback.extract_tb(tracebackInfo, 10)
		space = "&nbsp &nbsp "
		totalSpace = space
		for i in range(len(list)):
			(file, line, funct, code) = list[i]
			if code == None: continue
			(dir, filename) = os.path.split(file)
			self.textOutput.append("<nobr>" + totalSpace + "File: <u>" + filename + "</u>  in line %4d</nobr>" %(line))
			self.textOutput.append("<nobr>" + totalSpace + "<nobr>Function name: %s</nobr>" % (funct))
			if i == len(list)-1:
				self.textOutput.append("<nobr>" + totalSpace + "Code: <b>" + code + "</b></nobr>")
			else:
				self.textOutput.append("<nobr>" + totalSpace + "Code: " + code + "</nobr>")
				totalSpace += space
			
		self.textOutput.append("<nobr>" + totalSpace + "Exception type: <b>" + str(type) + "</b></nobr>")
		self.textOutput.append("<nobr>" + totalSpace + "Exception value: <b>" + str(value)+ "</b></nobr>")
		self.textOutput.append("<hr>")
		self.textOutput.ensureVisible(0, self.textOutput.contentsHeight())
		
