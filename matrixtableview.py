from PyQt4.QtGui import QTableView

class MatrixTableView(QTableView):
	"""docstring for MatrixTableView"""
	def __init__(self, parent=None):
		super(MatrixTableView, self).__init__(parent)
		vheader=self.verticalHeader()
		vheader.setDefaultSectionSize(30)
		hheader = self.horizontalHeader()
		hheader.setDefaultSectionSize(50)

	def setItemDelegate(self,delegate):
		super(MatrixTableView,self).setItemDelegate(delegate)
		delegate.editorCreated.connect(self._expandCell)
		delegate.editorClosed.connect(self._resetCellSize)

	def _expandCell(self,row,column):
		self.resizeRowToContents(row)
		self.resizeColumnToContents(column)
		
	def _resetCellSize(self,row,column):
		defaultheight = self.verticalHeader().defaultSectionSize()
		defaultwidth = self.horizontalHeader().defaultSectionSize()
		self.setRowHeight(row,defaultheight)
		self.setColumnWidth(column,defaultwidth)