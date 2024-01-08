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
        if categoryId == "261186" or "461186" or "561186":
            

            self.dbQuery = '''INSERT OR IGNORE into newbooks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            
            return self.dbQuery
        
        return None
    
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
                self.query = self.categoryChecker(categoryKey)

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
                        #print(itemTuple)
                        try:
                            self.cursor.execute(self.query, itemTuple)
                            self.db.commit()
                        except Exception as e:
                            print("ERROR UPLOADING TO DATABASE: ", str(e))
                            return e
                        #print(itemTuple)
            
            self.cursor.close()
            return self.sortedCategories
        
    def get_product_info(self, product_id):
        self.db = get_db()
        self.cursor = self.db.cursor()
        #return product info using product_id
        product_info = self.cursor.execute(
            '''SELECT * from books where product_id = (?)''',
            (product_id)
        ).fetchone()
        #convert into dictionary
        product_dict = dict(product_info)

        #print(product_dict)

        return product_dict

        
    #insert product ids into pending table
    
    #insert product ids into posted if item has been listed
        
    #check whether item has been posted or is pending

    #retrieve row info based on dbTable value passed in