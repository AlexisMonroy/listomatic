import functools
from flask import (
    Blueprint, flash , g, redirect, render_template, request, session, url_for
)

import requests 
from urllib.parse import unquote
from flaskr.db import get_db

class ebayApiCaller(object):
    def __init__(self):
        self.uri = 'https://api.ebay.com/sell/inventory/v1/location/!1993_pochtecha_alexis'

        self.userHeaders = {
            'Authorization': f'Bearer {self.authorization_code}',
            'Consent-Type': 'application/json'
            }

        self.callBody = {
            'location': { 
                'address': 'place'
            },
            'time': {
                'day': 'monday'
            }
        }