import os

from flask import Flask, request, make_response, session, render_template, redirect, url_for
from postdrop.database import session as db
from postdrop.models import *
app = Flask(__name__)

app.secret_key = os.urandom(24) # TODO: Change to static value in production!
# TODO: Set app.config['SERVER_NAME'] to hostname in production.

# NOTE: Must run python3 -m makesgame.database before first run of webserver. Needed to create database.

