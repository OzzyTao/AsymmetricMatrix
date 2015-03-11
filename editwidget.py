from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QSpinBox, QCheckBox, QSizePolicy, QDialog, QGridLayout
from PyQt4.QtCore import QSize, Qt, pyqtSignal, QRectF, QMargins
from interactiveprogressbar import InteractiveProgressBar
MaximumDistance = 10
MinimumDistance = 0
class EditWidget(QWidget):
	"""docstring for EditWidget"""
	stateChanged = pyqtSignal(bool)
	probabilityChanged = pyqtSignal(int)
	distanceChanged = pyqtSignal(int)
	def __init__(self, probability=50, distance=5,locked=False,parent=None ):
		super(EditWidget, self).__init__(parent)
		self.setFocusPolicy(Qt.WheelFocus)
		self.setAutoFillBackground(True)
		self._probability = probability
		self._distance = distance
		self._locked = locked

		hlayout = QHBoxLayout()
		self._spinbox = QSpinBox()
		self._spinbox.setMaximum(MaximumDistance)
		self._spinbox.setMinimum(MinimumDistance)
		self._spinbox.setValue(distance)
		hlayout.addWidget(self._spinbox)
		hlayout.setAlignment(Qt.AlignCenter)
		hlayout.setContentsMargins(QMargins(3,0,3,0))

		self._checkbox = QCheckBox()
		self._checkbox.setChecked(locked)
		hlayout.addWidget(self._checkbox)

		vlayout = QVBoxLayout()
		vlayout.addLayout(hlayout)
		self._progressbar = InteractiveProgressBar(probability,distance)
		vlayout.addWidget(self._progressbar)
		vlayout.setContentsMargins(QMargins(3,0,3,0))
		vlayout.setMargin(0)
		vlayout.setAlignment(Qt.AlignCenter)
		self.setLayout(vlayout)
		self.setSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum)

		self._progressbar.valueChanged.connect(self._probabilityChanged)
		self._spinbox.valueChanged.connect(self._distanceChanged)
		self._checkbox.stateChanged.connect(self._stateChanged)

	def sizeHint(self):
		return QSize(96,67)

	def setData(self, probability,distance,checked):
		self._probability = probability
		self._distance = distance
		self._locked = checked

		self._spinbox.setValue(distance)
		self._progressbar.setValue(probability)
		self._progressbar.setColor(distance)
		self._checkbox.setChecked(Qt.Checked if checked else Qt.Unchecked)

	def data(self):
		return self._probability,self._distance,self._locked

	def _probabilityChanged(self,newvalue):
		self._probability = newvalue
		self.probabilityChanged.emit(newvalue)

	def _distanceChanged(self,newvalue):
		self._distance = newvalue
		self._progressbar.setColor(newvalue)
		self.distanceChanged.emit(newvalue)

	def _stateChanged(self,newvalue):
		self._locked = True if newvalue else False
		self.stateChanged.emit(self._locked)



if __name__=='__main__':
	from PyQt4.QtGui import QApplication
	import sys
	app = QApplication(sys.argv)
	cell = EditWidget()
	cell.show()
	print cell.size()
	app.exec_()
