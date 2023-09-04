import functools
from flask import (
    Blueprint, flash , g, redirect, render_template, request, session, url_for
)
import requests 


bp = Blueprint('index', __name__)

url = "https://api.ebay.com/identity/v1/oauth2/token"

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': ''
}

oauth_request = {
    'grant_type': 'client_credentials',
    'scope': 'https://api.ebay.com/oauth/api_scope'
}

oauth_response = requests.post(url, headers=headers, data=oauth_request)

if oauth_response.status_code == 200:

    print(oauth_response,'\n',oauth_response.text)

@bp.route('/user_consent')
def consent():

    url = 'https://auth.ebay.com/oauth2/authorize'

    # Define the parameters as a dictionary
    params = {
        'client_id': 'AlexisGo-pricepre-PRD-3ca7161d2-d3ef5057',
        'prompt': 'login',
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

@bp.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        url = 'https://auth.ebay.com/oauth2/authorize'

    # Define the parameters as a dictionary
        params = {
            'client_id': 'AlexisGo-pricepre-PRD-3ca7161d2-d3ef5057',
            'prompt': 'login',
            'redirect_uri': 'Alexis_Gonzalez-AlexisGo-pricep-ufgmqsmji',
            'response_type': 'code',
            'scope': 'https://api.ebay.com/oauth/api_scope',
        }

        # Send the GET request with the formatted URL
        response = requests.get(url, params=params)

    else:
        return render_template('index.html')

        

