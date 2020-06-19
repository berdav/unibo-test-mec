#!/bin/sh

set -eu

KUBEYAML=./unibo-test-mec.yml

cleanup() {
	kubectl delete -f "$KUBEYAML" 
}

trap cleanup EXIT

cd docker-img-application
./build.sh
cd -

kubectl create -f "$KUBEYAML"

read -p  "Press a key to exit" _
