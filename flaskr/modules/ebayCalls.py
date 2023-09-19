import functools
from flask import (
    Blueprint, flash , g, redirect, render_template, request, session, url_for
)

import requests 
from urllib.parse import unquote
from flaskr.db import get_db

class ebayApiCaller(object):
    #will follow the structure of sendCommand function in ebayAuthorization
    def __init__(self):
        self.uri = 'https://api.ebay.com/sell/inventory/v1/location/1993_pochtecha_alexis'
        self.info_uri = 'https://apiz.ebay.com/commerce/identity/v1/user/'

        self.user_headers = None

        self.callBody = {

            'location': { 
                'address': {
                    'addressLine1': '14915 1/2 Condon Avenue',
                    'city': 'Lawndale',
                    'country': 'US'
                }     
            },
                
            'phone': '4243766461'
        }

    def getToken(self):
        self.info_header = self.user_headers
        if self.info_header is not None:
            return self.info_header

        self.db = get_db()
        self.cursor = self.db.cursor()
        self.user_id = self.cursor.execute(
            'SELECT user_id FROM user_tokens where user_id = (?)',
            (g.user['id'],)
        ).fetchone()

        if self.user_id is not None:

            self.user_oauth_token = self.cursor.execute(
            'SELECT user_token FROM user_tokens where user_id = (?)',
            (g.user['id'],)
        ).fetchone()
            if self.user_oauth_token is not None:

                self.authorization_code = str(self.user_oauth_token[0])
                self.user_headers = {
                    'Authorization': f'Bearer {self.authorization_code}', 
                    'Content-Type': 'application/json'                   
                }
                return
            
            raise Exception("No User Token Found.")
            
        raise Exception("User not found.")

    def sendRequest(self, command):

        command_actions = {
            "Create Ebay Inventory Location": lambda: requests.post(self.uri, headers=self.user_headers, json=self.callBody),
            "Get Ebay Inventory Location": lambda: requests.get(self.uri, headers=self.user_headers),
            "Get User Info": lambda: requests.get(self.info_uri, headers=self.user_headers),
    
            "Create Inventory Item": lambda: requests.post(self.oauthUrl, headers=self.oauthHeaders, data=self.appTokenBody),
            "Send Offer": lambda: requests.post(self.oauthUrl, headers=self.oauthHeaders, data=self.appTokenBody),
            "Confirm Offer": lambda: requests.post(self.oauthUrl, headers=self.oauthHeaders, data=self.appTokenBody),
            "Get Listing Details": lambda: requests.post(self.oauthUrl, headers=self.oauthHeaders, data=self.appTokenBody)
        }

        action = command_actions.get(command)
        if action:
            self.authResponse = action()
            return self.authResponse

        self.authResponse = None
        return None

    def __str__(self):
        #could insert a guard rail here
        if self.authResponse is not None:
            self.statusCode = self.authResponse.status_code
            self.responseText = self.authResponse.text
            return (f"Status Code: {self.statusCode}\nReponse Text: {self.responseText}")
        
        raise Exception("No response info. Call not sent. Recheck call parameters.")