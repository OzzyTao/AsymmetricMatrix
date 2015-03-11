from PyQt4.QtGui import QProgressBar, QColor, QPalette, QSizePolicy
from PyQt4.QtCore import Qt, QSize
MaximunDistance=10.0
PROGESS_STYLE='''
QProgressBar{
	border: 2px solid grey;
	border-radius: 5px;
	text-align:center;
}
QProgressBar::chunk{
	background-color: rgb(%d,%d,0);
	width:10px;
}
'''

class InteractiveProgressBar(QProgressBar):
	"""docstring for InteractiveProgressBar"""
	def __init__(self, value, color, parent = None):
		super(InteractiveProgressBar, self).__init__(parent)
		super(InteractiveProgressBar,self).setMaximum(100)		
		super(InteractiveProgressBar,self).setMinimum(0)
		super(InteractiveProgressBar,self).setTextVisible(True)
		super(InteractiveProgressBar,self).setValue(value)
		super(InteractiveProgressBar,self).setSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum)
		self.setColor(color)
	def setColor(self,colorvalue):
		style = PROGESS_STYLE % (colorvalue/MaximunDistance*255,(1-colorvalue/MaximunDistance)*255)
		self.setStyleSheet(style)
	def wheelEvent(self,event):
		oldvalue = self.value()
		newvalue = oldvalue+event.delta()/12.0
		newvalue = newvalue if self.minimum()<=newvalue<=self.maximum() else self.minimum() if newvalue<self.minimum() else self.maximum()
		self.setValue(newvalue)
		self.valueChanged.emit(newvalue)
		event.accept()
	def sizeHint(self):
		return QSize(90,24)
	def minimumSizeHint(self):
		return self.sizeHint()


if __name__=='__main__':
	from PyQt4.QtGui import QApplication
	import sys
	app = QApplication(sys.argv)
	progressbar = InteractiveProgressBar(20,5)
	progressbar.show()
	print progressbar.size()
	# progressbar.setEnabled(False)
	app.exec_()