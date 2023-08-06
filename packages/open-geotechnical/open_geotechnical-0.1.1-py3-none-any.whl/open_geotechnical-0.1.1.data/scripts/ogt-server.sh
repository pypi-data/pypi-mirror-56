#!/bin/bash

export FLASK_DEBUG="1"
export FLASK_APP=ogtserver.main.py
/usr/bin/python2.7 -m flask run --host=0.0.0.0 --port=1377


