#!/bin/bash

# create logs directory and make it writable by everyone
mkdir -p logs
chmod 777 logs

# create cache directory
mkdir -p /tmp/django_f4k_cache

echo "Pulling from repository ..."
hg pull
wait $!

RET=$?
if [[ ${RET} != 0 ]]
then
    exit ${RET}
fi

echo "Updating local copy ..."
hg update
wait $!

RET=$?
if [[ ${RET} != 0 ]]
then
    exit ${RET}
fi

echo "Trigger WSGI reload ..."
touch django_ui/wsgi.py
wait $!

RET=$?
if [[ ${RET} != 0 ]]
then
    exit ${RET}
fi