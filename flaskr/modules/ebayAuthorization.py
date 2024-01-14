import functools
from flask import (
    Blueprint, flash , g, redirect, render_template, request, session, url_for
)

import requests 
from urllib.parse import unquote
from flaskr.db import get_db

class ebayTokenizer(object):
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
            'scope': 'https://api.ebay.com/oauth/api_scope'
        }
        #User Consent Request
        self.consentUrl = 'https://auth.ebay.com/oauth2/authorize'

        #dev credentials, RuName 
        self.consentBody = {
            'client_id': 'AlexisGo-pricepre-PRD-3ca7161d2-d3ef5057',
            'redirect_uri': 'Alexis_Gonzalez-AlexisGo-pricep-ufgmqsmji',
            'response_type': 'code',
            'scope': 'https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/commerce.identity.readonly https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.account',
        }
        self.encoded_string = 'v%5E1.1%23i%5E1%23f%5E0%23I%5E3%23r%5E1%23p%5E3%23t%5EUl41XzU6ODNBQjgwNDE4Q0IyOTY3RjUzQkM3M0Q2OTg2NkRDMTBfMl8xI0VeMjYw'
        self.decoded_string = unquote(self.encoded_string)

        #print(decoded_url)
        self.userTokenBody = {
                'grant_type': 'authorization_code',
                'code': f'{self.decoded_string}',
                'redirect_uri': 'Alexis_Gonzalez-AlexisGo-pricep-ufgmqsmji'
            }
        self.uri = 'https://apiz.ebay.com/commerce/identity/v1/user/'
    
        self.user_headers = None
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
            self.db = get_db()
            self.cursor = self.db.cursor()
            self.user_tokens_info= self.cursor.execute(
                'SELECT user_id, user_token, refresh_token, consent_token FROM user_tokens where user_id = (?)',
                (g.user['id'],)
            ).fetchone()
            self.tokens_string = str(self.user_tokens_info[1])
            return f"Status Code: {self.statusCode}\nResponse Text: {self.responseText}\nUser Tokens: {self.tokens_string}"
         
         raise Exception("There is no response. Request not sent.")
    
    #Add either App or User Token to DB
    def addOauthToken(self):
        if self.authResponse is not None:
            status_code = self.authResponse.status_code
            if status_code == 200:  
                #.json() converts the response into a Python dictionary
                self.responseJson = self.authResponse.json()
                print(self.responseJson)

                if not self.responseJson.get("access_token"):
                    raise Exception("No access token available")
                
                self.token = self.responseJson["access_token"]
               

                if self.token is not None:

                    self.db = get_db()
                    self.cursor = self.db.cursor()
                    self.user_id = self.cursor.execute(
                        'SELECT user_id FROM user_tokens where user_id = (?)',
                        (g.user['id'],)
                    ).fetchone()
                 
                    if self.user_id is not None:
                        
                        if self.user_id[0] == g.user['id']:
                            self.cursor.execute(
                                'UPDATE user_tokens SET oauth_token = (?), TIMESTAMP = CURRENT_TIMESTAMP WHERE user_id = (?)',
                                (self.token, g.user['id'])
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
                    
                
                    raise Exception("There is no token. Error retrieving information.")
            
            raise Exception("Error with request. Status code: '%s'" % self.authResponse.status_code)
            
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

                        if self.user_id[0] == g.user['id']:
                            
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
            
                
                raise Exception("There is no token. Error retrieving information.")
            
            raise Exception("Error with request.")
        
        raise Exception("There is no response. Request not sent.")

    def getToken(self):
        info_header = self.user_headers
        if info_header is not None:
            return info_header

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
                self.user_headers = {'Authorization': f'Bearer {self.authorization_code}'}
                return
            
            raise Exception("No Oauth Token Found.")
            
        raise Exception("User not found.")

        
            
        

    def getRedirect(self):
        self.redirectUrl = self.authResponse.url
        return self.redirectUrl
    
    def testCall(self, command):
        if command == "app":
            return "Test successful"
        else:
            return "Failure"  