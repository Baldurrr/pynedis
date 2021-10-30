import http.client
import json
# conn = http.client.HTTPSConnection("enedisgateway.tech")
# payload = {
#   'type': 'consumption_load_curve',
#   'usage_point_id': "19766136021931",
#   'start': '2021-10-21',
#   'end': '2021-10-22'}

# headers = {
#   'Authorization': "o1UaKkMaYraRh26Ra7SqnR6As70yuecS37OYR0a2l7CdF8usaSgh97",
#   'Content-Type': "application/json",
# }
# conn.request("POST", "/api", json.dumps(payload), headers)
# res = conn.getresponse()
# data = res.read()
# print(data.decode("utf-8"))

with open('api_response.txt') as f:
    lines = f.readlines()
print(lines)