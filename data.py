from PyQt4.QtCore import Qt
data = {
	'Artificial Surfaces':[
		(1,'Built-up Area (settlement)',Qt.darkYellow),
		(2,'Urban Parkland/Open Space',Qt.darkYellow),
		(6,'Surface Mines and Dumps',Qt.darkYellow),
		(5,'Transport Infrastructure',Qt.darkYellow)
	],
	'Bare or Lightly-vegetated Surfaces':[
		(10, 'Sand and Gravel',Qt.darkRed),
		(16, 'Gravel and Rock',Qt.darkRed),
		(12, 'Landslide',Qt.darkRed),
		(14,'Permanent Snow and Ice',Qt.darkRed),
		(15, 'Alpine Grass/Herbfield',Qt.darkRed)
	],
	'Water Bodies':[
		(20, 'Lake or Pond',Qt.blue),
		(21,'River',Qt.blue),
		(22, 'Estuarine Open Water',Qt.blue)
	],
	'Cropland': [
		(30,'Short-rotation Cropland',Qt.red),
		(33,'Orchard Vineyard & Other Perennial Crops',Qt.red)
	],
	'Grassland, Sedgeland and Marshland':[
		(40,'High producing Exotic Grassland',Qt.green),
		(41, 'Low Producing Grassland',Qt.green),
		(43, 'Tall Tussock Grassland',Qt.green),
		(44, 'Depleted Grassland',Qt.green),
		(45, 'Herbaceous Freshwater Vegetation',Qt.green),
		(46, 'Herbaceous Saline Vegetation',Qt.green),
		(47, 'Flaxland',Qt.green)
	],
	'Scrub and Shrubland':[
		(50,'Fernland',Qt.gray),
		(51, 'Gorse and/or Broom',Qt.gray),
		(52, 'Manuka and/or Kanuka',Qt.gray),
		(58, 'Matagouri or Grey Scrub',Qt.gray),
		(54, 'Broadleaved Indigenous Hardwoods',Qt.gray),
		(55, 'Sub Alpine Shrubland',Qt.gray),
		(56, 'Mixed Exotic Shrubland',Qt.gray)
	],
	'Forest':[
		(71,'Exotic Forest',Qt.cyan),
		(64,'Forest-Harvested',Qt.cyan),
		(68,'Deciduous Hardwoods',Qt.cyan),
		(69,'Indigenous Forest',Qt.cyan),
		(70,'Mangrove',Qt.cyan)
	]
}

classes = reduce(lambda x,y:x+y,data.values())
