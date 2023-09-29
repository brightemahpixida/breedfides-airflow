# see https://geopython.github.io/OWSLib/usage.html#wcs

from owslib.wcs import WebCoverageService
import rasterio
from rasterio import plot, MemoryFile

# connect to wcs
wcs = WebCoverageService(url='https://tisdar.thuenen.de/geoserver/ows', version='2.0.1')

# get list of layers
# list(wcs.contents)
# e.g.
# 'geonode__dgm5_2020-09_utm32'
# 'geonode__dgm25_2020-09_utm32'
dgm = wcs.contents['geonode__dgm25_2020-09_utm32']

# fetch bbox info if needed
# dgm.boundingboxes
# returns
# [{'nativeSrs': 'http://www.opengis.net/def/crs/EPSG/0/25832',
#   'bbox': (279987.5, 5235712.5, 922212.5, 6101987.5)}
# ]

# set bbox as subset
# get axis abbreviations from http://www.opengis.net/def/crs/EPSG/0/25832 (see above)
# in there >>  <gml:cartesianCS xlink:href="https://apps.epsg.org/api/v1/CoordSystem/4400/export?format=gml"/>
# Example:
# <gml:axis>
# <gml:CoordinateSystemAxis gml:id="epsg-axis-1" uom="9001">
# <gml:descriptionReference xlink:href="https://apps.epsg.org/api/v1/CoordinateAxisName/9906/export?format=gml"/>
# <gml:identifier codeSpace="EPSG">1</gml:identifier>
# <gml:axisAbbrev>E</gml:axisAbbrev>   <<<< THIS
# <gml:axisDirection codeSpace="EPSG">east</gml:axisDirection>
# </gml:CoordinateSystemAxis>
# </gml:axis>

subsets = [('E', 591464, 614578), ('N', 5785984, 5795003)]

response = wcs.getCoverage(identifier=[dgm.id],
                           crs='urn:ogc:def:crs:EPSG::25832',
                           subsets=subsets,
                           format='GeoTIFF',
                           timeout=6000000
                           )

# write response to hdd as geotiff file:
filename = '../data/' + dgm.id + "_subset.tif"
with open(filename, 'wb') as file:
    file.write(response.read())

# open in rasterio
dgm_subset = rasterio.open(filename, driver="GTiff")
plot.show(dgm_subset, title='Subsetted DGM from TISDAR', cmap='viridis')


# load data in memory for huge datasets like dgm5
dgm5 = wcs.contents['geonode__dgm5_2020-09_utm32']
response = wcs.getCoverage(identifier=[dgm5.id],
                           crs='urn:ogc:def:crs:EPSG::25832',
                           format='GeoTIFF',
                           timeout=6000000
                           )

with MemoryFile(response.read()) as memfile:
    with memfile.open() as dataset:
        data_array = dataset.read()
        plot.show(data_array, title='DGM5 from TISDAR as in memory dataset', cmap='viridis')

