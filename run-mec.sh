#!/bin/sh

set -eu

cd docker-img-mec
./build.sh
cd -

docker run --rm -ti \
        -e APP_INSTANCE_ID="997fc80a-cfc1-498a-b77f-608f09506e86" \
	unibo-test-mec-mec
