#!/bin/sh

set -eu

cd docker-img-application
./build.sh
cd -

docker run --rm -ti \
        -e MEC_BASE="http://172.17.0.3:80" \
        -e APP_INSTANCE_ID="997fc80a-cfc1-498a-b77f-608f09506e86" \
	unibo-test-mec-application
