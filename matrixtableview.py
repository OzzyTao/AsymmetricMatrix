from PyQt4.QtGui import QTableView
from PyQt4.QtCore import QSize

class MatrixTableView(QTableView):
	"""docstring for MatrixTableView"""
	def __init__(self, parent=None):
		super(MatrixTableView, self).__init__(parent)
		vheader=self.verticalHeader()
		vheader.setDefaultSectionSize(30)
		hheader = self.horizontalHeader()
		hheader.setDefaultSectionSize(50)

	def _resizeAll(self,row,column):
		totalrows = self.model().rowCount()
		totalcols = self.model().columnCount()
		defaultheight = self.verticalHeader().defaultSectionSize()
		defaultwidth = self.horizontalHeader().defaultSectionSize()
		for r in range(totalrows):
			self.setRowHeight(r,defaultheight)
		for c in range(totalcols):
			self.setColumnWidth(c,defaultwidth)
		self.resizeRowToContents(row)
		self.resizeColumnToContents(column)

	def setItemDelegate(self,delegate):
		super(MatrixTableView,self).setItemDelegate(delegate)
		delegate.editorCreated.connect(self._resizeAll)


	# def _expandCell(self,row,column):
	# 	defaultheight = self.verticalHeader().defaultSectionSize()
	# 	defaultwidth = self.horizontalHeader().defaultSectionSize()
	# 	self.resizeRowToContents(row)
	# 	self.resizeColumnToContents(column)
		
	# def _resetCellSize(self,row,column):

	# 	self.setRowHeight(row,defaultheight)
	# 	self.setColumnWidth(column,defaultwidth)

	def sizeHint(self):
		return QSize(1500,1300)