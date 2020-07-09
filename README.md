# Unibo Test MEC

![Unibo-test-MEC logo](https://github.com/berdav/unibo-test-mec/blob/readme-modifications/readme-images/logo.png?raw=true)

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

## Implemented MEC 011 APIs
|API|Implemented|URL|
|---|-----------|---|
|   |           |   |
|   |           |   |
|   |           |   |
