#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/html/job-task-python-ubi/")

from app import app as application
application.secret_key = 'Holgyeim es Uraim, tisztelt Elnok Ur! Boldog Karacsonyt!'