#!/bin/sh

rm -rf static/js static/css
cp -r tweetmoof-web/build/static/js static/js
cp -r tweetmoof-web/build/static/css static/css
ls static/js
ls static/css
