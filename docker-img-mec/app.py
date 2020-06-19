#!/usr/bin/env python3

import os
import json
import requests
from flask import Flask, Response, request

# Base dir of the html, css and js files
BASEDIR='/var/www'

app = Flask(__name__)

appids = {}

def init_appids(app_instance_id):
    global appids

    # Default transport
    transports = [
            {
                "id": "TransId12345",
                "name": "REST",
                "description": "REST API",
                "type": "REST_HTTP",
                "protocol": "HTTP",
                "version": "2.0",
                "endpoint": {},
                "security": {
                    "oAuth2Info": {
                        "grantTypes": [
                            "OAUTH2_CLIENT_CREDENTIALS"
                            ],
                        "tokenEndpoint": "/mecSerMgmtApi/security/TokenEndPoint"
                        }
                    },
                "implSpecificInfo": {}
                }
            ]
    dns_rules = {
            'dnsRule1' : {
                "dnsRuleId": "dnsRule1",
                "domainName": "www.example.com",
                "ipAddressType": "IP_V6",
                "ipAddress": "192.0.2.0",
                "state": "ACTIVE"
            }
        }

    servicelist = [
            {
                "serInstanceId": "ServiceInstance123",
                "serName": "ExampleService",
                "serCategory": {
                    "href": "/example/catalogue1",
                    "id": "id12345",
                    "name": "RNI",
                    "version": "version1"
                    },
                "version": "ServiceVersion1",
                "state": "ACTIVE",
                "transportInfo": {
                    "id": "TransId12345",
                    "name": "REST",
                    "description": "REST API",
                    "type": "REST_HTTP",
                    "protocol": "HTTP",
                    "version": "2.0",
                    "endpoint": {},
                    "security": {
                        "oAuth2Info": {
                            "grantTypes": [
                                "OAUTH2_CLIENT_CREDENTIALS"
                                ],
                            "tokenEndpoint": "/mecSerMgmtApi/security/TokenEndPoint"
                            }
                        },
                    "implSpecificInfo": {}
                    },
                "serializer": "JSON",
                "scopeOfLocality": "MEC_SYSTEM",
                "consumedLocalOnly": False,
                "isLocal": True
                }
            ]

    appids[app_instance_id] = {}
    appids[app_instance_id]['transports'] = transports
    appids[app_instance_id]['dns_rules'] = dns_rules
    appids[app_instance_id]['servicelist'] = servicelist
    appids[app_instance_id]['servicedict'] = {}

# 8.2.2
@app.route('/transports')
def get_transports():
    global appids
    return Response(json.dumps(appids[app_instance_id]['transports']), mimetype='application/json')

# Services List
# Services Subscribe
# Services Unsubscribe
@app.route('/applications/<appId>/services', methods=[ "GET", "POST" ])
@app.route('/applications/<appId>/services/<serviceId>',
        methods=["GET", "DELETE"])
def application_services(appId, serviceId = None):
    global appids

    if request.method == 'GET':
        if serviceId != None:
            return json.dumps(appids[appId]['servicedict'][serviceId])
        else:
            return json.dumps(appids[appId]['servicelist'])

    elif request.method == 'POST':
        data = request.json
        appids[appId]['servicedict'][data['serName']] = data.copy()

        headers={'location': '/applications/{}/services/{}'.format(
            appId, data['serName']
        ) }
        
        return Response("ok", headers=headers)

    elif request.method == 'DELETE':
        print(serviceId)
        del appids[appId]['servicedict'][serviceId]
        return "ok"

# DNSRules list
# DNSRules change
@app.route('/applications/<appId>/dns_rules')
@app.route('/applications/<appId>/dns_rules/<dnsruleId>',
        defaults={'dnsruleId':None},
        methods = [ 'GET', 'PUT' ])
def dns_rules(appId,dnsruleId = None):
    global appids

    if request.method == 'GET':
        dns_rules_list = list(appids[appId]['dns_rules'].values())
        return Response(json.dumps(dns_rules_list), mimetype='application/json');

    elif request.method == 'PUT':
        appids[appId]['dns_rules'][dnsruleId] = json.loads(request.data)
        return "ok"

if __name__=='__main__':
    app_instance_id = os.environ['APP_INSTANCE_ID']
    init_appids(app_instance_id)
    app.run("0.0.0.0", port=80)
