import hashlib
import hmac
import json
import random
import requests
import time
import logging

def hmac_sha256(data, key):
  hashed = hmac.new(key.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).digest()
  return ''.join(format(byte, '02x') for byte in hashed)

def get_qstring(params): return '&'.join([f"{key}={params[key]}" for key in sorted(params.keys())])

def get_api(url, key, secret, params=None):
  nonce = str(random.randint(100000, 999999))
  timestamp = str(int(time.time() * 1000))
  headers = {'accessKey':key,'nonce':nonce,'timestamp':timestamp}
  sign_str = (get_qstring(params) + '&' if params else '') + get_qstring(headers)
  headers['sign'] = hmac_sha256(sign_str, secret)
  response = requests.get(url, headers=headers, params=params)
  if response.status_code == 200: return response.json()
  else: logging.error(f"get_api: {response.text}")
 
if __name__ == "__main__":

  url     = 'https://api.ecoflow.com'
  path    = '/iot-open/sign/device/quota/all'
  key     = 'BbTDqSL72CDcga9J9vkqoPEDdHXCMU45'
  secret  = 'MwVa9zG3JzYZ6mH6fYzTP4lHENguZYmI'
  sn      = 'R351ZEB5HG8L0154'  
  payload = get_api(f"{url}{path}",key,secret,{'sn':sn})
  print(json.dumps(payload,indent=2))