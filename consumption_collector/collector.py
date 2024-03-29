"""
Collector collects data from some type of communicator, which produces this data in form of influx points.
These data are stored in a queue and after a defined time are flushed to the database (InfluxDB).
Every Collector is inserted inside another class called communicator. This communicator inserts data into internal
queue of collector.
"""
from influxdb_client.client.write_api import ASYNCHRONOUS
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.influxdb_client import InfluxDBClient


class Collector:
    def __init__(self, url=None, token=None, org=None, bucket=None):
        """
        Initialize Collector class and set parameters for InfluxDBClient.
        :param url: InfluxDB url
        :param token: InfluxDB token
        :param org: InfluxDB organization
        :param bucket: InfluxDB bucket
        """
        self._url = url
        self._token = token
        self._org = org
        self._bucket = bucket
        self._points_queue = []         # Queue for points

    def save_point(self, point):
        """
        Method for saving/uploading points into Collectors queue.
        :param point: InfluxDB point
        """
        self._points_queue.append(point)

    def flush_data(self):
        """
        Method for flushing data into InfluxDB. This method needs to be called at defined intervals.
        This method takes all data from Collectors points_queue, till it reach empty queue + 1.
        """
        with InfluxDBClient(url=self._url, token=self._token, org=self._org) as influx_client:
            write_api = influx_client.write_api(write_options=ASYNCHRONOUS)
            record = []

            while len(self._points_queue) != 1:
                record.append(self._points_queue.pop(0))

            try:
                write_api.write(bucket=self._bucket, record=record)
            except InfluxDBError:
                #TODO log
                raise Exception("Insufficient write permissions to InfluxDB.")
