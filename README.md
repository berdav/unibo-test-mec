# Unibo Test MEC

![Unibo-test-MEC logo](https://github.com/berdav/unibo-test-mec/blob/master/readme-images/logo.png?raw=true)

Unibo Test MEC is a testing application for the MEC Infrastructure.

While testing the infrastructure capabilities, it can be used to create
a complete use-case for the interaction with the MEC.

The main application goals are the easiness of use and the support of
the MEC 011 API.

## Application design
This application is composed of a web server that communicates with the
MEC platform, exposing an easy to use interface.

The webserver does not need any configuration besides from the
infrastructure ones such as `application-id` and the `MEC endpoint` (the
MEC platform IP address and port in form of an HTTP URL) which is
required to perform the API calls.

## Installation
To execute the application you need to compile the docker images, put
them on a reachable image repository (or use the local one)

```bash
$ sudo apt-get install docker.io
```

To do so you can use the helper script `build.sh` placed in the
docker-application directory.  You can use the `run.sh` or
`run-local.sh` scripts to compile and run the application in a single
step.  Otherwise you can issue a `docker build` command in the
docker-application directory

```bash
# ./run-local.sh
```

### Kubernetes Build
The application has a `kubernetes` descriptor `unibo-test-mec.yml`.
You can import this file and modify it accordingly to put it on your
Kubernetes cluster.

The `run.sh` script will generate the required image and instantiate it
in the default Kubernetes cluster configured previously (a standard
installation would be sufficient).  The script runs without parameters:

```bash
# ./run.sh
```

## Usage
The application is designed to be used with small-to-any configuration.
Besides from that, a little configuration is required to make it
interacts with the MEC platform.  To do so, start the application using
the preferred method above.  For instance to start it with docker you
can simply run:
```bash
# ./run-local.sh
```

After this step, navigate with a web browser to your docker container
endpoint (usually it would be at the IP 172.17.0.2, but it can vary
depending on your configuration).

<!-- Screen generico -->

After reaching the webserver, go to the configuration tab.
<!-- Screen configurazione -->

Configure all the fields according to your needs.  After that you can
start to check the functions of your MEC application or server using the
various tabs and buttons.

For instance, if you want to retrieve the DNS configuration associated
with your application you can click on the button "..."
<!-- Screen utilizzo -->

### MEC simulation
To simulate a dummy MEC platform, you can use the `docker-img-mec` image
which can be built and run using the `run-mec.sh` script with no
parameters.

## Implemented MEC 011 APIs
|API Method and URL                                                   | Implemented | Notes                                              | Description URL |
|---------------------------------------------------------------------|-------------|----------------------------------------------------|-----------------|
|`GET    /applications/{appInstanceId}/subscriptions`                 |✔️            |                                                    |[Forge ETSI](https://forge.etsi.org/swagger/ui/?url=https://forge.etsi.org/rep/mec/gs011-app-enablement-api/raw/master/MecServiceMgmtApi.yaml#/appSubscriptions/ApplicationsSubscriptions_GET) |
|`POST   /applications/{appInstanceId}/subscriptions`                 |✔️            |                                                    |[Forge ETSI](https://forge.etsi.org/swagger/ui/?url=https://forge.etsi.org/rep/mec/gs011-app-enablement-api/raw/master/MecServiceMgmtApi.yaml#/appSubscriptions/ApplicationsSubscriptions_POST) |
|`GET    /applications/{appInstanceId}/subscriptions/{subscriptionId}`|             |                                                    |[Forge ETSI](https://forge.etsi.org/swagger/ui/?url=https://forge.etsi.org/rep/mec/gs011-app-enablement-api/raw/master/MecServiceMgmtApi.yaml#/appSubscriptions/ApplicationsSubscription_GET) |
|`DELETE /applications/{appInstanceId}/subscriptions/{subscriptionId}`|✔️            |                                                    |[Forge ETSI](https://forge.etsi.org/swagger/ui/?https://forge.etsi.org/rep/mec/gs011-app-enablement-api/raw/master/MecServiceMgmtApi.yaml#/appSubscriptions/ApplicationsSubscription_DELETE) |
|`GET    /applications/{appInstanceId}/services`                      |✔️            |                                                    |[Forge ETSI](https://forge.etsi.org/swagger/ui/?https://forge.etsi.org/rep/mec/gs011-app-enablement-api/raw/master/MecServiceMgmtApi.yaml#/appServices/AppServices_GET) |
|`POST   /applications/{appInstanceId}/services`                      |✔️            |                                                    |[Forge ETSI](https://forge.etsi.org/swagger/ui/?https://forge.etsi.org/rep/mec/gs011-app-enablement-api/raw/master/MecServiceMgmtApi.yaml#/appServices/AppServices_POST) |
|`GET    /applications/{appInstanceId}/services/{serviceId}`          |             |                                                    |[Forge ETSI](https://forge.etsi.org/swagger/ui/?https://forge.etsi.org/rep/mec/gs011-app-enablement-api/raw/master/MecServiceMgmtApi.yaml#/appServices/AppServicesServiceId_GET) |
|`PUT    /applications/{appInstanceId}/services/{serviceId}`          |             |                                                    |[Forge ETSI](https://forge.etsi.org/swagger/ui/?https://forge.etsi.org/rep/mec/gs011-app-enablement-api/raw/master/MecServiceMgmtApi.yaml#/appServices/AppServicesServiceId_PUT) |
|`DELETE /applications/{appInstanceId}/services/{serviceId}`          |✔️            |                                                    |[Forge ETSI](https://forge.etsi.org/swagger/ui/?https://forge.etsi.org/rep/mec/gs011-app-enablement-api/raw/master/MecServiceMgmtApi.yaml#/appServices/AppServicesServiceId_DELETE) |
|`GET    /services`                                                   |             |                                                    |[Forge ETSI](https://forge.etsi.org/swagger/ui/?https://forge.etsi.org/rep/mec/gs011-app-enablement-api/raw/master/MecServiceMgmtApi.yaml#/services/Services_GET) |
|`GET    /services/{serviceId}`                                       |             |                                                    |[Forge ETSI](https://forge.etsi.org/swagger/ui/?https://forge.etsi.org/rep/mec/gs011-app-enablement-api/raw/master/MecServiceMgmtApi.yaml#/services/ServicesServiceId_GET) |
|`GET    /transports`                                                 |✔️            |                                                    |[Forge ETSI](https://forge.etsi.org/swagger/ui/?https://forge.etsi.org/rep/mec/gs011-app-enablement-api/raw/master/MecServiceMgmtApi.yaml#/transports/Transports_GET) |
|`GET    /applications/{appInstanceId}/traffic_rules`                 |✔️            |                                                    |[Forge ETSI](https://forge.etsi.org/swagger/ui/?https://forge.etsi.org/gitlab/mec/gs011-app-enablement-api/raw/master/MecAppSupportApi.yaml#/appTrafficRules/ApplicationsTrafficRules_GET) |
|`GET    /applications/{appInstanceId}/traffic_rules/{trafficRuleId}` |             |                                                    |[Forge ETSI](https://forge.etsi.org/swagger/ui/?https://forge.etsi.org/gitlab/mec/gs011-app-enablement-api/raw/master/MecAppSupportApi.yaml#/appTrafficRules/ApplicationsTrafficRule_GET) |
|`PUT    /applications/{appInstanceId}/traffic_rules/{trafficRuleId}` |✔️            | Supports only state modification                   |[Forge ETSI](https://forge.etsi.org/swagger/ui/?https://forge.etsi.org/gitlab/mec/gs011-app-enablement-api/raw/master/MecAppSupportApi.yaml#/appTrafficRules/ApplicationsTrafficRule_PUT) |
|`GET    /applications/{appInstanceId}/dns_rules`                     |✔️            |                                                    |[Forge ETSI](https://forge.etsi.org/swagger/ui/?https://forge.etsi.org/gitlab/mec/gs011-app-enablement-api/raw/master/MecAppSupportApi.yaml#/appDnsRules/ApplicationsDnsRules_GET) |
|`GET    /applications/{appInstanceId}/dns_rules/{dnsRuleId}`         |             |                                                    |[Forge ETSI](https://forge.etsi.org/swagger/ui/?https://forge.etsi.org/gitlab/mec/gs011-app-enablement-api/raw/master/MecAppSupportApi.yaml#/appDnsRules/ApplicationsDnsRule_GET) |
|`PUT    /applications/{appInstanceId}/dns_rules/{dnsRuleId}`         |✔️            | Supports only state modification                   |[Forge ETSI](https://forge.etsi.org/swagger/ui/?https://forge.etsi.org/gitlab/mec/gs011-app-enablement-api/raw/master/MecAppSupportApi.yaml#/appDnsRules/ApplicationsDnsRule_PUT) |
|`GET    /applications/{appInstanceId}/subscriptions`                 |✔️            |                                                    |[Forge ETSI](https://forge.etsi.org/swagger/ui/?https://forge.etsi.org/gitlab/mec/gs011-app-enablement-api/raw/master/MecAppSupportApi.yaml#/appSubscriptions/ApplicationsSubscriptions_GET) |
|`POST   /applications/{appInstanceId}/subscriptions`                 |✔️            |                                                    |[Forge ETSI](https://forge.etsi.org/swagger/ui/?https://forge.etsi.org/gitlab/mec/gs011-app-enablement-api/raw/master/MecAppSupportApi.yaml#/appSubscriptions/ApplicationsSubscriptions_POST) |
|`GET    /applications/{appInstanceId}/subscriptions/{subscriptionId}`|             |                                                    |[Forge ETSI](https://forge.etsi.org/swagger/ui/?https://forge.etsi.org/gitlab/mec/gs011-app-enablement-api/raw/master/MecAppSupportApi.yaml#/appSubscriptions/ApplicationsSubscription_GET) |
|`DELETE /applications/{appInstanceId}/subscriptions/{subscriptionId}`|✔️            |                                                    |[Forge ETSI](https://forge.etsi.org/swagger/ui/?https://forge.etsi.org/gitlab/mec/gs011-app-enablement-api/raw/master/MecAppSupportApi.yaml#/appSubscriptions/ApplicationsSubscription_DELETE) |
|`POST   /applications/{appInstanceId}/confirm_termination`           |             |                                                    |[Forge ETSI](https://forge.etsi.org/swagger/ui/?https://forge.etsi.org/gitlab/mec/gs011-app-enablement-api/raw/master/MecAppSupportApi.yaml#/appConfirmTermination/ApplicationsConfirmTermination_POST) |
|`POST   /applications/{appInstanceId}/confirm_ready`                 |✔️            | Notification via the red LED                       |[Forge ETSI](https://forge.etsi.org/swagger/ui/?https://forge.etsi.org/gitlab/mec/gs011-app-enablement-api/raw/master/MecAppSupportApi.yaml#/appConfirmReady/ApplicationsConfirmReady_POST) |
|`GET    /timing/timing_caps`                                         |✔️            |                                                    |[Forge ETSI](https://forge.etsi.org/swagger/ui/?https://forge.etsi.org/gitlab/mec/gs011-app-enablement-api/raw/master/MecAppSupportApi.yaml#/timing/TimingCaps_GET) |
|`GET    /timing/current_time`                                        |✔️            | Only application timestamp, no NTP and PTP support |[Forge ETSI](https://forge.etsi.org/swagger/ui/?https://forge.etsi.org/gitlab/mec/gs011-app-enablement-api/raw/master/MecAppSupportApi.yaml#/timing/TimingCurrentTime_GET) |
