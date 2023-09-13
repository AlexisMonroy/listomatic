def sendRequest(self, command):
    command_actions = {
        "Start Auth Flow": lambda: requests.post(self.oauthUrl, headers=self.oauthHeaders, data=self.appTokenBody),
        "User Sign In": lambda: requests.get(self.consentUrl, params=self.consentBody),
        "Get User Token": lambda: requests.post(self.oauthUrl, headers=self.oauthHeaders, data=self.userTokenBody)
        "Get User Info"
        uri = 'https://apiz.ebay.com/commerce/identity/v1/user/'
            get_headers = {'Authorization': 'Bearer v^1.1#i^1#f^0#p^3#r^0#I^3#t^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'}

            get_user_response = requests.get(uri, headers=get_headers)   
    }

    action = command_actions.get(command)
    if action:
        self.authResponse = action()
        return self.authResponse

    self.authResponse = None
    return None

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
        self.authResponse = None
        return



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

        command_actions = {
            "Start Auth Flow": lambda: requests.post(self.oauthUrl, headers=self.oauthHeaders, data=self.appTokenBody),
            "User Sign In": lambda: requests.get(self.consentUrl, params=self.consentBody),
            "Get User Token": lambda: requests.post(self.oauthUrl, headers=self.oauthHeaders, data=self.userTokenBody)
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
                
                self.token = self.responseJson["access_token"]

                if self.token is not None:

                    self.db = get_db()
                    self.cursor = self.db.cursor()
                    self.user_id, self.oauth_token = self.cursor.execute(
                        'SELECT user_id, oauth_token FROM user_tokens where user_id = (?) AND oauth_token = (?)',
                        (g.user['id'], self.token)
                    ).fetchone()
                    if self.user_id is not None:

                        if self.user_id == g.user['id']:

                            self.cursor.execute(
                                'UPDATE user_tokens SET user_id = (?), oauth_token = (?) WHERE user_id = (?)',
                                (g.user['id'], self.token, g.user['id'])
                            )

                            self.db.commit()
                            self.cursor.close()
                            return self.oauth_token
                        
                        self.cursor.execute(
                            'INSERT into user_tokens (user_id, oauth_token) VALUES (?, ?)',
                            (g.user['id'], self.token)
                        )
                        self.db.commit()
                        self.cursor.close()
                        return self.oauth_token
                    
                    raise Exception("User information not found.")
                
                raise Exception("There is no token. Error retrieving information.")
            
            raise Exception("Error with request.")
            
        raise Exception("There is no response. Request not sent.")
            
    def addRefreshToken(self):
        if self.authResponse is not None:
            status_code = self.authResponse.status_code
            if status_code == 200:  
                self.token = self.responseJson["access_token"]
                self.refreshToken = self.responseJson["refresh_token"]

                if self.token is not None:

                    self.db = get_db()
                    self.cursor = self.db.cursor()
                    self.user_id, self.user_token_db, self.refresh_token_db = self.cursor.execute(
                        'SELECT user_id, user_token, refresh_token FROM user_tokens where user_id = (?) AND user_token = (?) and refresh_token = (?)',
                        (g.user['id'], self.token, self.refreshToken)
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