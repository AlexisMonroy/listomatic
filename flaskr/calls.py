import functools
from flask import (
    Blueprint, flash , g, redirect, render_template, request, session, url_for
)
import requests 
from flaskr.auth import log_required
from flaskr.db import get_db
from flaskr.modules.ebayCalls import ebayApiCaller

bp = Blueprint('calls', __name__, url_prefix='/calls')

@bp.route("/", methods=('GET', 'POST'))
def callsIndex():
    if request.method == 'POST':

        upload = request.form.get('upload')
        if upload is not None:
            title = request.form.get('title')
            print(title)
            return render_template('calls/callIndex.html', title=title)
        
        caller = ebayApiCaller()
        button = request.form['button']
        try:

            if button == "Create Ebay Inventory Location":

                error = None
                caller.getToken()
                auth_response = caller.sendRequest(button)
                if auth_response.status_code == 200:
                    caller   
                    print(caller)

                    return render_template('calls/callIndex.html', caller=caller)
                caller
                return render_template('calls/callIndex.html', caller=caller)
                
                
            if button == "Get Ebay Inventory Location":

                error = None
                caller.getToken()
                auth_response = caller.sendRequest(button)
                if auth_response.status_code == 200:
                    caller   
                    print(caller)

                    return render_template('calls/callIndex.html', caller=caller)
                caller
                return render_template('calls/callIndex.html', caller=caller)
                
            if button == "Get User Info":

                error = None
                caller.getToken()
                auth_response = caller.sendRequest(button)
                if auth_response.status_code == 200:
                    caller   
                    print(caller)


                    return render_template('calls/callIndex.html', caller=caller)
                
                caller
                return render_template('calls/callIndex.html', caller=caller)
                
        except Exception as e:
            print("Error", str(e)) 
        
        print(upload)
        return render_template('calls/callIndex.html', upload=upload)

        
    return render_template('calls/callIndex.html')