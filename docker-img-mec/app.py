#!/usr/bin/env python3

import os
import uuid
import json
import requests
from flask import Flask, Response, request

notification_callback = ''

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
                "ipAddressType": "IP_V4",
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

    subscriptionlist = [
            {
              "_links": {
                "self": {
                  "href": "/mecSerMgmtApi/example"
                },
                "subscriptions": [
                  {
                    "href": "/mecSerMgmtApi/example",
                    "rel": "string"
                  }
                ]
              }
            }
            ]

    appids[app_instance_id] = {}
    appids[app_instance_id]['transports'] = transports
    appids[app_instance_id]['dns_rules'] = dns_rules
    appids[app_instance_id]['servicelist'] = servicelist
    appids[app_instance_id]['subscriptionlist'] = subscriptionlist
    appids[app_instance_id]['servicedict'] = {}
    appids[app_instance_id]['subscriptiondict'] = {}

# 8.2.2
@app.route('/mec_service_mgmt/v1/transports')
def get_transports():
    global appids
    return Response(json.dumps(appids[app_instance_id]['transports']), mimetype='application/json')

# Services List
# Services Subscribe
# Services Unsubscribe
@app.route('/mec_service_mgmt/v1/applications/<appId>/services', methods=[ "GET", "POST" ])
@app.route('/mec_service_mgmt/v1/applications/<appId>/services/<serviceId>',
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

        # Call notification upon the creation of a new service
        if notification_callback != '':
            requests.get(notification_callback)
        
        return Response("ok", headers=headers)

    elif request.method == 'DELETE':
        del appids[appId]['servicedict'][serviceId]
        return "ok"

# DNSRules list
# DNSRules change
@app.route('/mec_app_support/v1/applications/<appId>/dns_rules')
@app.route('/mec_app_support/v1/applications/<appId>/dns_rules/<dnsruleId>',
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

# Notifications List
# Notifications Subscribe
# Notifications Unsubscribe
@app.route('/mec_service_mgmt/v1/applications/<appId>/subscriptions', methods=[ "GET", "POST" ])
@app.route('/mec_service_mgmt/v1/applications/<appId>/subscriptions/<subscriptionId>',
        methods=["GET", "DELETE"])
def application_subscriptions(appId, subscriptionId = None):
    global appids
    global notification_callback

    if request.method == 'GET':
        if subscriptionId != None:
            return json.dumps(appids[appId]['subscriptiondict'][subscriptionId])
        else:
            return json.dumps(appids[appId]['subscriptionlist'])

    elif request.method == 'POST':
        data = request.json
        notification_id = str(uuid.uuid1())
        appids[appId]['subscriptiondict'][notification_id] = data.copy()

        headers={'location': '/applications/{}/services/{}'.format(
            appId, notification_id
        ) }

        notification_callback = "http://{}/{}".format(
                request.remote_addr,
                data['_links']['self']['href']
        )
        
        return Response("ok", headers=headers)

    elif request.method == 'DELETE':
        if subscriptionId != None:
            del appids[appId]['subscriptiondict'][subscriptionId]
        return "ok"

if __name__=='__main__':
    app_instance_id = os.environ['APP_INSTANCE_ID']
    init_appids(app_instance_id)
    app.run("0.0.0.0", port=80)
