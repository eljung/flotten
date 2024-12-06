import time
import logging
from utils import Ecoflow, Conf, Influx

class App:
    def __init__(self):
        self.conf = Conf()
        self.ecoflow = Ecoflow()
        self.influx = Influx()

    def run(self):
        pi = self.conf.env("APP_POLLING_INTERVAL", cast=int)
        sn = self.conf.secrets("ECOFLOW_SN")

        while True:
            try:
                # lets give some time for the influxdb service to get online
                time.sleep(pi)

                response = self.ecoflow.call_api_get(
                    "/iot-open/sign/device/quota/all", {"sn": sn})
                points = self.influx.json_to_points(response)
                self.influx.write_points(points)

                logging.info("heartbeat, next poll in %ds", pi)
            except Exception as e:
                logging.error(f"caught Exception, e = {e}")


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s",
                    datefmt="%Y.%m.%d %H:%M:%S")


if __name__ == "__main__":
    app = App()
    app.run()
