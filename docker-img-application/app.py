#!/usr/bin/env python3

import os
import json
import requests
from flask import Flask, Response

# Base dir of the html, css and js files
BASEDIR='/var/www'

app = Flask(__name__)

mec_base = ''
service_id = ''
app_instance_id = ''
transports = [ { 'id': 'TransId12345' } ]

# 8.2.2
@app.route('/transports')
def get_transports():
    global mec_base
    global transports
    query_base = "{}/transports".format( mec_base )
    r = requests.get(query_base)

    return r.text

# 8.2.1
@app.route('/services')
def service_availability():
    global mec_base
    global app_instance_id
    out = ''
    query_base = "{}/applications/{}/services".format(
            mec_base, app_instance_id)

    r = requests.get(query_base)

    return r.text

@app.route('/services/subscribe')
def subscribe():
    global mec_base
    global service_id
    global transports
    global app_instance_id

    data = {
      "serName": "UniboMECService",
      "serCategory": {
        "href": "/example/catalogue1",
        "id": "id12345",
        "name": "RNI",
        "version": "v1"
      },
      "version": "ServiceVersion1",
      "state": "ACTIVE",
      "transportId": "Rest1",
      "transportInfo": {
        "id": '{}'.format(transports[0]['id']),
        "name": "REST",
        "description": "REST API",
        "type": "REST_HTTP",
        "protocol": "HTTP",
        "version": "2.0",
        "endpoint": {
        },
      "security": {
        "oAuth2Info": {
          "grantTypes": [
            ""
          ],
          "tokenEndpoint": ""
        }
      },
      "implSpecificInfo": {}
      },
      "serializer": "JSON",
      "scopeOfLocality": "MEC_SYSTEM",
      "consumedLocalOnly": True,
      "isLocal": True
    }

    query_base = "{}/applications/{}/services".format(mec_base,
            app_instance_id)

    headers = {"content-type": "application/json"}
    r = requests.post(query_base, data=json.dumps(data), headers=headers)

    # XXX we don't have any slash in the url?
    service_id = r.headers['location'].split('/')[-1]

    return 'New service_id: {}'.format(service_id)

# 8.2.4
@app.route('/services/unsubscribe')
def unsubscribe():
    global mec_base
    global service_id
    global app_instance_id
    query_base = "{}/applications/{}/services/{}".format(mec_base,
            app_instance_id, service_id)
    r = requests.delete(query_base)
    return r.text

# 8.3.5
@app.route('/dns_rules')
def get_dns_rule():
    global mec_base
    global dns_rules
    global app_instance_id

    query_base = "{}/applications/{}/dns_rules".format(mec_base,
            app_instance_id)
    r = requests.get(query_base)

    dns_rules = json.loads(r.text)

    return r.text

@app.route('/dns_rules/<modification>')
def modify_dns(modification):
    global mec_base
    global dns_rules
    global app_instance_id
    dns_rule = dns_rules[0]

    query_base = "{}/applications/{}/dns_rules/{}".format(
            mec_base, app_instance_id, dns_rule['dnsRuleId']
    )

    dns_rule["state"] = modification
    headers = { 'content-type': 'application/json' }
    r = requests.put(query_base, data=json.dumps(dns_rule), headers=headers)
    return json.dumps(dns_rule)

@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def catch_all(path):
    if '.ico' in path:
        return '';

    t = 'text/html'
    with open("{}/{}".format(BASEDIR,path)) as f:
        body = f.read()

    if '.css' in path:
        t = 'text/css'
    if '.js' in path:
        t = 'text/javascript'

    return Response(body, mimetype=t)

if __name__=='__main__':
    app_instance_id = os.environ['APP_INSTANCE_ID']
    mec_base = os.environ['MEC_BASE']
    app.run("0.0.0.0", port=80)
