#! venv/bin/python3
from influxdb import InfluxDBClient
import pprint, time

pp = pprint.PrettyPrinter(indent=2)

client=None
while not client:
    client = InfluxDBClient(host='172.16.10.1', port=8086)
    time.sleep(5)
client.get_list_database()
client.switch_database('telegraf')
# result = client.query('SELECT * FROM "mqtt_consumer" WHERE time > now() - 10s')
# pp.pprint(result.raw['series'])    
result = client.query('SELECT * FROM "rfid_events" WHERE time > now() - 10m')
try:
    pp.pprint(result.raw['series'])
except:
    print("an exception occured")
    pass
# points = result.get_points()
# for point in points:
#     pp.pprint(point)

def write_points(json_body):
    return client.write_points(json_body)