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
            form_data = {}

            if request.form is not None:

                for key in request.form:
                    form_data[key] = request.form[key]
                    print(form_data[key])
                #ADD GUARD RAIL TO CHECK IF BOOK ENTRY EXISTS
                #PROBABLY NEED TO RETHINK SCHEMA AND ADD ID COLUMN FOR PRODUCTS
                db = get_db()
                cursor = db.cursor()
                cursor.execute(
                    'INSERT into books (user_id, quantity, title, author, price, description, condition, height, width, length, weight_maj, weight_min, pictures, illustrator, genre, publisher, publication_year) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (g.user['id'], form_data['title'], form_data['author'], form_data['quantity'], form_data['price'], form_data['description'], form_data['condition'], form_data['height'], form_data['width'], form_data['length'], form_data['majWeight'], form_data['minWeight'], form_data['pictures'], form_data['illustrator'], form_data['genre'], form_data['publisher'], form_data['publicationYear'])
                )
                db.commit()
                cursor.close()

                return render_template('calls/callIndex.html', form_data=form_data)
        
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
        
        print("Upload is None: ", upload)
        return render_template('calls/callIndex.html', upload=upload)

        
    return render_template('calls/callIndex.html')