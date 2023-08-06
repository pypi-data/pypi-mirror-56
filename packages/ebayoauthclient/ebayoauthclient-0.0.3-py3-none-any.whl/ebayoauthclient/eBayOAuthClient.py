# -*- coding: utf-8 -*-
"""
Copyright 2019 eBay Inc.
 
Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,

WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and
limitations under the License.
"""

import json
import urllib
import requests
from datetime import datetime, timedelta
import base64
from .model.model import environment


class eBayOAuthClient(object):
    def __init__(self, client_id, client_secret, dev_id, redirect_uri, scopes, env="PRODUCTION"):
        self.client_id = client_id 
        self.dev_id = dev_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scopes = scopes
        self.env_type = getattr(environment, env, None)
        if self.env_type is None:
            raise ValueError('Unkown env: {}'.format(env))

    def _basic_request_headers(self):
        b64_encoded_credential = base64.b64encode((self.client_id + ':' + self.client_secret).encode('utf-8')).decode('utf-8')
        return {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + b64_encoded_credential
        }

    def generate_user_authorization_url(self, state=None):
        '''
            env_type = environment.SANDBOX or environment.PRODUCTION
            scopes = list of strings
        '''
        param = {
                'client_id':self.client_id,
                'redirect_uri':self.redirect_uri,
                'response_type':'code',
                'prompt':'login',
                'scope':' '.join(self.scopes)
                }
        
        if state != None:
            param.update({'state':state})
        
       
        query = urllib.urlencode(param) if hasattr(urllib, 'urlencode') else \
            urllib.parse.urlencode(param)
        return self.env_type.web_endpoint + '?' + query
    

    def get_application_token(self):
        """
            makes call for application token and stores result in credential object
            returns credential object
        """
        headers = self._basic_request_headers()
        body = {
            'grant_type': 'client_credentials',
            'redirect_uri': self.redirect_uri,
            'scope': ' '.join(self.scopes)
        }
        resp = requests.post(self.env_type.api_endpoint, data=body, headers=headers)
        content = json.loads(resp.content)

        if resp.status_code == requests.codes.ok:
            return content
        else:
            raise ValueError('un-expected response ' + str(resp.status_code) + ': ' + content['error_description'])
    

    def exchange_code_for_access_token(self, code):
        headers = self._basic_request_headers()
        body = {
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri,
            'code': code,
        }
        resp = requests.post(self.env_type.api_endpoint, data=body, headers=headers)
        content = json.loads(resp.content)
        
        if resp.status_code == requests.codes.ok:
            return content
        else:
            raise ValueError('un-expected response ' + str(resp.status_code) + ': ' + content['error_description'])
    
    
    def get_access_token(self, refresh_token):
        """
        refresh token call
        """
        headers = self._basic_request_headers()
        if refresh_token == None:
            raise StandardError("credential object does not contain refresh_token and/or scopes")
        body = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'scope': ' '.join(self.scopes)
        }
        resp = requests.post(self.env_type.api_endpoint, data=body, headers=headers)
        content = json.loads(resp.content)

        if resp.status_code == requests.codes.ok:
            return content
        else:
            raise ValueError('un-expected response ' + str(resp.status_code) + ': ' + content['error_description'])
