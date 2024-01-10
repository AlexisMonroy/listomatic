import functools
from flask import (
    Blueprint, flash , g, redirect, render_template, request, session, url_for
)
import requests 
from flaskr.auth import log_required
from flaskr.db import get_db
from flaskr.modules.ebayCalls import ebayApiCaller
from flaskr.modules.dbmanager import DatabaseManager

bp = Blueprint('calls', __name__, url_prefix='/calls')

@bp.route("/", methods=('GET', 'POST'))
def callsIndex():
   
    if request.method == 'POST':
        
        caller = ebayApiCaller()
        dbManager = DatabaseManager()

        dbButton = request.form.get("uploadToDb")
        callButton = request.form.get("button")

        if  dbButton is not None:

            try:
                csvFile = "\\" + request.form["csvFile"] + ".csv"  
                dbResponse = dbManager.upload_csv(csvFile)
                #print(dbResponse)
                return render_template('calls/callIndex.html', caller=dbResponse)
            
            except Exception as e:
                print("Error", str(e))
                return render_template('calls/callIndex.html', caller = str(e))
            
        if callButton is not None:
                try:
                    callResponse = caller.getCommand(callButton)
                    print(callResponse)
                    return render_template('calls/callIndex.html', caller=callResponse)
                
                except Exception as e:
                    print("Error: ", str(e))
               
                
    return render_template('calls/callIndex.html')