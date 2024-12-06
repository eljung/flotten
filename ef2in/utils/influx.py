import logging
import jmespath
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timezone
from .conf import Conf


class Influx:
    def __init__(self):
        self.conf = Conf()
        self.client = InfluxDBClient(url=self.conf.env("INFLUX_URL"),
                                     token=self.conf.influx_token(),
                                     org=self.conf.env("INFLUX_ORG"))

    def __del__(self):
        self.client.close()

    def data_to_point(self, key, value):
        point = Point(self.conf.env("INFLUX_MEASUREMENT"))

        (tag, fieldname) = key.split(".")
        point.tag("function", tag)
        point.field(fieldname, value)

        return point.time(datetime.now(timezone.utc))

    def json_to_points(self, json):
        points = []

        for key, value in jmespath.search("data", json).items():
            if isinstance(value, (float, int)):
                points.append(self.data_to_point(key, value))

        return points

    def write_points(self, points):
        write_api = self.client.write_api(write_options=SYNCHRONOUS)

        try:
            write_api.write(bucket=self.conf.env("INFLUX_BUCKET"),
                            org=self.conf.env("INFLUX_ORG"),
                            record=points)
        except Exception as e:
            logging.error(f"caught Exception, e = {e}")
