
from owslib.wcs import WebCoverageService
import rasterio
from rasterio import plot, MemoryFile

from airflow.decorators import dag, task

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator, get_current_context
import pendulum

if __name__ == "__main__":
    dag.test()

## DEFAULT ARGS

default_args = {
    'wcs_url': 'http://maps.isric.org/mapserv?map=/map/phh2o.map',
    'cov_id': 'phh2o_0-5cm_mean',
    'bbox' : [('X', 1947689, 1975229), ('Y', 5716675, 5737890)],
    'srsname' : 'http://www.opengis.net/def/crs/EPSG/0/152160'
}

# {
#     "conf": {
#             "wcs_url": "http://maps.isric.org/mapserv?map=/map/phh2o.map",
#             "cov_id": "phh2o_0-5cm_mean",
#             "bbox" :[["X", 1947689, 1975229],["Y", 5716675, 5737890]],
#             "srsname" : "http://www.opengis.net/def/crs/EPSG/0/152160"
#         },
#     "note": "posted via curl"
# }


## FUNCTIONS

def fetch_tif_from_wcs(wcs_url, cov_id, bbox, srsname):
    # connect to wcs
    wcs = WebCoverageService(wcs_url, version='2.0.1')

    coverage = wcs.contents[cov_id]
    subsets = bbox

    response = wcs.getCoverage(
        identifier=[cov_id], 
        crs=srsname,
        subsets=subsets, 
        format='image/tiff')

    return response


## DAG
@dag(
    default_args= default_args,
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["BreedFides","OGC"],
)

def fetch_wcs_tif():
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
        pipeline. In this case, we fetch it from an OGC WCS
        """

        context = get_current_context()
        print(context["params"])
        dag_run = context["dag_run"]
        dagrun_conf = dag_run.conf
        wcs_url = dagrun_conf["wcs_url"]
        cov_id = dagrun_conf["cov_id"]
        bbox = dagrun_conf["bbox"]
        srsname = dagrun_conf["srsname"]

        coverage = fetch_tif_from_wcs(wcs_url, cov_id, bbox, srsname)
        # get rid of non ascii characters for filename:
        filename = ''.join(e for e in cov_id if e.isalnum())

        # write response to hdd as json file:
        with open(filename + '.tif', 'wb') as file:
            file.write(coverage.read())
        return filename + '.tif'
    
    @task()
    def transform(coverage):
        """
        #### Transform task
        YOU COULD DO TRANSFORMATION STUFF HERE LIKE.
        OR DO NOTHING AND JUST SEND IT TO THE PERSISTING LAYER.
        As example a viridis plot will be drawn.
        """
        
        # YOU COULD DO TRANSFORMATION STUFF HERE LIKE
        
        # save file and retransform it into some other CRS?

        coverage_file = rasterio.open(coverage, driver="GTiff")
        plot.show(coverage_file, title='some example vis', cmap='viridis')

        ## OR DO NOTHING AND JUST SEND IT TO THE PERSISTING LAYER

        return coverage
    
    @task()
    def load(coverage, cov_id=None):
        """
        #### Load task
        Seems airflow does not like to pass response object. 
        raster was saved in exract step.
        nonetheless it was saved on this VM.
        Likely there will be some kind of S3 bucket to send it to.
        """
        # DO S3 stuff here
        # CLEANUP VM SPACE AFTERWARDS

    wcs_data = extract()
    wcs_data_tranfsormed = transform(wcs_data)
    load(wcs_data_tranfsormed)

fetch_wcs_tif()