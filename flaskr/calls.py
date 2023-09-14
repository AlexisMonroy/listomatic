import functools
from flask import (
    Blueprint, flash , g, redirect, render_template, request, session, url_for
)
import requests 
from flaskr.auth import log_required
from flaskr.db import get_db

bp = Blueprint('calls', __name__, url_prefix='/calls')

@bp.route("/", methods=('GET', 'POST'))
def callsIndex():
    return render_template("404.html")