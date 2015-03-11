from PyQt4.QtGui import QItemDelegate, QApplication, QStyle, QTableView, QProgressBar, QStyleOptionProgressBar, QHeaderView, QPen, QBrush, QColor, QPainter, QTextOption
from PyQt4.QtCore import QAbstractTableModel, QObject, Qt, QSize, QRectF, pyqtSignal, QEvent, QVariant
from editwidget import EditWidget
from interactiveprogressbar import MaximunDistance
class Cell(QObject):
	"""docstring for Cell"""
	def __init__(self, probability, distance):
		super(Cell, self).__init__()
		self._probability = probability
		self._distance = distance
		self._locked = False

	def probability(self):
		return self._probability

	def distance(self):
		return self._distance

	def lockState(self):
		return self._locked

	def setProbability(self,probability):
		self._probability=int(probability)

	def setDistance(self,distance):
		self._distance = int(distance)

	def setState(self,state):
		self._locked = bool(state)

class MatrixModel(QAbstractTableModel):
	"""docstring for MatrixModel"""
	Probability_DataRole = Qt.UserRole
	Distance_DataRole = Qt.UserRole+1
	Lock_DataRole = Qt.UserRole+2
	Probability_EditRole = Qt.UserRole+3
	Distance_EditRole = Qt.UserRole+4
	Lock_EditRole = Qt.UserRole+5
	def __init__(self, classnames):
		super(MatrixModel, self).__init__()
		self._classNames = classnames
		self._classIDs = [str(x[0]) for x in classnames]
		self._matrixData = {}
		self.initMatrix()

	def initMatrix(self):
		for rowname in self._classNames:
			self._matrixData[str(rowname[0])] = {}
			for colname in self._classNames:
				self._matrixData[str(rowname[0])][str(colname[0])] = Cell(100 if rowname[0]==colname[0] else 0, 0 if rowname[0]==colname[0] else 3 if rowname[2]==colname[2] else 6)

	def rowCount(self,parent=None):
		return len(self._classNames)

	def columnCount(self,parent=None):
		return len(self._classNames)

	def data(self,index,role):
		if index.isValid():
			rowname = str(self._classNames[index.row()][0])
			columnname = str(self._classNames[index.column()][0])
			if role == MatrixModel.Probability_DataRole:
				return self._matrixData[rowname][columnname].probability()
			elif role == MatrixModel.Distance_DataRole:
				return self._matrixData[rowname][columnname].distance()
			elif role == MatrixModel.Lock_DataRole:
				return self._matrixData[rowname][columnname].lockState()
		return None

	def setData(self,index,value,role):
		if index.isValid():
			rowname = str(self._classNames[index.row()][0])
			columnname = str(self._classNames[index.column()][0])
			if role == MatrixModel.Probability_EditRole:
				self._matrixData[rowname][columnname].setProbability(value)
				return True
			if role == MatrixModel.Distance_EditRole:
				self._matrixData[rowname][columnname].setDistance(value)
				return True
			if role == MatrixModel.Lock_EditRole:
				self._matrixData[rowname][columnname].setState(value)
				return True
		return False

	def flags(self,index):
		return Qt.ItemIsEnabled|Qt.ItemIsEditable

	def headerData(self, section, orientation,role):
		headerinfo = self._classNames[section]
		if role == Qt.DisplayRole:
			return headerinfo[0]
		if role == Qt.ForegroundRole:
			return QBrush(headerinfo[2])
		if role == Qt.ToolTipRole:
			return headerinfo[1]

	def probability(self,observation1,observation2):
		if str(observation1) in self._classIDs and str(observation2) in self._classIDs:
			realclass1 = self.trueClass(observation1)
			realclass2 = self.trueClass(observation2)
			return realclass1[1]*realclass2[1]/10000.0
		else:
			return 0

	def changeLevel(self,observation1,observation2):
		if str(observation1) in self._classIDs and str(observation2) in self._classIDs:
			if observation1!=observation2:
				realclass1 = self.trueClass(observation1)
				realclass2 = self.trueClass(observation2)
				return self._matrixData[realclass1[0]][realclass2[0]].distance()
			else:
				return 0
		else:
			return -1

	def trueClass(self,observation):
		maxPossi = 0
		cl = str(observation)
		trans = self._matrixData[cl]
		for key in trans:
			if trans[key].probability()>=maxPossi:
				maxPossi = trans[key].probability()
				cl = key
		return cl, maxPossi if maxPossi else 1.0



class CellDelegate(QItemDelegate):
	"""docstring for CellDelegate"""
	editorCreated = pyqtSignal(int,int)
	editorClosed = pyqtSignal(int,int)
	def __init__(self, parent=None):
		super(CellDelegate, self).__init__(parent)
		self.closeEditor.connect(self.close_editor)

	def paint(self,painter,option,index):
		painter.save()
		probability = index.data(MatrixModel.Probability_DataRole)
		probability = probability.toInt()[0] if isinstance(probability,QVariant) else probability
		colorvalue = index.data(MatrixModel.Distance_DataRole)
		colorvalue = colorvalue.toInt()[0] if isinstance(colorvalue,QVariant) else colorvalue
		rect = option.rect
		painter.setRenderHint(QPainter.Antialiasing,True)
		painter.setPen(Qt.NoPen)
		painter.setBrush(QBrush(QColor(colorvalue/MaximunDistance*255,(1-colorvalue/MaximunDistance)*255,0)))
		chunk = rect.adjusted(4,4,-4,-4)
		chunk.setWidth(chunk.width()*probability/100.0)
		painter.drawRoundedRect(chunk,6,6)
		painter.setBrush(Qt.NoBrush)
		borderpen = QPen(Qt.gray)
		borderpen.setWidth(2)
		painter.setPen(borderpen)
		painter.drawRoundedRect(rect.adjusted(2,2,-2,-2),6,6)
		textpen = QPen(Qt.black)
		painter.setPen(textpen)
		painter.drawText(QRectF(rect),'%d%%' % (probability,),QTextOption(Qt.AlignCenter))
		painter.restore()

	def sizeHint(self, option, index):
		return QSize(96,67)

	def createEditor(self,parent,option,index):
		editor=EditWidget(parent=parent)
		editor.row = index.row()
		editor.column = index.column()
		self.editorCreated.emit(index.row(),index.column())
		return editor

	def setEditorData(self,editor,index):
		probability = index.data(MatrixModel.Probability_DataRole)
		probability = probability.toInt()[0] if isinstance(probability,QVariant) else probability
		distance = index.data(MatrixModel.Distance_DataRole)
		distance = distance.toInt()[0] if isinstance(distance,QVariant) else distance
		lockState = index.data(MatrixModel.Lock_DataRole)
		lockState = lockState.toBool() if isinstance(lockState,QVariant) else lockState
		editor.setData(probability,distance,lockState)

	# def updateEditorGeometry(self,editor,option,index):
	# 	editor.setGeometry(option.rect)

	def setModelData(self,editor,model,index):
		probability, distance, lockState = editor.data()
		model.setData(index,probability,MatrixModel.Probability_EditRole)
		model.setData(index,distance,MatrixModel.Distance_EditRole)
		model.setData(index,lockState,MatrixModel.Lock_EditRole)

	def close_editor(self,editor,hint):
		self.editorClosed.emit(editor.row,editor.column)

	
if __name__ == '__main__':
	import sys
	from data import classes
	from matrixtableview import MatrixTableView
	app = QApplication(sys.argv)
	classnames = classes
	model = MatrixModel(classnames)
	tableView = MatrixTableView()
	tableView.setModel(model)
	delegate = CellDelegate()
	tableView.setItemDelegate(delegate)
	tableView.show()
	print model.probability(1,2),model.changeLevel(1,2)
	print model.probability(1,1),model.changeLevel(1,1)
	print model.probability(10,20),model.changeLevel(10,20)
	sys.exit(app.exec_())
