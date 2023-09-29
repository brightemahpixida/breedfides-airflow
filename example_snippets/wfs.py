# see https://geopython.github.io/OWSLib/usage.html#wfs
import owslib.fes
from owslib.wfs import WebFeatureService

# PARAMETERS

wfs_url = 'https://tisdar.thuenen.de/geoserver/ows'
typename = 'geonode:bze_lw_standorte_verschleiert'
# typename = 'geonode:bze_lw_standorte_verschleiert'
bbox = (642286, 5732690, 691959, 5757916)
srsname = 'urn:x-ogc:def:crs:EPSG:25832'

# 634009, 5746431, 687756, 5773726

# "wfs_url": "https://tisdar.thuenen.de/geoserver/ows",
# "typename": "geonode:nsg_2018",
# "bbox" :[3426647, 5949995, 3483101, 6005329],
# "srsname" : "urn:x-ogc:def:crs:EPSG:5677"

# "wfs_url": "https://tisdar.thuenen.de/geoserver/ows",
# "typename": "geonode:VG250_GEM0",
# "bbox" :[5762401, 3643974 : 5776054, 3670859],
# "srsname" : "urn:x-ogc:def:crs:EPSG:31467"



# connect to wfs
wfs = WebFeatureService(url=wfs_url, version='1.1.0')
# get list of layers
# list(wfs.contents)

# example of a WFS filter with filter xml
# dataset = "geonode:meeresatlas_anlandungen_tisdar"
# wfs_filter = "art=Sprotte"
# filter_ = owslib.fes.PropertyIsEqualTo(propertyname=wfs_filter.split("=")[0], literal=wfs_filter.split("=")[1])
# filterxml = et.tostring(filter_.toXML()).decode("utf-8")
# response = wfs.getfeature(typename=dataset, filter=filterxml, outputFormat='json')

# e.g. geonode:nsg_2018

response = wfs.getfeature(typename=typename,
                          bbox=bbox,
                          srsname=srsname,
                          outputFormat='json')

# load response BytesIO (json) as python object
import json
dataObject = json.load(response)

# do stuff with dataObject ...

# eg load it into a pandas dataframe
import pandas as pd
df = pd.json_normalize(dataObject['features'])
# get dataframe axes
# print(df.axes)
# select objects with properties.FLAECHE > 5000
# greater_5000_area = df[df['properties.FLAECHE'] > 5000]

# get rid of non ascii characters for filename:
filename = ''.join(e for e in typename if e.isalnum())

# write response to hdd as json file:
with open(filename + '.json', 'w') as file:
    json.dump(dataObject, file, ensure_ascii=False, indent=4)