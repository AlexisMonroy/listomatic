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