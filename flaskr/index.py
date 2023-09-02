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

    print(oauth_response)

@bp.route('/user_consent')
def consent():
    signin_url = "https://auth.ebay.com/oauth2/authorize?client_id=AlexisGo-pricepre-PRD-3ca7161d2-d3ef5057&prompt=login&redirect_uri=Alexis_Monroy-AlexisMo-pricep-wunhoeu&response_type=code&scope=https://api.ebay.com/oauth/api_scope"
    return redirect(signin_url) 
        

