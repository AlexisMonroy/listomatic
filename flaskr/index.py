import functools
from flask import (
    Blueprint, flash , g, redirect, render_template, request, session, url_for
)
import requests 
from flaskr.auth import log_required
from flaskr.db import get_db
from urllib.parse import unquote


bp = Blueprint('index', __name__)

@bp.route('/', methods=('GET', 'POST'))
@log_required
def home():
    url = "https://api.ebay.com/identity/v1/oauth2/token"

    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic QWxleGlzR28tcHJpY2VwcmUtUFJELTNjYTcxNjFkMi1kM2VmNTA1NzpQUkQtY2E3MTYxZDJhNThiLTY2M2ItNGM4Ny05Y2VjLThjYmQ='
}
    #send oauth token request
    if request.method == 'POST':
        button = request.form['button']
        if button == 'Get User Token':
            #grab consent token
            #db = get_db()
            #cursor = db.cursor()
            #consent_token = cursor.execute(
                #'SELECT consent_token from user_tokens where user_id = (?)',
                #(g.user['id'],)
            #)
            encoded_string = 'v%5E1.1%23i%5E1%23I%5E3%23f%5E0%23p%5E3%23r%5E1%23t%5EUl41Xzg6RjVDRDIxMThFMzAwQjk4NDg5ODUzMkY0MDU1QUMzMDlfMV8xI0VeMjYw'
            decoded_string = unquote(encoded_string)

            #print(decoded_url)
            user_token_request = {
                'grant_type': 'authorization_code',
                'code': f'{decoded_string}',
                'redirect_uri': 'Alexis_Gonzalez-AlexisGo-pricep-ufgmqsmji'
            }

            user_token_response = requests.post(url, headers=headers, data=user_token_request)
            print(user_token_response.status_code)
            print(user_token_response.text)
            #if status success, get user token and refresh token, input into db
            if user_token_response.status_code == 200:
                user_token_data = user_token_response.json()
                print("Retrieved user token, brah")
                user_token = user_token_data["access_token"]
                user_refresh_token = user_token_data["refresh_token"]
                db = get_db()
                cursor = db.cursor()
                cursor.execute(
                    'UPDATE user_tokens SET user_token = (?) where user_id = (?)',
                    (user_token, g.user['id'])
                )
                db.commit()
                cursor.close()
                
                return render_template('index.html', user_token_data=user_token_data, user_refresh_token=user_refresh_token)
            else:
                return render_template('index.html')
            
        elif button == 'Get User Info':
            uri = 'https://apiz.ebay.com/commerce/identity/v1/user/'
            get_headers = {'Authorization': 'Bearer v^1.1#i^1#f^0#p^3#r^0#I^3#t^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'}

            get_user_response = requests.get(uri, headers=get_headers)
            if get_user_response.status_code == 200:
                get_user_data = get_user_response.json()
                username = get_user_data["username"]
                print(username)
                print("It worked")
                return render_template('index.html', username=username)
            else:
                return render_template('index.html')
        elif button == 'Start Auth Flow':
        #if success status, enter oauth_token into token table
            oauth_request = {
                'grant_type': 'client_credentials',
                'scope': 'https://api.ebay.com/oauth/api_scope'
            }
            oauth_response = requests.post(url, headers=headers, data=oauth_request)
            if oauth_response.status_code == 200:
                oauth_response_data = oauth_response.json()
                print("it worked")
                client_token = oauth_response_data["access_token"]
                print(client_token)
                db = get_db()
                cursor = db.cursor()
                cursor.execute(
                    'UPDATE user_tokens SET user_id = (?), oauth_token = (?)',
                    (g.user['id'], client_token)
                )
                db.commit()
                cursor.close()
                
                return render_template('index.html', oauth_response_data=oauth_response_data)
            else:
                return render_template('index.html')
    else:
        return render_template('index.html')


@bp.route('/user_consent')
def consent():

    url = 'https://auth.ebay.com/oauth2/authorize'

    # Define the parameters as a dictionary
    params = {
        'client_id': 'AlexisGo-pricepre-PRD-3ca7161d2-d3ef5057',
        'redirect_uri': 'Alexis_Gonzalez-AlexisGo-pricep-ufgmqsmji',
        'response_type': 'code',
        'scope': 'https://api.ebay.com/oauth/api_scope',
    }

    # Send the GET request with the formatted URL
    response = requests.get(url, params=params)

    redirect_url = response.url

    return redirect(redirect_url)
 

@bp.route('/signin_test')
def signin():
    print('hello')
    signin_url = f'https://signin.ebay.com/ws/eBayISAPI.dll?SignIn&AppName=AlexisGo-pricepre-PRD-3ca7161d2-d3ef5057&ru=https%3A%2F%2Fauth.ebay.com%2Foauth2%2Fconsents%3Fclient_id%3DAlexisGo-pricepre-PRD-3ca7161d2-d3ef5057%26redirect_uri%3DAlexis_Gonzalez-AlexisGo-pricep-ufgmqsmji%26scope%3Dhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.marketing.readonly%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.marketing%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.inventory.readonly%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.inventory%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.account.readonly%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.account%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.fulfillment.readonly%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.fulfillment%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.analytics.readonly%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.finances%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fsell.payment.dispute%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fcommerce.identity.readonly%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fcommerce.notification.subscription%2Bhttps%253A%252F%252Fapi.ebay.com%252Foauth%252Fapi_scope%252Fcommerce.notification.subscription.readonly%26state%26response_type%3Dcode%26hd%26consentGiven%3Dfalse'
    return redirect(signin_url)



        

