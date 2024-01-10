import os
import csv
import functools
import datetime
from flask import (
    Blueprint, flash , g, redirect, render_template, request, session, url_for
)

import requests 
from urllib.parse import unquote
from flaskr.db import get_db

class DatabaseManager(object):
    def __init__(self):
        self.file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'inventory_files'))
 
    def categoryChecker(self, categoryId):
        #BOOKS
        if categoryId == "261186":
            

            self.dbQuery = '''INSERT OR IGNORE into books VALUES (
            ?, ?, ?, ?, ?, ?, ?, 
            ?, ?, ?, ?, ?, ?, ?, 
            ?, ?, ?, ?, ?, ?, ?, 
            ?, ?, ?, ?, ?, ?, ?, 
            ?, ?, ?, ?, ?, ?, ?
            )'''
            
            self.pendingQuery = '''INSERT OR IGNORE into pending VALUES (
            ?, ?, ?, ?
            )'''
            return self.dbQuery, self.pendingQuery
        
        return None
    
    def categoryCallBody(self, categoryId, item):
        if categoryId == 261186:

            productGenres = item["genre"].split(', ')
            self.invRecordBody = {
                
                "availability": {
                    "shipToLocationAvailability": {
                        "quantity": item["quantity"]
                    }
                },
                "condition": "USED_GOOD",
                "packageWeightAndSize": { 
                    "dimensions" : { 
                        "height" : item["height"],
                        "length" : item["length"],
                        "unit" : "INCH",
                        "width" : item["width"]
                    },
                        #"packageType" : "MAILING_BOX",
                        "weight" : { 
                            "unit" : "OUNCE",
                            "value" : item["weight"]
                        }
                },
                "product": {
                    "title": item["title"],
                    "description": item["description"],
                    "aspects": {
                        "Author": [
                            item["author"]
                        ],
                        "Book Title": [
                            item["title"]
                        ],
                        "Language": [
                            "English"
                        ],
                        "Genre": productGenres,
                    # "Illustrator": [
                        # item["illustrator"]
                    # ],
                        "Publisher": [
                            item["publisher"]
                        ],
                        "Publication Year": [
                            item["publicationYear"]
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

        return self.invRecordBody
    #insert into database
    def upload_csv(self, csvfile):

        self.db = get_db()
        self.cursor = self.db.cursor()
        self.error = None
        self.csv_path = self.file_path + csvfile

 
        
        #open and read csv file 
        with open(self.csv_path, newline='') as csvfile:
            try:
                reader = csv.reader(csvfile)
                header = next(reader)
            except Exception as e:
                print("ERROR READING CSV FILE: ", str(e))
                return e    

            self.rows = []
            self.sortedCategories = []
                

        #add each row as a dictionary
            for row in reader:
                modified_row = {header[i]: (int(cell) if cell.isdigit() else cell) for i, cell in enumerate(row)}
                self.rows.append(modified_row)

            #create a list of category numbers for sortedCateories list
            lookup = {list(d.keys())[0]: d for d in self.sortedCategories}

            #sort rows into a sorted list of dictionaries, based on category numbers
            for dict in self.rows:
                key = dict['Category']
                if key in lookup:
                    #print(lookup[key])
                    #print(lookup[key][key])
                    lookup[key][key].append(dict)
                   
                else:
                   
                    lookup[key] = {key: [dict]}
                    self.sortedCategories.append(lookup[key])
            

            userId = {'userId': g.user['id']}

            #ADD userId and convert to list of tuples
            for category in self.sortedCategories:

                #grab category id from sortedCategories
                categoryKey = str(list(category.keys())[0])

                #grab category call info from category checker
                self.uploadCsvQuery, self.insertPendingQuery = self.categoryChecker(categoryKey)

                for lst in category:
                   
                    for item in category[lst]:
                        
                        #add userId
                        item.update(userId)

                        #add time entry    
                        time = datetime.datetime.now()
                        timeString = str(time)
                        timestamp = {'time': timeString}
                        item.update(timestamp)
                        
                        #add Item details to a list
                        itemDetails = []

                        for header in item:                
                            #print(item[header])
                            itemDetails.append(item[header])
                        
                        #print(itemDetails)
                            
                        #CONVERT ITEM DETAILS TO TUPLE AND INSERT INTO DB
                        itemTuple = tuple(itemDetails)
                        pendingTuple = (item["ProductId"], item["Category"], g.user["id"], timeString)
                        
                        
                        try:
                            #INSERT ITEM DETAILS INTO RESPECTIVE TABLE
                            self.cursor.execute(self.uploadCsvQuery, itemTuple)
                            self.db.commit()

                        except Exception as e:

                            print("ERROR UPLOADING TO CATEGORY TABLE: ", str(e))
                            return e
                        
                        try:
                            #INSERT PRODUCTID INTO PENDING
                            self.cursor.execute(self.insertPendingQuery, pendingTuple)
                            self.db.commit()

                        except Exception as e:

                            print("ERROR INSERTING INTO PENDING TABLE: ", str(e))
                            return e
                        
            
            self.cursor.close()
            return self.sortedCategories
        
    def get_item(self, product_id):
        self.db = get_db()
        self.cursor = self.db.cursor()
        #return product info using product_id
        item = self.cursor.execute(
            '''SELECT * from books where product_id = (?)''',
            (product_id)
        ).fetchone()
        #convert into dictionary
        product_dict = dict(item)

        #print(product_dict)

        return product_dict

    def getPendingItems(self):
        self.db = get_db()
        self.cursor = self.db.cursor()
        self.pendingQuery = '''SELECT * FROM pending'''
        self.categoryNameQuery = '''SELECT categoryName from categories where categoryId = ?'''
        

        #get list of pendingId's
        self.pendingItems = self.cursor.execute(self.pendingQuery).fetchall()
        self.pendingItemDetails = []

        for item in self.pendingItems:

            try:

                pendProductId = item["productId"]
                pendCategoryId = item["categoryId"]

                #get category Name 
                categoryNameObject = self.cursor.execute(self.categoryNameQuery, (pendCategoryId,)).fetchone()
                categoryName = categoryNameObject["categoryName"]
                
                #get item details and add to pendItemDetails
                pendingItemDetail = self.cursor.execute(f'''SELECT * FROM {categoryName} WHERE productId = ?''', (pendProductId,)).fetchone()
                self.pendingItemDetails.append(pendingItemDetail)

            except Exception as e:
                print("ERROR GETTING ITEM DETAILS: ", str(e))

        for detailList in self.pendingItemDetails:
            print(detailList["productId"])


        return self.pendingItemDetails
        
    #insert product ids into pending table
    
    #insert product ids into posted if item has been listed
        
    #check whether item has been posted or is pending

    #retrieve row info based on dbTable value passed in