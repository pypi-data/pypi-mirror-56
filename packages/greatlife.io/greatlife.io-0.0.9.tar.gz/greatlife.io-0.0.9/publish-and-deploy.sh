#!/usr/bin/env bash

wst test

set -ex

wst publish

ssh -T great-life <<EOF
set -e

sudo su -

echo [ Show what\'s running ]
ps -eaf | grep web-app | grep -v grep

echo [ Updating greatlife.io ]
app update --wait greatlife.io

echo [ Stop apps ]
killall web-app

echo [ Wait a second to make sure apps are down ]
sleep 1

echo [ Show what\'s running ]
ps -eaf | grep web-app | grep -v grep

echo [ Start apps ]
web-app --port 80 &>/tmp/web-app.out &

echo [ Wait a second to make sure apps stay up ]
sleep 1

echo [ Show what\'s running ]
ps -eaf | grep web-app | grep -v grep

EOF
