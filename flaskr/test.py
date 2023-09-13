import functools
from flask import (
    Blueprint, flash , g, redirect, render_template, request, session, url_for
)

import requests 
from urllib.parse import unquote

caller = caller.addRefreshToken()
    
ebayCaller = EbayCaller()
command = "Start Auth Flow"
ebayCaller.sendRequest(command)
try:
    test_string = ebayCaller.__str__()
    init_auth = ebayCaller.sendRequest("Start Auth Flow")
    print(ebayCaller)
except Exception as e:
    print("Error", str(e))

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