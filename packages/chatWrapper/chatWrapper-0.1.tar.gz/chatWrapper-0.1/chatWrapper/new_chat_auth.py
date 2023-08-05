import webbrowser
import requests
import base64
import six
import six.moves.urllib.parse as urllibparse


class ChatAuthError(Exception):
    pass


class ChatAuth(object):
    """
    SDK for Chat API Authentication 
    Implements Authorization Code Flow for Chat Client OAuth implementation.
    """
    
    OAUTH_AUTHORIZE_URL = 'https://os-chat-api.herokuapp.com/o/authorize'
    OAUTH_TOKEN_URL = 'https://os-chat-api.herokuapp.com/o/token/'

    def __init__(self, client_id, client_secret, redirect_url):
        """
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_url = redirect_url    

    def _make_authorization_headers(self):
        """
        """        
        auth_header = base64.b64encode(six.text_type(self.client_id + ':' + self.client_secret).encode('ascii'))
        return {'Authorization': 'Basic %s' % auth_header.decode('ascii')}

    def _parse_response_code(self, url):
        """ Parse the response code in the given response url
            Parameters:
                - url - the response url
        """
        try:
            return url.split("?code=")[1].split("&")[0]
        except IndexError:
            return None

    def create_auth_credientials(self):
        """
        """
        payload = {
            'client_id': self.client_id,
            'response_type': 'code',
            'state': 'random_state_string',
        }
        urlparams = urllibparse.urlencode(payload)
        new_url = "%s?%s" % (self.OAUTH_AUTHORIZE_URL, urlparams)
        webbrowser.open_new_tab(new_url)
        user_input = input('Enter the url you are redirected to: \n')
        auth_code = self._parse_response_code(user_input)
        return auth_code

    def get_access_token(self, code):
        """ Gets the access token for the app given the code
            Parameters:
                - code - the response code
        """
        payload = {'redirect_uri': self.redirect_url,
                    'code': code,
                    'grant_type': 'authorization_code',
                }

        headers = self._make_authorization_headers()
        response = requests.post(self.OAUTH_TOKEN_URL, data=payload, headers=headers, verify=True)
        if response.status_code != 200:
            raise ChatAuthError(response.json()['error'])
        
        token_info = response.json()
        return token_info

    def refresh_access_token(self, refresh_token):
        """
        """
        payload = {
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }
        headers = self._make_authorization_headers()
        response = requests.post(self.OAUTH_TOKEN_URL, data=payload, headers=headers)
        if response.status_code != 200:
            raise ChatAuthError(response.json()['error'])
        token_info = response.json()
        return token_info




