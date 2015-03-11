from qgis.utils import qgsfunction, iface
from qgis.core import QgsSymbolV2
from PyQt4.QtGui import QColor
from qgis.core import QgsSimpleFillSymbolLayerV2, QgsSingleSymbolRendererV2
@qgsfunction(2,"Python")
def compareClass(values, feature, parent):
    if values[0] == values[1]:
        return QColor('green')
    else:
        return QColor('red')
        

symbol_layer = QgsSimpleFillSymbolLayerV2()
symbol_layer.setDataDefinedProperty('color', '''compareClass("Class_1996","Class_2012")''')
layer = iface.activeLayer()
symbol = QgsSymbolV2.defaultSymbol(layer.geometryType())
symbol.appendSymbolLayer(symbol_layer)
symbol.deleteSymbolLayer(0)
renderer = QgsSingleSymbolRendererV2(symbol) 
layer.setRendererV2(renderer)
