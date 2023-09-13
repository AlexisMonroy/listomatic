import functools
from flask import (
    Blueprint, flash , g, redirect, render_template, request, session, url_for
)
import requests 
from flaskr.auth import log_required
from flaskr.db import get_db
from flaskr.ebaycaller import EbayCaller
from urllib.parse import unquote


bp = Blueprint('index', __name__)

@bp.route('/', methods=('GET', 'POST'))
@log_required
def home():
    #send oauth token request
    if request.method == 'POST':
        caller = EbayCaller()
        button = request.form['button']
        
        if button == "User Sign In":
            auth_response = caller.sendRequest(button)
            auth_redirect = caller.getRedirect()
            return f'<script>window.open("{auth_redirect}", "_blank");</script>'
        #listen for call
        try:
            auth_response = caller.sendRequest(button)
            if button == "Get User Token":
                if auth_response.status_code == 200:
                    caller.addRefreshToken()
                    #if tuple: user_token and refresh_token
                    #if isinstance(caller, tuple):
                        #return render_template('index.html', caller=caller)

                    #else just oauth token    
                    caller = caller
                    print(caller)
                    return render_template('index.html', caller=caller)
            
            print('TESTING')
            print(auth_response.text)
            return render_template('index.html', auth_response=auth_response.text)
        except Exception as e:
            print("Error", str(e))
    
    return render_template('index.html')
        

@bp.route('/user_consent')
def consent():
    redirect_url = EbayCaller.getRedirect()

    return redirect(redirect_url)
 

@bp.route('/signin_test')
def signin():
    print('hello')
    signin_url = f'https://signin.ebay.com/ws/eBayISAPI.dll?SignIn&AppName=AlexisGo-pricepre-PRD-3ca7161d2-d3ef5057&ru=https%3A%2F%2Fauth.ebay.com%2Foauth2%2Fconsents%3Fclient_id%3DAlexisGo-pricepre-PRD-3ca7161d2-d3ef5057%26redirect_uri%3DAlexis_Gonzalez-AlexisGo-pricep-ufgmqsmji%26scope%3Dhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.marketing.readonly%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.marketing%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.inventory.readonly%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.inventory%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.account.readonly%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.account%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.fulfillment.readonly%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.fulfillment%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.analytics.readonly%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.finances%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.payment.dispute%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fcommerce.identity.readonly%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fcommerce.notification.subscription%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fcommerce.notification.subscription.readonly%26state%26response_type%3Dcode%26hd%26consentGiven%3Dfalse'
    return redirect(signin_url)



        

