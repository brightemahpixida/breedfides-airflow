# install

* GDAL and OGR must be installed! `sudo apt install gdal-bin python3-gdal`
* create python 3.10. venv
* `pip3 install requirements -r`
* check successful install with `python hello-spatial.py`
* run `airflow standalone`
* use post_example.json on API to trigger DAG runs
* results will be stored here