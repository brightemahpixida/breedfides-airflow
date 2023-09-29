from owslib.wcs import WebCoverageService

wcs = WebCoverageService('http://maps.isric.org/mapserv?map=/map/phh2o.map', version='2.0.1')

cov_id = 'phh2o_0-5cm_mean'
ph_0_5 = wcs.contents[cov_id]
ph_0_5.supportedFormats

# 1947689, 5724479 : 1954541, 5727959
# 1924135 5716675 : 1975229 5737890

subsets = [('X', 1947689, 1975229), ('Y', 5716675, 5737890)]
# -1767986, 1485789 : -1243862, 1751964
#subsets = [('X', -1784000, -1140000), ('Y', 1356000, 1863000)]

crs = "http://www.opengis.net/def/crs/EPSG/0/152160"

response = wcs.getCoverage(
    identifier=[cov_id], 
    crs=crs,
    subsets=subsets, 
    resx=250, resy=250, 
    format=ph_0_5.supportedFormats[0])

with open('Senegal_pH_0-5_mean-2.tif', 'wb') as file:
    file.write(response.read())