import functools
import datetime
from flask import (
    Blueprint, flash , g, redirect, render_template, request, session, url_for
)

import requests 
from urllib.parse import unquote
from flaskr.db import get_db
from flaskr.modules.dbmanager import DatabaseManager

class ebayApiCaller(object):
    #will follow the structure of sendCommand function in ebayAuthorization
    def __init__(self):
        self.uri = 'https://api.ebay.com/sell/inventory/v1/location/1993_twt_pochteca_alexis'
        self.deleteInvLocUri = "https://api.ebay.com/sell/inventory/v1/location/1993_pochtecha_alexis"

        self.info_uri = 'https://apiz.ebay.com/commerce/identity/v1/user/'
        self.aspects_uri = 'https://api.ebay.com/commerce/taxonomy/v1/category_tree/0/get_item_aspects_for_category?category_id=261186'
        self.getItemuri = "https://api.ebay.com/sell/inventory/v1/inventory_item/1"

        self.pubOfferUri = "https://api.ebay.com/sell/inventory/v1/offer/391071490016/publish/"
        self.delOfferUri = "https://api.ebay.com/sell/inventory/v1/offer/391071490016"

        self.getFulfillmentIduri = "https://api.ebay.com/sell/account/v1/fulfillment_policy?marketplace_id=EBAY_US"
        self.fId = "226779583024"

        self.getPaymentIduri = "https://api.ebay.com/sell/account/v1/payment_policy?marketplace_id=EBAY_US"
        self.pId = "226779859024"

        self.getReturnId = "https://api.ebay.com/sell/account/v1/return_policy?marketplace_id=EBAY_US"
        self.rId = "226779866024"

        self.aspects_headers = {
            'Authorization': 'Bearer v^1.1#i^1#f^0#r^0#I^3#p^3#t^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', 
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip'
        }

        

        self.user_headers = None

        self.callBody = {

            'location': { 
                'address': {
                    'addressLine1': '14915 1/2 Condon Avenue',
                    'city': 'Lawndale',
                    'country': 'US',
                    "postalCode": "90260"
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


    def getCommand(self, command):
        dbManager = DatabaseManager()
        if command == "Create Inventory Record":
            #get item details for call body from Database 
            self.itemDetailsList = dbManager.getPendingItems()
            self.invRecordResponses = []

            for item in self.itemDetailsList:

                self.productSku = item["productId"]
                self.invRecordUri = f"https://api.ebay.com/sell/inventory/v1/inventory_item/{self.productSku}"
                self.invRecordHeaders = {
            'Authorization': 'v^1.1#i^1#f^0#r^0#p^3#I^3#t^H4sIAAAAAAAAAOVZe2wcxRm/s52khiQUJQppVKrjHBAi2rvZvd3bR31Xzr5zfAmO7VvnURdkze3O3k28t7vZnfXlnNJabhuKVJRKhLSAkCKUPyqQEH8ArQqqStVi6COC0gIBNWpRKeWVVk0KpQpqZ8+POK7yaNdSTur9c9pvvpn5fr/vMS8wtbLzloP9Bz9aE13VdnQKTLVFo+zVoHPlii1r29s2rYiARQrRo1Obpzqm2//c7cGa6Sgl5Dm25aHY/pppeUpTmIn7rqXY0MOeYsEa8hSiKWpu4DaFSwDFcW1ia7YZjxXzmXiZk6Aos5omCZIssYhKrfkxR+xMHHGckOYB5GQZshyXou2e56Oi5RFokUycAxzPAJZhUyNAUARWAXJCFIXReGwXcj1sW1QlAeLZprlKs6+7yNaLmwo9D7mEDhLPFnN96mCumC/sGOlOLhorO8eDSiDxvfO/em0dxXZB00cXn8Zraiuqr2nI8+LJ7OwM5w+q5OaN+R/Mb1LNy0gztBQv6jBF+YbLQmWf7dYgubgdgQTrjNFUVZBFMGlcilHKRnkv0sjc1w46RDEfC/6GfWhiAyM3Ey/05L64Uy2U4jF1aMi1J7CO9AApx/EcK/GcxMezpIrq0NKRi60KwdDa5+NJYuK5KWfHnSN8yZy9tqXjgD4vtsMmPYjaj5ayxC9iiSoNWoNuziCBbYv1xAU2udHAvbP+9EnVCjyMapSSWPPz0r6YD45z4bBs4SEagsAZgqbJMIW0+UwLcj1UiGQDL+WGhpKBLagMG0wNuuOIOCbUEKNRev0a9Y6upASDS0kGYvS0bDC8bBhMWdDTDGsgBBAqlzVZ+v+MFEJcXPYJWoiWpQ1NuJm4qtkOGrJNrDXiS1WadWguNvZ7mXiVEEdJJuv1eqKeSthuJckBwCb3DNymalVUo9VhXhdfWpnBzQjRaPmm+gppONSa/TQISUBmPJty9SHokoaKTJMK5kP4PNuyS6UXANlrYsrACJ2itTD22x5BeihoOprAGhrD+hVCFuT6BdBxbJqXRCklAgDkUCBNu4KtAUSq9pWCeQGIQX0o5kNho+UUktZCtVBduBGOm69CrMjQUgNAKLA5xynWaj6BZRMVW8yXvCikBSEUPMf3r1giXgCVb0qm78G622iEghaswkGuKxgaCrHHkdV65bRU6CsV1P6xkcHthR2h0JaQ4SKvOhLgbLU4zQ3ntuXob2C7pvZXd28n24b3lTEpm5W9xfK2PUUbOXVhUpasHjxa2OrzJtfvWoLGVft1C6Z7+PLwVnZiV19Kq2cyoUhSkeaiFitdpWFndG+e69tijo6rTt1K7t434Yq86NtVtq9352gFNjyc3rNFGpbCgR+otFqmL99yG4R9kOstmOLubGKONSvQGP0KBbRQabl6DbiULmg8YiUJQKBrogh1xBlpw0AGECUu9PLbYnhzJtqPva0247h0H+u4iBkq5ZmUBkU2zeoco6eQIQBBDLkut5qbl2tZ9oLjW1hoQa4vL7ygv0cHgA5OBDuHhGbXkjb0STUQjTWtjl2OUpLK6FFfQwl6/G7eAiVcBHXbMhuX19+jx8cEtiZoZ9v9b/pATbN9i4Tb2yMdu/TMP+a7uLXibzbtxrba1iQ00SSzJA0Z36jU9nm1vTgU/oDXVjy2DeVUdfdgKdzBLY8mWq2Y6hBJssCLDC+VJYbX+DIjI0FkkIRkKPECJ+od09HucDcOLXdcZUUgsJwA2Mve9SwRLLoj+4+L0uT5bxbZSPPHTkd/AqajP2qLRkE3uJHtAjesbN/Z0b56k4cJrVXQSHi4YkHiuygxjhoOxG7busjfHr6vv3dTYfDILQdGGi8+OBNZvejJ5OgdYOPCo0lnO3v1ohcU8NlzLSvYa65bw/GAZVNAEFggj4Kuc60d7IaO9e9v+PLpX4wfecd874NfHfj78NfPfu3JY2DNglI0uiJC4yAS+fbTHZ2fYzd3vv6nyFvdT83ozs0f/PNarG4zb13buP3na0qrjn8GrX8dnR3YctPMq6cSHV2vfu/Eavm5E+8lH/jqvXe+8dtEe3Fz4a6e2IaHHj321D9KnzplSdfsye/OHO5aPbNq59vfPNh38sAbG3+p3/3rOyMv3f/uy6cOHj7z2JkXXnjk2fd/+sq3bjz9u4F0/a4feP2HIte/GfEefHpA+Y10+JWJjnsOCbW/ZJ744d3Z29c9Gy3Z+eObzn4af/eeP761/sOrPur7zoeP7wL1Q1/a8Nrkc9c9Y719/R0nbz3+V+7Hnxy5/8QNP/v88xuv+v7Hv3/m5ZemMw98cvrjb3xhZu3mF9Wb/hV9s/fMw394resr8PljD50cX9c268t/Awk5abTMGgAA', 
            'Content-Language': 'en-US',
            'Content-Type': 'application/json'
        }
                #pass in categoryId and get callBody
                self.invRecordBody = dbManager.categoryInvCallBody(item["category"], item)

                try:
                    #send Create Inventory API Call
                    self.invRecordResponse = requests.put(self.invRecordUri, headers=self.invRecordHeaders, json=self.invRecordBody)

                except Exception as e:

                    print("ERROR CREATING INVENTORY RECORD: ", str(e))

                print(self.invRecordResponse.status_code)
                self.invRecordResponses.append(self.invRecordResponse.status_code)

            return self.itemDetailsList
        
        if command == "Create Offer":
            self.itemDetailsList = dbManager.getPendingItems()
            self.createOfferResponses = []

            for item in self.itemDetailsList:

                self.createOfferUri = "https://api.ebay.com/sell/inventory/v1/offer"
        
                self.createOfferHeaders = {
                    'Authorization': 'Bearer v^1.1#i^1#f^0#r^0#p^3#I^3#t^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', 
                    'Content-Language': 'en-US',
                    'Content-Type': 'application/json'
                }

                self.createOfferBody = dbManager.categoryCreateOfferBody(item["category"], item, self.fId, self.pId, self.rId)

                try:
                    self.createOfferResponse = requests.post(self.createOfferUri, headers=self.createOfferHeaders, json=self.createOfferBody)

                except Exception as e:
                    print("ERROR CREATING OFFER: ", str(e))
                
                  
                self.createOfferJson = self.createOfferResponse.json()
                self.offerId = self.createOfferJson["offerId"]

                time = datetime.datetime.now()
                timeString = str(time)

                #INSERT OFFER ID INTO DB
                self.insertQueryResponse = dbManager.insertOfferId(self.offerId, item["productId"], item["category"], timeString)

                print(self.insertQueryResponse)
                print(self.createOfferJson)
                self.createOfferResponses.append(self.offerId)
            
            return self.createOfferResponses
        
        if command == "Publish Offer":

            #get list of offer ids
            self.offersList = dbManager.getOfferId()
            self.publishOfferResponses = []
            #use productId to check if item is pending
            for offer in self.offersList:
                print(offer["productId"])
                self.productId = dbManager.getPendingId(offer["productId"])

                #if item is pending, send publish offer request
                if self.productId is not None:
                    print("got id")
                    self.publishOfferUri = f"https://api.ebay.com/sell/inventory/v1/offer/{offer['offerId']}/publish/"
                    
                    self.publishOfferHeaders = {
            'Authorization': 'Bearer v^1.1#i^1#f^0#r^0#p^3#I^3#t^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', 
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip'
        }
                    try:
                        self.publishOfferResponse = requests.post(self.publishOfferUri, headers=self.publishOfferHeaders)
                    except Exception as e:
                        print("ERROR PUBLISHING OFFER ID: ", str(e))
                    
                    self.publishOfferJson = self.publishOfferResponse.json()
                    print(self.publishOfferJson)
                    self.listingId = self.publishOfferJson["listingId"]
                    self.publishOfferResponses.append(self.listingId)

                else:
                    print("no id")
            
            return self.publishOfferResponses
            
            #if offer is published, delete item from pending and insert into posted

        if command == "Delete Offer":
            self.offersList = dbManager.getOfferId()
            self.deleteOfferResponses = []
            
            for offerId in self.offersList:
                self.deleteOfferUri = f"https://api.ebay.com/sell/inventory/v1/offer/{offerId['offerId']}"

                self.deleteOfferHeaders = {
            'Authorization': 'Bearer v^1.1#i^1#f^0#r^0#p^3#I^3#t^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', 
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip'
        }
                try:
                    self.deleteOfferIdResponse = requests.delete(self.deleteOfferUri, headers = self.deleteOfferHeaders)

                except Exception as e:
                    print("ERROR DELETING OFFERS: ", str(e))

                dbManager.deleteOfferId(offerId["offerId"])
                self.deleteOfferResponses.append(self.deleteOfferIdResponse.status_code)

            return self.deleteOfferResponses

            
            
    def sendRequest(self, command):

        command_actions = {
            "Create Ebay Inventory Location": lambda: requests.post(self.uri, headers=self.user_headers, json=self.callBody),
            "Get Ebay Inventory Location": lambda: requests.get(self.uri, headers=self.aspects_headers),
            "Delete Ebay Inventory Location": lambda: requests.get(self.deleteInvLocUri, headers=self.aspects_headers),
            "Get Fulfillment Policy ID": lambda: requests.get(self.getFulfillmentIduri, headers=self.aspects_headers),
            "Get Payment Policy ID": lambda: requests.get(self.getPaymentIduri, headers=self.aspects_headers),
            "Get Return Policy ID": lambda: requests.get(self.getReturnId, headers=self.aspects_headers),
            "Get User Info": lambda: requests.get(self.info_uri, headers=self.user_headers),
            "Get Category Aspects": lambda: requests.get(self.aspects_uri, headers=self.aspects_headers),
            "Get Inventory Record": lambda: requests.get(self.getItemuri, headers=self.aspects_headers),
    
            "Create Inventory Record": lambda: requests.put(self.inv_record_uri, headers=self.invRecordHeaders, json=self.invRecordBody),
            "Create Offer": lambda: requests.post(self.createOfferUri, headers=self.createOfferHeaders, json=self.createOfferBody),
            "Publish Offer": lambda: requests.post(self.publishOfferUri, headers=self.aspects_headers),
            "Delete Offer": lambda: requests.delete(self.deleteOfferUri, headers=self.aspects_headers),
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
    
