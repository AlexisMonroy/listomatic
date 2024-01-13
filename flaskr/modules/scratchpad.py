 if button == "Create Ebay Inventory Location":

                    error = None
                    caller.getToken()
                    auth_response = caller.sendRequest(button)
                    if auth_response.status_code == 200:
                        caller   
                        print(caller)

                        return render_template('calls/callIndex.html', caller=caller)
                    caller
                    return render_template('calls/callIndex.html', caller=caller)
                    
                    
                if button == "Get Ebay Inventory Location":

                    error = None
                    caller.getToken()
                    auth_response = caller.sendRequest(button)
                    if auth_response.status_code == 200:
                        caller   
                        print(caller)

                        return render_template('calls/callIndex.html', caller=caller)
                    caller
                    return render_template('calls/callIndex.html', caller=caller)
                
                if button == "Delete Ebay Inventory Location":

                    error = None
                    
                    auth_response = caller.sendRequest(button)
                    print(auth_response.status_code)
                    print(auth_response.text)

                    return render_template('calls/callIndex.html', caller=auth_response)
                    caller
                    return render_template('calls/callIndex.html', caller=caller)
                
                if button == "Get Fulfillment Policy ID":

                    error = None
                    auth_response = caller.sendRequest(button)
                    if auth_response.status_code == 200:
                        caller   
                        print(caller)


                        return render_template('calls/callIndex.html', caller=caller)
                
                if button == "Get Payment Policy ID":

                    error = None
                    auth_response = caller.sendRequest(button)
                    if auth_response.status_code == 200:
                        caller   
                        print(caller)


                        return render_template('calls/callIndex.html', caller=caller)
                    
                if button == "Get Return Policy ID":

                    error = None
                    auth_response = caller.sendRequest(button)
                    if auth_response.status_code == 200:
                        caller   
                        print(caller)


                        return render_template('calls/callIndex.html', caller=caller)
                
                if button == "Get User Info":

                    error = None
                    caller.getToken()
                    auth_response = caller.sendRequest(button)
                    if auth_response.status_code == 200:
                        caller   
                        print(caller)


                        return render_template('calls/callIndex.html', caller=caller)
                    
                    
                if button == "Get Category Aspects":

                    error = None
                    caller.getToken()
                    auth_response = caller.sendRequest(button)
                    if auth_response.status_code == 200:
                        caller   
                        print(caller)


                        return render_template('calls/callIndex.html', caller=caller)
                    
                    caller
                    return render_template('calls/callIndex.html', caller=caller)
                
                if button == "Get Inventory Record":
                    error = None
                    caller.getToken()
                    auth_response = caller.sendRequest(button)
                    if auth_response.status_code == 200:
                        caller   
                        print(caller)


                        return render_template('calls/callIndex.html', caller=caller)
                    
                    caller
                    return render_template('calls/callIndex.html', caller=caller)
                
                # if button == "Create Inventory Record":

                    #error = None
                    # testInvRecord = caller.createInvRecord("1")
                    #invRecCall = caller.sendRequest(button)
                    # print(invRecCall.status_code)
                    #auth_response = caller.sendRequest(button)
                    #if invRecCall.status_code == 204:
                            
                        #  print(invRecCall.status_code)
                    # else:
                        #  print(invRecCall.text)


                    #  return render_template('calls/callIndex.html', caller=invRecCall.text)
                    
                    
                    #  return render_template('calls/callIndex.html', caller=caller)
                
                if button == "Create Offer":

                    error = None
                    testInvRecord = caller.createOffer("1")
                    createOfferCall = caller.sendRequest(button)
                    print(createOfferCall.status_code)
                    print (createOfferCall.text)
                    #auth_response = caller.sendRequest(button)
                    if createOfferCall.status_code != 200:
                        print('ERROR')
                    return render_template('calls/callIndex.html', caller=createOfferCall.text)
                
                if button == "Publish Offer":

                    error = None
                    publishOfferCall = caller.sendRequest(button)
                    print(publishOfferCall.status_code)
                    print (publishOfferCall.text)
                    #auth_response = caller.sendRequest(button)
                    if publishOfferCall.status_code != 200:
                        print('ERROR')
                    return render_template('calls/callIndex.html', caller=publishOfferCall.text)
                
                if button == "Delete Offer":

                    error = None
                    deleteOfferCall = caller.sendRequest(button)
                    print(deleteOfferCall.status_code)
                    print (deleteOfferCall.text)
                    #auth_response = caller.sendRequest(button)
                    if deleteOfferCall.status_code != 204:
                        print('ERROR')
                    return render_template('calls/callIndex.html', caller=deleteOfferCall.status_code)



_____
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