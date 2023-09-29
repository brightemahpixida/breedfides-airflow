# see https://geopython.github.io/OWSLib/usage.html#wcs

from owslib.wcs import WebCoverageService
import rasterio
from rasterio import plot, MemoryFile

# https://atlas.thuenen.de/geoserver/ows?service=WCS&request=GetCoverage&coverageid=geonode__pH_map_0_30&format=image%2Ftiff&version=2.0.1&compression=DEFLATE&tileWidth=512&tileHeight=512

# connect to wcs
wcs = WebCoverageService(url='https://atlas.thuenen.de/geoserver/ows', version='2.0.1')

# get list of layers
# list(wcs.contents)

cov_id = wcs.contents['geonode__pH_map_0_30']



subsets = [("X", 5730909, 5758160),("Y", 4433677, 4487337)]

response = wcs.getCoverage(identifier=[cov_id.id],
                           crs='urn:ogc:def:crs:EPSG::31468',
                           subsets=subsets,
                           format='image/tiff',
                           timeout=6000000
                           )

# write response to hdd as geotiff file:
filename = cov_id.id + ".tif"
with open(filename, 'wb') as file:
    file.write(response.read())

# open in rasterio
cov_subset = rasterio.open(filename, driver="GTiff")
plot.show(cov_subset, title='Subsetted DGM from TISDAR', cmap='viridis')


# # load data in memory for huge datasets like dgm5
# dgm5 = wcs.contents['geonode__dgm5_2020-09_utm32']
# response = wcs.getCoverage(identifier=[dgm5.id],
#                            crs='urn:ogc:def:crs:EPSG::25832',
#                            format='GeoTIFF',
#                            timeout=6000000
#                            )

# with MemoryFile(response.read()) as memfile:
#     with memfile.open() as dataset:
#         data_array = dataset.read()
#         plot.show(data_array, title='DGM5 from TISDAR as in memory dataset', cmap='viridis')

