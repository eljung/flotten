import hashlib, sys, hmac, json, random, requests, time, logging, urllib
import influxdb_client
from decouple import config
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

def hmac_sha256(data, key):
    hashed = hmac.new(key.encode('utf-8'),
                      data.encode('utf-8'), hashlib.sha256).digest()
    return ''.join(format(byte, '02x') for byte in hashed)

def get_api(url, key, secret, params=None):
    nonce = str(random.randint(100000, 999999))
    timestamp = str(int(time.time() * 1000))
    headers = {'accessKey': key, 'nonce': nonce, 'timestamp': timestamp}
    sign_str = (urllib.parse.urlencode(params) + '&' if params else '') + \
        urllib.parse.urlencode(headers)
    headers['sign'] = hmac_sha256(sign_str, secret)
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"get_api: {response.text}")

def validate_config():
    required_keys = ["KEY", "SECRET", "SN"]
    missing_keys = [key for key in required_keys if not config(key, default=None)]

    if missing_keys:
        print(f"Error: Missing mandatory configuration values: {', '.join(missing_keys)}")
        sys.exit(1)

def main():
    validate_config()

    api_base_url = config("API_BASE_URL", default="https://api.ecoflow.com")
    api_path = config("API_PATH", default="/iot-open/sign/device/quota/all")
    url = f"{api_base_url}{api_path}"
    
    key = config("KEY")
    secret = config("SECRET")
    sn = config("SN")

    polling_interval = config("POLLING_INTERVAL", default=10, cast=int)

    print("Starting application...")

    while True:
        try:
            payload = get_api(url, key, secret, {'sn': sn})
            print(json.dumps(payload, indent=2))
        except Exception as e:
            print(f"Error during API call: {e}")
        time.sleep(polling_interval)

if __name__ == "__main__":
    main()