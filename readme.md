# install

* GDAL and OGR must be installed!
    * `sudo apt install gdal-bin python3-gdal libgdal-dev`
* check successful install with `python3 hello-spatial.py`
* create python 3.10. venv
    * install visual studio code python extension and follow (https://code.visualstudio.com/docs/python/environments)
    * use vscode to install requirements or `pip3 install requirements -r`
* start airflow via `airflow standalone`
* use post_example.json on API to trigger DAG runs
* results will be stored here