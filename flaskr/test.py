import functools
from flask import (
    Blueprint, flash , g, redirect, render_template, request, session, url_for
)
import requests 

class Oauth (object):
    #initialize values for app token request
    def __init__(self):
        self.url = "https://api.ebay.com/identity/v1/oauth2/token"
        self.headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic QWxleGlzR28tcHJpY2VwcmUtUFJELTNjYTcxNjFkMi1kM2VmNTA1NzpQUkQtY2E3MTYxZDJhNThiLTY2M2ItNGM4Ny05Y2VjLThjYmQ='
}
        self.body = {
            'grant_type': 'client_credentials',
            'scope': 'https://api.ebay.com/oauth/api_scopefdsafd'
        }
    
    def __str__(self):
        print(self.oauth_response.text)

    def __repr__(self):
        print(self.oauth_response)
    #send app token request to Ebay API
    def get_auth(self):
        self.error = False
        self.oauth_response = requests.post(self.url, headers=self.headers, data=self.body)

        if not self.oauth_response.ok:
            raise Exception(f"Error: {self.oauth_response.status_code}\nApp authorization failed. Review your credentials before trying again.")
            self.error = True
        return self.oauth_response, self.error
