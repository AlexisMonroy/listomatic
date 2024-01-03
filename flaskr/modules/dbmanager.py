import os
import csv
import functools
from flask import (
    Blueprint, flash , g, redirect, render_template, request, session, url_for
)

import requests 
from urllib.parse import unquote
from flaskr.db import get_db

class DatabaseManager(object):
    def __init__(self):
        self.file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'inventory_files'))
 
    
    #insert into database
    def upload_csv(self, csvfile):
        self.db = get_db()
        self.cursor = self.db.cursor()
        self.error = None
        self.csv_path = self.file_path + '\\' + csvfile
        
        #open and read csv file
        with open(self.csv_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            self.rows = []
            self.quantity = 1
            self.weight_min = 0

            #add each row as a dictionary
            for row in reader:
                modified_row = {header[i]: (int(cell) if cell.isdigit() else cell) for i, cell in enumerate(row)}
                self.rows.append(modified_row)

            #save values and insert into database
            for row in self.rows:
                
                user_id = g.user["id"]
                product_id = row["ID"]
                quantity = self.quantity
                title = row["Title"]
                author = row["Author"]
                price = row["Price"]
                description = row["Description"]
                condition = row["Condition"]
                height = row["Height"]
                width = row["Width"]
                length = row["Length"]
                weight_maj = row["Weight"]
                weight_min = self.weight_min
                pictures = row["Pictures"]
                illustrator = row["Illustrator"]
                genre = row["Genre"]
                publisher = row["Publisher"]
                publication_year = row["Publication Year"]
                self.cursor.execute(
                    '''INSERT into books (user_id, quantity, title, author, price, 
                    description, condition, height, width, length, weight_maj, weight_min, 
                    pictures, illustrator, genre, publisher, publication_year, product_id) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                    (user_id, quantity, title, author, price, description, condition, 
                    height, width, length, weight_maj, weight_min, pictures, illustrator, 
                    genre, publisher, publication_year, product_id)
                    )
                self.db.commit()

            self.cursor.close()
            return self.rows
        
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