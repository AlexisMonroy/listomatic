import functools
from flask import (
    Blueprint, flash , g, redirect, render_template, request, session, url_for
)

import requests 
from urllib.parse import unquote
from flaskr.db import get_db

class EbayCaller(object):
    #initialize values for app token request
    def __init__(self):
        #app Oauth creds
        self.oauthUrl= "https://api.ebay.com/identity/v1/oauth2/token"
        
        self.oauthHeaders = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic QWxleGlzR28tcHJpY2VwcmUtUFJELTNjYTcxNjFkMi1kM2VmNTA1NzpQUkQtY2E3MTYxZDJhNThiLTY2M2ItNGM4Ny05Y2VjLThjYmQ='
}
        self.appTokenBody = {
            'grant_type': 'client_credentials',
            'scope': 'https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/commerce.identity.readonly'
        }
        #User Consent Request
        self.consentUrl = 'https://auth.ebay.com/oauth2/authorize'

        #dev credentials, RuName 
        self.consentBody = {
            'client_id': 'AlexisGo-pricepre-PRD-3ca7161d2-d3ef5057',
            'redirect_uri': 'Alexis_Gonzalez-AlexisGo-pricep-ufgmqsmji',
            'response_type': 'code',
            'scope': 'https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/commerce.identity.readonly',
        }
        self.encoded_string = 'v%5E1.1%23i%5E1%23r%5E1%23f%5E0%23I%5E3%23p%5E3%23t%5EUl41Xzc6MTE2RTU5NUQ1OERCMzlEMUMxNUY3N0QxNTRBNjJGRjRfMl8xI0VeMjYw'
        self.decoded_string = unquote(self.encoded_string)

        #print(decoded_url)
        self.userTokenBody = {
                'grant_type': 'authorization_code',
                'code': f'{self.decoded_string}',
                'redirect_uri': 'Alexis_Gonzalez-AlexisGo-pricep-ufgmqsmji'
            }
        self.uri = 'https://apiz.ebay.com/commerce/identity/v1/user/'

        self.user_headers = {'Authorization': 'Bearer v^1.1#i^1#p^3#f^0#I^3#r^0#t^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'}
    #Get DataBase    

    #Specify App or Client Auth Flow
    def sendRequest(self, command):

        command_actions = {
            "Start Auth Flow": lambda: requests.post(self.oauthUrl, headers=self.oauthHeaders, data=self.appTokenBody),
            "User Sign In": lambda: requests.get(self.consentUrl, params=self.consentBody),
            "Get User Token": lambda: requests.post(self.oauthUrl, headers=self.oauthHeaders, data=self.userTokenBody),
            "Get User Info": lambda: requests.get(self.uri, headers=self.user_headers)
        }

        action = command_actions.get(command)
        if action:
            self.authResponse = action()
            return self.authResponse

        self.authResponse = None
        return None

    #Return Response Status Code and Text
    def __str__(self):
        #could insert a guard rail here
         if self.authResponse is not None:
            self.statusCode = self.authResponse.status_code
            self.responseText = self.authResponse.text
            #self.responseData = self.authResponse.json()
            return f"{self.statusCode}\n{self.responseText}"
         
         raise Exception("There is no response. Request not sent.")
    
    #Add either App or User Token to DB
    def addOauthToken(self):
        if self.authResponse is not None:
            status_code = self.authResponse.status_code
            if status_code == 200:  
                self.responseJson = self.authResponse.json()

                if not self.responseJson.get("access_token"):
                    raise Exception("No access token available")
                
                self.token = self.responseJson("access_token")

                if self.token is not None:

                    self.db = get_db()
                    self.cursor = self.db.cursor()
                    self.user_id = self.cursor.execute(
                        'SELECT user_id FROM user_tokens where user_id = (?)',
                        (g.user['id'],)
                    ).fetchone()
                    if self.user_id is not None:

                        if self.user_id == g.user['id']:

                            self.cursor.execute(
                                'UPDATE user_tokens SET user_id = (?), oauth_token = (?) WHERE user_id = (?)',
                                (g.user['id'], self.token, g.user['id'])
                            )

                            self.db.commit()
                            self.cursor.close()
                            return self.token
                        
                    self.cursor.execute(
                        'INSERT into user_tokens (user_id, oauth_token) VALUES (?, ?)',
                        (g.user['id'], self.token)
                    )
                    self.db.commit()
                    self.cursor.close()
                    return self.token
                    
                    raise Exception("User information not found.")
                
                raise Exception("There is no token. Error retrieving information.")
            
            raise Exception("Error with request.")
            
        raise Exception("There is no response. Request not sent.")
            
    def addRefreshToken(self):
        if self.authResponse is not None:
            status_code = self.authResponse.status_code
            if status_code == 200: 
                self.responseJson = self.authResponse.json() 
                self.token = self.responseJson["access_token"]
                self.refreshToken = self.responseJson["refresh_token"]

                if self.token is not None:

                    self.db = get_db()
                    self.cursor = self.db.cursor()
                    self.user_id = self.cursor.execute(
                        'SELECT user_id FROM user_tokens where user_id = (?)',
                        (g.user['id'],)
                    ).fetchone()

                    if self.user_id is not None:

                        if self.user_id == g.user['id']:

                            self.db = get_db()
                            self.cursor = self.db.cursor()
                            self.cursor.execute(
                                'UPDATE user_tokens SET user_token = (?), refresh_token = (?) where user_id = (?)',
                                (self.token, self.refreshToken, g.user['id'])
                            )
                            self.db.commit()
                            self.cursor.close()
                            return self.token, self.refreshToken
                        
                    self.cursor.execute(
                        'INSERT into user_tokens (user_id, user_token, refresh_token) VALUES (?, ?, ?)',
                        (g.user['id'], self.token, self.refreshToken)
                    )
                    self.db.commit()
                    self.cursor.close()
                    return self.token, self.refreshToken
                
                    raise Exception("User information not found.")
                
                raise Exception("There is no token. Error retrieving information.")
            
            raise Exception("Error with request.")
        
        raise Exception("There is no response. Request not sent.")

    def getRedirect(self):
        self.redirectUrl = self.authResponse.url
        return self.redirectUrl
    
    def testCall(self, command):
        if command == "app":
            return "Test successful"
        else:
            return "Failure"  