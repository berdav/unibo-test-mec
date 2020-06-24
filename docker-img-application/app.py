#!/usr/bin/env python3

# unibo-test-application - Testbed for MEC API 011 applications
# This application is part of unibo-test-mec
# Copyright (C) 2020  Davide Berardi <berardi.dav@gmail.com>
#                     Davide Borsatti <davide.borsatti@studio.unibo.it>
#                     Franco Callegati <franco.callegati@unibo.it>
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
# USA

# TODO:
#  - This can be transformed into a framework.
#
# TODO:
#  - remove hardcoded and environmental variable with a configurable
#    page
#
# TODO:
#  - README.md

import os
import json
import requests
import datetime
import subprocess
from flask import Flask, Response, request

def get_nic():
    for k in os.listdir('/sys/class/net'):
        if k != 'lo':
            return k;

def set_to_list(s):
    if isinstance(s, set):
        return list(s)
    return None

# Base dir of the html, css and js files
BASEDIR='/var/www'
# MEC Service endpoint
MEC_SERVICE_MGMT="mec_service_mgmt/v1"
# MEC Application endpoint
MEC_APP_SUPPORT="mec_app_support/v1"

# Application business endpoint
EXTERNAL_ENDPOINT='/external_endpoint'
# Callback proposed
CALLBACK_URL='/_mecSerMgmtApi/callback'

# Network interface for PTP daemon
INTERFACE=get_nic()

# XXX Unsupported in alpine atm.
PTP_COMMAND="ptp4l -A -4 -S -i {}".format(INTERFACE)

# The endpoint we will contact to get data from the application.
other_application_uri=''

# Service ID, this will be set by the MEC
service_id = ''

# Flask initialization.
app = Flask(__name__)

# MEC Base Endpoint.
mec_base = ''

# Application instance, this can be set by environment variables and
#  overwritten within the application
app_instance_id = ''

# The service we are searching in the services list to be notified on.
target_service = ''

# Default service data, this can be edited within the application
service_data = {
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
        "id": 'TransId12345' ,
        "name": "REST",
        "description": "REST API",
        "type": "REST_HTTP",
        "protocol": "HTTP",
        "version": "2.0",
        "endpoint": { EXTERNAL_ENDPOINT },
        "security": {
            "oAuth2Info": {
                "grantTypes": [ ],
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

# The application has been notified
application_notified = False

# Transport API
@app.route('/transports')
def transports():
    global mec_base
    query_base = "{}/{}/transports".format(
            mec_base,
            MEC_SERVICE_MGMT
    )
    r = requests.get(query_base)

    return r.text


# Services API
@app.route('/services')
def services():
    global mec_base
    global app_instance_id
    global other_application_uri
    out = ''
    query_base = "{}/{}/applications/{}/services".format(
            mec_base,
            MEC_SERVICE_MGMT,
            app_instance_id
    )

    r = requests.get(query_base)

    # Get transport endpoint from services
    try:
        srvs = json.loads(r.text)
        for s in srvs:
            if s['serName'] != target_service:
                continue
            other_application_uri = s['transportInfo']['endpoint']['uris'][0]
    except Exception as e:
        print(str(e))

    return r.text

# Subscribe to service
@app.route('/services/subscribe')
def service_subscribe():
    data = service_data

    query_base = "{}/{}/applications/{}/services".format(
            mec_base,
            MEC_SERVICE_MGMT,
            app_instance_id
    )

    headers = {"content-type": "application/json"}
    r = requests.post(query_base, data=json.dumps(data), headers=headers)

    # XXX we don't have any slash in the url?
    service_id = r.headers['location'].split('/')[-1]

    return 'New service_id: {}'.format(service_id)

# Unsubscribe a service
@app.route('/services/unsubscribe')
def service_unsubscribe():
    query_base = "{}/{}/applications/{}/services/{}".format(
            mec_base,
            MEC_SERVICE_MGMT,
            app_instance_id,
            service_id
    )
    r = requests.delete(query_base)
    return r.text

# Get DNS Rules
@app.route('/dns_rules')
def dns_rules():
    global dns_rules

    query_base = "{}/{}/applications/{}/dns_rules".format(
            mec_base,
            MEC_APP_SUPPORT,
            app_instance_id
    )
    r = requests.get(query_base)

    dns_rules = json.loads(r.text)

    return r.text

# Modify DNS rules
@app.route('/dns_rules/<modification>')
def dns_rule_modify(modification):
    global dns_rules
    dns_rule = dns_rules[0]

    query_base = "{}/{}/applications/{}/dns_rules/{}".format(
            mec_base,
            MEC_APP_SUPPORT,
            app_instance_id,
            dns_rule['dnsRuleId']
    )

    dns_rule["state"] = modification
    headers = { 'content-type': 'application/json' }
    r = requests.put(query_base, data=json.dumps(dns_rule), headers=headers)
    return json.dumps(dns_rule)

# Notifications API
@app.route('/notifications')
def notifications():
    query_base = "{}/{}/applications/{}/subscriptions".format(
            mec_base,
            MEC_SERVICE_MGMT,
            app_instance_id
    )

    r = requests.get(query_base)

    return r.text

# Subscribe to notifications
@app.route('/notifications/subscribe')
def notifications_subscribe():
    global service_id

    # Catch all notification endpoint
    data = {
      "subscriptionType": "SerAvailabilityNotificationSubscription",
      "callbackReference": "string",
      "_links": {
        "self": {
          "href": CALLBACK_URL
        }
      }
    }

    query_base = "{}/{}/applications/{}/subscriptions".format(
            mec_base,
            MEC_SERVICE_MGMT,
            app_instance_id
    )

    headers = {"content-type": "application/json"}
    r = requests.post(query_base, data=json.dumps(data), headers=headers)

    # XXX we don't have any slash in the url?
    service_id = r.headers['location'].split('/')[-1]

    return 'New notification_id: {}'.format(service_id)

# Unsubscribe notifications
@app.route('/notifications/unsubscribe')
def notification_unsubscribe():
    query_base = "{}/{}/applications/{}/subscriptions/{}".format(
            mec_base,
            MEC_SERVICE_MGMT,
            app_instance_id,
            service_id
    )
    r = requests.delete(query_base)
    return r.text

@app.route('/notifications/notify_ready')
def notification_confirm_ready():
    query_base = "{}/{}/applications/{}/confirm_ready".format(
            mec_base,
            MEC_APP_SUPPORT,
            app_instance_id
    )

    ready_indication = { "indication": "READY" }
    headers = { 'content-type': 'application/json' }

    r = requests.post(query_base, data=json.dumps(ready_indication), headers=headers)
    return r.text

# Time API
@app.route('/timings/timing_caps')
def timing_timing_caps():
    query_base = "{}/{}/timing/timing_caps".format(
            mec_base,
            MEC_APP_SUPPORT,
            app_instance_id,
            service_id
    )
    r = requests.get(query_base)
    return r.text

@app.route('/timings/current_time')
def timing_current_time():
    query_base = "{}/{}/timing/current_time".format(
            mec_base,
            MEC_APP_SUPPORT,
            app_instance_id,
            service_id
    )
    r = requests.get(query_base)
    return r.text

@app.route('/timings/_ptp_status')
def timing_ptp_status():
    global ptp_process
    if ptp_process.poll != None:
        return "Not Running"
    return "Running"

@app.route('/timings/_start_ptp')
def timing_ptp_start():
    global ptp_process
    if timing_ptp_status() != "Not Running":
        return "Already running"

    ptp_process = subprocess.Popen(PTP_COMMAND.split(" "))
    return "Unimplemented"

@app.route('/timings/_ptp_time')
def timing_ptp_time():
    return str(datetime.datetime.now())

# Get Traffic Rules
@app.route('/traffic_rules')
def traffic_rules():
    global traffic_rules

    query_base = "{}/{}/applications/{}/traffic_rules".format(
            mec_base,
            MEC_APP_SUPPORT,
            app_instance_id
    )
    r = requests.get(query_base)

    traffic_rules = json.loads(r.text)

    return r.text

# Modify DNS rules
@app.route('/traffic_rules/<modification>')
def traffic_rule_modify(modification):
    global traffic_rules
    traffic_rule = traffic_rules[0]

    query_base = "{}/{}/applications/{}/traffic_rules/{}".format(
            mec_base,
            MEC_APP_SUPPORT,
            app_instance_id,
            traffic_rule['trafficRuleId']
    )

    traffic_rule["state"] = modification
    headers = { 'content-type': 'application/json' }
    r = requests.put(query_base, data=json.dumps(traffic_rule), headers=headers)
    return json.dumps(traffic_rule)

# Catch all, return the retrieved file
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

@app.route("/_get_application_notice")
def get_application_notice():
    return str(application_notified);


# Callback for the notification framework
@app.route(CALLBACK_URL)
def service_notification_callback():
    global application_notified
    application_notified = True

    # XXX We should notify back using a structured json?
    return ""

# Query the other application
@app.route('/_contactapplication')
def contact_application():
    query_base = "{}".format(
            other_application_uri
    )

    r = requests.get(query_base)
    return r.text

# Application endpoint, contacting this will return information
#  on the running application
@app.route(EXTERNAL_ENDPOINT)
def external_endpoint():
    result = { }
    result['app_instance_id'] = app_instance_id
    result['mec_base'] = mec_base
    result['application_notified'] = application_notified
    result['other_application_uri'] = other_application_uri
    result['traffic_rules'] = traffic_rules
    result['service_id'] = service_id
    result['callback_url'] = CALLBACK_URL
    result['dns_rules'] = dns_rules

    # And a dynamic value
    result['current_time'] = str(time.time())

    return json.dumps(result)

# Get and change the configurations
@app.route("/_configuration", methods=[ "GET", "POST" ])
def configuration():
    global mec_base
    global target_service
    global other_application_uri
    global app_instance_id
    global service_data

    if request.method == 'GET':
        result = { }
        result['mec_base'] = mec_base
        result['target_service'] = target_service
        result['other_application_uri'] = other_application_uri
        result['app_instance_id'] = app_instance_id
        result['service_data'] = service_data

        return json.dumps(result, default=set_to_list)
    elif request.method == 'POST':
        r = request.json
        mec_base = r['mec_base']
        target_service = r['target_service']
        other_application_uri = r['other_application_uri']
        app_instance_id = r['app_instance_id']
        service_data = r['service_data']
        return "ok"


if __name__=='__main__':
    try:
        app_instance_id = os.environ['APP_INSTANCE_ID']
        mec_base = os.environ['MEC_BASE']
    except:
        # No configuration for now, will except when a request to an
        # invalid endpoint will be made.
        pass
    app.run("0.0.0.0", port=80)
