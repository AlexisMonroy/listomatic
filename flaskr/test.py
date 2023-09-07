import functools
from flask import (
    Blueprint, flash , g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db
import requests 
from urllib.parse import unquote

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
            'scope': 'https://api.ebay.com/oauth/api_scope'
        }
        #User Consent Request
        self.consentUrl = 'https://auth.ebay.com/oauth2/authorize'

        #dev credentials, RuName 
        self.consentBody = {
            'client_id': 'AlexisGo-pricepre-PRD-3ca7161d2-d3ef5057',
            'redirect_uri': 'Alexis_Gonzalez-AlexisGo-pricep-ufgmqsmji',
            'response_type': 'code',
            'scope': 'https://api.ebay.com/oauth/api_scope',
        }
        self.encoded_string = 'v%5E1.1%23i%5E1%23I%5E3%23f%5E0%23p%5E3%23r%5E1%23t%5EUl41Xzg6RjVDRDIxMThFMzAwQjk4NDg5ODUzMkY0MDU1QUMzMDlfMV8xI0VeMjYw'
        self.decoded_string = unquote(self.encoded_string)

        #print(decoded_url)
        self.userTokenBody = {
                'grant_type': 'authorization_code',
                'code': f'{self.decoded_string}',
                'redirect_uri': 'Alexis_Gonzalez-AlexisGo-pricep-ufgmqsmji'
            }
    #Get DataBase    

    #Specify App or Client Auth Flow
    def sendRequest(self, command):
        if command == "Start Auth Flow":
            self.authResponse = requests.post(self.oauthUrl, headers=self.oauthHeaders, data=self.appTokenBody)
            return self.authResponse
        elif command == "User Sign In":
            self.authResponse = requests.get(self.consentUrl, params=self.consentBody)
            return self.authResponse
        elif command == "Get User Token":
            self.authResponse = requests.post(self.oauthUrl, headers=self.oauthHeaders, data=self.userTokenBody)
            return self.authResponse
    #Return Response Status Code and Text
    def __str__(self):
        self.statusCode = self.authResponse.status_code
        self.responseText = self.authResponse.text
        #self.responseData = self.authResponse.json()
        return f"{self.statusCode}\n{self.responseText}"
    #Add either App or User Token to DB
    def addToken(self):
        self.responseJson = self.authResponse.json()
        if not self.responseJson.get("access_token"):
            raise Exception("No access token available")
        else:
            self.token = self.responseJson["access_token"]
        if not self.responseJson.get("refresh_token"):
            self.db = get_db()
            self.cursor = self.db.cursor()
            self.cursor.execute(
                'UPDATE user_tokens SET user_id = (?), oauth_token = (?)',
                (g.user['id'], self.token)
            )
            self.db.commit()
            self.cursor.close()
        else:
            self.refreshToken = self.responseJson["refresh_token"]
            self.db = get_db()
            self.cursor = self.db.cursor()
            self.cursor.execute(
                'UPDATE user_tokens SET user_token = (?), refresh_token = (?) where user_id = (?)'
                (self.token, self.refreshToken, g.user['id'])
            )
            self.db.commit()
            self.cursor.close()

    def testCall(self, command):
        if command == "app":
            return "Test successful"
        else:
            return "Failure"  
    
ebayCaller = EbayCaller()
command = "Start Auth Flow"
ebayCaller.sendRequest(command)
try:
    test_string = ebayCaller.__str__()
    test_addToken = ebayCaller.addToken()
    print(test_string)
    print(test_addToken)
except Exception as e:
    print("Error", str(e))

