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
                    'Authorization': 'Bearer v^1.1#i^1#f^0#r^0#p^3#I^3#t^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', 
                    'Content-Language': 'en-US',
                    'Content-Type': 'application/json'
                }
                #pass in categoryId and get callBody
                self.invRecordBody = dbManager.categoryInvCallBody(item["category"], item, item["pictures"])

                try:
                    #send Create Inventory API Call
                    self.invRecordResponse = requests.put(self.invRecordUri, headers=self.invRecordHeaders, json=self.invRecordBody)

                except Exception as e:

                    print("ERROR CREATING INVENTORY RECORD: ", str(e))

                print(self.invRecordResponse.status_code)
                print(self.invRecordResponse.text)
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

                    time = datetime.datetime.now()
                    timeString = str(time)
                    #if offer is published, delete item from pending and insert into posted
                    self.PostedDbResponse = dbManager.insertPostedId(offer["productId"], offer["categoryId"], g.user['id'], timeString)

                    if self.PostedDbResponse == "Successfully Inserted Item into Posted Table":
                        self.deletePendingResponse = dbManager.deletePendingId(offer["productId"])
                        print(self.deletePendingResponse)

                else:
                    print("no id")
            
            return self.publishOfferResponses
            
            

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
        
        if command == "Delete Listing":
            self.offersList = dbManager.getOfferId()
            self.deleteListingResponses = []

            for offerId in self.offersList:
                self.withdrawListingUri = f"https://api.ebay.com/sell/inventory/v1/offer/{offerId['offerId']}/withdraw"

                self.deleteListingHeaders = {
            'Authorization': 'Bearer v^1.1#i^1#f^0#r^0#p^3#I^3#t^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', 
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip'
        }

                try:
                    self.deleteListingResponse = requests.post(self.withdrawListingUri, headers=self.deleteListingHeaders)

                except Exception as e:
                    print("ERROR DELETING LISTING: ", str(e))

                self.deleteListingJson = self.deleteListingResponse.json()
                print(self.deleteListingJson)
                self.listingId = self.deleteListingJson["listingId"]
                self.deleteListingResponses.append(self.listingId)
            
            return self.deleteListingResponses
            
            
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
    
