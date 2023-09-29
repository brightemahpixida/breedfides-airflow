# see https://geopython.github.io/OWSLib/usage.html#wfs
import owslib.fes
from owslib.wfs import WebFeatureService


import json

import pendulum

from airflow.decorators import dag, task

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator, get_current_context

if __name__ == "__main__":
    dag.test()

## DEFAULT ARGS

default_args = {
    'wfs_url': 'https://tisdar.thuenen.de/geoserver/ows',
    'typename': 'geonode:nsg_2018',
    'bbox' : (3426647, 5949995, 3483101, 6005329),
    'srsname' : 'urn:x-ogc:def:crs:EPSG:5677'
}


## FUNCTIONS

def fetch_json_from_wfs(wfs_url, typename, bbox, srsname):
    # connect to wfs
    wfs = WebFeatureService(url=wfs_url, version='1.1.0')

    response = wfs.getfeature(typename=typename,
                            bbox=bbox,
                            srsname=srsname,
                            outputFormat='json')

    # load response BytesIO (json) as python object
    import json
    dataObject = json.load(response)

    return dataObject


## DAG
@dag(
    default_args= default_args,
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["BreedFides","OGC"],
)

def fetch_wfs_json():
    """
    ### TaskFlow API Tutorial Documentation
    This is a simple data pipeline example which demonstrates the use of
    the TaskFlow API using three simple tasks for Extract, Transform, and Load.
    Documentation that goes along with the Airflow TaskFlow API tutorial is
    located
    [here](https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html)
    """
    @task()
    def extract(**kwargs):
        """
        #### Extract task
        A simple Extract task to get data ready for the rest of the data
        pipeline. In this case, we fetch it from an OGC WFS
        """
        
        # does not work?
        context = get_current_context()
        print(context["params"])
        dag_run = context["dag_run"]
        dagrun_conf = dag_run.conf
        wfs_url = dagrun_conf["wfs_url"]
        typename = dagrun_conf["typename"]
        bbox = dagrun_conf["bbox"]
        srsname = dagrun_conf["srsname"]

        data_json = fetch_json_from_wfs(wfs_url, typename, bbox, srsname)
        return data_json
    
    @task(multiple_outputs=True)
    def transform(data_json: dict, **kwargs):
        """
        #### Transform task
        YOU COULD DO TRANSFORMATION STUFF HERE LIKE.
        OR DO NOTHING AND JUST SEND IT TO THE PERSISTING LAYER
        """
        
        # eg load it into a pandas dataframe
        # import pandas as pd
        # df = pd.json_normalize(data_json['features'])
        # get dataframe axes
        # print(df.axes)
        # select objects with properties.FLAECHE > 5000
        # greater_5000_area = df[df['properties.FLAECHE'] > 5000]

        # example of a WFS filter with filter xml
        # dataset = "geonode:meeresatlas_anlandungen_tisdar"
        # wfs_filter = "art=Sprotte"
        # filter_ = owslib.fes.PropertyIsEqualTo(propertyname=wfs_filter.split("=")[0], literal=wfs_filter.split("=")[1])
        # filterxml = et.tostring(filter_.toXML()).decode("utf-8")
        # response = wfs.getfeature(typename=dataset, filter=filterxml, outputFormat='json')

        return data_json
    
    @task()
    def load(data_json: dict, **kwargs):
        """
        #### Load task
        A simple Load task which takes in the result of the Transform task and
        saving it to end user review.
        """

        context = get_current_context()
        print(context["params"])
        dag_run = context["dag_run"]
        dagrun_conf = dag_run.conf
        wfs_url = dagrun_conf["wfs_url"]
        typename = dagrun_conf["typename"]
        bbox = dagrun_conf["bbox"]
        srsname = dagrun_conf["srsname"]


        # get rid of non ascii characters for filename:
        filename = ''.join(e for e in typename if e.isalnum())

        # write response to hdd as json file:
        with open(filename + '.json', 'w') as file:
            json.dump(data_json, file, ensure_ascii=False, indent=4)

        # DO S3 stuff here
        # CLEANUP VM SPACE AFTERWARDS

    wfs_data = extract()
    wfs_data_tranfsormed = transform(wfs_data)
    load(wfs_data_tranfsormed)

fetch_wfs_json()