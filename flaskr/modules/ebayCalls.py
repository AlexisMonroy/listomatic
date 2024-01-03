import functools
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

        self.publishOfferUri = "https://api.ebay.com/sell/inventory/v1/offer/391071490016/publish/"
        self.deleteOfferUri = "https://api.ebay.com/sell/inventory/v1/offer/391071490016"

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

    def createInvRecord(self, product_id):
        #make call to DB manager and get product info from DB
        db_manager = DatabaseManager()
        product_info = db_manager.get_product_info(product_id)
        #grab product_id from return value and use value for sku
        product_sku = product_info["product_id"]

        self.inv_record_uri = f"https://api.ebay.com/sell/inventory/v1/inventory_item/{product_sku}"

        self.invRecordHeaders = {
            'Authorization': 'Bearer v^1.1#i^1#f^0#r^0#I^3#p^3#t^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', 
            'Content-Language': 'en-US',
            'Content-Type': 'application/json'
        }
        #WRITE GUARD RAIL TO CHECK FOR DICT CONDITION VALUE AND SET THE APPROPRIATE VALUE, FOR NOW JUST USING "USED_GOOD" FOR ALL
        productGenres = product_info["genre"].split(', ')
        self.invRecordBody = {
            
            "availability": {
                "shipToLocationAvailability": {
                    "quantity": product_info["quantity"]
                }
            },
            "condition": "USED_GOOD",
            "packageWeightAndSize": { 
                "dimensions" : { 
                    "height" : product_info["height"],
                    "length" : product_info["length"],
                    "unit" : "INCH",
                    "width" : product_info["width"]
                },
                    #"packageType" : "MAILING_BOX",
                    "weight" : { 
                        "unit" : "OUNCE",
                        "value" : product_info["weight_maj"]
                    }
            },
            "product": {
                "title": product_info["title"],
                "description": product_info["description"],
                "aspects": {
                    "Author": [
                        product_info["author"]
                    ],
                    "Book Title": [
                        product_info["title"]
                    ],
                    "Language": [
                        "English"
                    ],
                    "Genre": productGenres,
                   # "Illustrator": [
                       # product_info["illustrator"]
                   # ],
                    "Publisher": [
                        product_info["publisher"]
                    ],
                    "Publication Year": [
                        product_info["publication_year"]
                    ]
                },
                "imageUrls": [
                    "https://alexismonroy.github.io/images/AgeofEnlightmentGreatAgesofMan/AgeofEnlightmentGreatAgesofMan0.jpg",
                    "https://alexismonroy.github.io/images/AgeofEnlightmentGreatAgesofMan/AgeofEnlightmentGreatAgesofMan1.jpg",
                    "https://alexismonroy.github.io/images/AgeofEnlightmentGreatAgesofMan/AgeofEnlightmentGreatAgesofMan2.jpg",
                    "https://alexismonroy.github.io/images/AgeofEnlightmentGreatAgesofMan/AgeofEnlightmentGreatAgesofMan3.jpg"
                ]

            }

        }
        return product_info

    def createOffer(self, product_id):
        db_manager = DatabaseManager()
        product_info = db_manager.get_product_info(product_id)
        #grab product_id from return value and use value for sku
        product_sku = str(product_info["product_id"])
        self.createOfferUri = "https://api.ebay.com/sell/inventory/v1/offer"
        
        self.createOfferHeaders = {
            'Authorization': 'Bearer v^1.1#i^1#f^0#r^0#I^3#p^3#t^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', 
            'Content-Language': 'en-US',
            'Content-Type': 'application/json'
        }

        self.createOfferBody = {
            "sku": product_sku,
            "categoryId": "261186",
            "format": "FIXED_PRICE",
            "listingDescription": product_info["description"],
            "listingDuration": "GTC",
            "listingPolicies": {
                "fulfillmentPolicyId": self.fId,
                "paymentPolicyId": self.pId,
                "returnPolicyId": self.rId,
            },
            "listingStartDate": "2024-01-05T07:00:00Z",
            "marketplaceId": "EBAY_US",
            "merchantLocationKey": "1993_twt_pochteca_alexis",
            "pricingSummary": {
                "price": {
                    "currency": "USD",
                    "value": str(product_info["price"])
                }
            }
        }
        return product_info

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