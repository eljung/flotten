import requests
import hashlib
import hmac
import logging
import random
import time
import urllib
from .conf import Conf


class Ecoflow:
    def __init__(self):
        self.conf = Conf()
        self.api_key = self.conf.secrets("ECOFLOW_API_KEY")
        self.api_secret = self.conf.secrets("ECOFLOW_API_SECRET")
        self.sn = self.conf.secrets("ECOFLOW_SN")
        self.base_url = self.conf.env("ECOFLOW_API_BASE_URL")

    def hmac_sha256(self, data, key):
        hashed = hmac.new(key.encode('utf-8'),
                          data.encode('utf-8'), hashlib.sha256).digest()
        return ''.join(format(byte, '02x') for byte in hashed)

    def headers(self, params=None):
        nonce = str(random.randint(100000, 999999))
        timestamp = str(int(time.time() * 1000))
        headers = {'accessKey': self.api_key,
                   'nonce': nonce, 'timestamp': timestamp}
        sign_str = (urllib.parse.urlencode(params) + '&' if params else '') + \
            urllib.parse.urlencode(headers)
        headers['sign'] = self.hmac_sha256(sign_str, self.api_secret)

        return headers

    def call_api_get(self, path, params=None):
        url = f"{self.base_url}{path}"
        headers = self.headers(params)

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"http error, e = {http_err}")
            raise
        except requests.exceptions.RequestException as req_err:
            logging.error(f"request error, e = {req_err}")
            raise
        except Exception as e:
            logging.error(f"caught Exception, e = {e}")
            raise
