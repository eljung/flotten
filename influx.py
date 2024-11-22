import influxdb_client, os, time
import numpy as np
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = os.environ.get("INFLUXDB_TOKEN")
org = "Nelara"
url = "http://localhost:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="flotten"

write_api = client.write_api(write_options=SYNCHRONOUS)

num_points = 100

# Generate a charge curve (ascending numbers)
charge_curve = np.linspace(1, 100, num_points // 2)

# Generate a discharge curve (descending numbers)
discharge_curve = np.linspace(100, 1, num_points // 2)

# Combine charge and discharge curves
battery_curve = np.concatenate([charge_curve, discharge_curve])

for value in battery_curve:
  point = (
    Point("ecoflow")
    .field("charge", value)
  )
  write_api.write(bucket=bucket, org="Nelara", record=point)
  time.sleep(0.05)

exit

query_api = client.query_api()

query = """from(bucket: "flotten")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "measurement1")"""
tables = query_api.query(query, org="Nelara")

for table in tables:
  for record in table.records:
    print(record)

query_api = client.query_api()

query = """from(bucket: "flotten")
  |> range(start: -10m)
  |> filter(fn: (r) => r._measurement == "measurement1")
  |> mean()"""
tables = query_api.query(query, org="Nelara")

for table in tables:
    for record in table.records:
        print(record)

