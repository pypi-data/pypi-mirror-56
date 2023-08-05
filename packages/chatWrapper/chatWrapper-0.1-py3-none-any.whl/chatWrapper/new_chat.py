import requests
import base64
import six
import six.moves.urllib.parse as urllibparse

from . import new_chat_auth


class ChatClientException(Exception):
    def __init__(self, http_status, msg):
        self.http_status = http_status
        self.msg = None
        if 'message' in msg:
            self.msg = msg['message']  
        else:
            self.msg = msg
        
    def __str__(self):
        return 'HTTP Status: {0}, Message: {1}'.format(
            self.http_status, self.msg)


class AuthenticationException(Exception):
    
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return self.msg


class ExpiryException(Exception):
    pass


class ChatClient(object):
    """
    Python Wrapper for Chat API
    """    
    def __init__(self, access_token, refresh_token):
        """
        """
        self.main_api_url = 'https://os-chat-api.herokuapp.com/api/'
        self.access_token = access_token
        self.refresh_token = refresh_token
        self._client_id = None
        self._client_secret = None
        self._redirect_uris = None
        self._application_id = None
        self.application_name = None        
        self._is_token_expired()
        self._check_if_token_valid()
        self._get_corresponding_application()

    def _is_token_expired(self):
        """
        Check if token is expired, if so, tell user so they can refresh the token and save it accordingly
        """
        ep = self.main_api_url + 'check_expiry'
        response = self._get(ep)
        expired = response.json()
        if expired['message'] is not False:
            raise AuthenticationException('expired token.')            

    def _check_if_token_valid(self):
        ep = self.main_api_url + 'check_token'
        response = self._get(ep)  # the _get will raise exception if not valid
        return True

    def _get_corresponding_application(self):
        ep = self.main_api_url + 'oauth_application'
        response = self._get(ep)    
        data = response.json()
        self._client_id, self._client_secret, self._redirect_uris = data['client_id'], data['client_secret'], data['redirect_uris']
        self._application_id, self.application_name = data['id'], data['name']
        
    def refresh_access_token(self):
        chatAuth = new_chat_auth.ChatAuth(self._client_id, self._client_secret, self._redirect_uris)
        token_information = chatAuth.refresh_access_token(self.refresh_token)
        return token_information
    
    def _make_authorization_headers(self):
        """
        """
        user_access_token = self.access_token
        return {'Authorization': 'Bearer %s' % user_access_token}

    def _get(self, url, params=None):
        headers = self._make_authorization_headers()
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 403:
            raise AuthenticationException('Authentication Error.')
        elif response.status_code == 200:
            return response
        else:
            msg = response.json()
            raise ChatClientException(response.status_code, msg)                                

    def _post(self, url, data=None):
        response = None
        headers = self._make_authorization_headers()
        
        if data is not None:
            response = requests.post(url, headers=headers, data=data)
        else:
            response = requests.post(url, headers=headers)
        
        if response.status_code == 200 or response.status_code == 201:
            return response        
        
        else:
            msg = response.json()
            raise ChatClientException(response.status_code, msg)
        
        return response

    def _put(self, url, params=None):
        response = None
        headers = self._make_authorization_headers()
        
        response = requests.put(url, headers=headers, params=params)
       
        if response.status_code != 200:
            msg = response.json()
            raise ChatClientException(response.status_code, msg)
        return response

    def _delete(self, url, params=None):
        response = None
        headers = self._make_authorization_headers()
        response = requests.delete(url, headers=headers, params=params)

        if response.status_code != 204:
            msg = response.json()
            raise ChatClientException(response.status_code, msg)

    def create_channel(self):
        """
        """
        url = self.main_api_url + 'channels'
        response = self._post(url)
        data = response.json()
        return data
    
    def delete_channel(self, channel_uuid):
        """
        """        
        url = self.main_api_url + 'channels'
        self._delete(url, params={'channel_id': channel_uuid})

    def create_user(self, username=None):
        """
        """
        url = self.main_api_url + 'chat_users'
        if username != None:
            response = self._post(url, data={
                'username': username
            })
            data = response.json()
            return data
        else:
            response = self._post(url)
            data = response.json()
            return data

    def get_all_chat_users(self, user_id=None):
        """
        """
        url = self.main_api_url + 'chat_users'
        if user_id is not None:
            response = self._get(url, params={'user_id': user_id})
            data = response.json()
            return data
        else:
            response = self._get(url)
            data = response.json()
            return data

    def add_member_to_channel(self, channel_uuid, user_uuid):
        """
        """
        url = self.main_api_url + 'chat_members'
        response = self._post(url, data={
                'channel_id': channel_uuid,
                'user_id': user_uuid,
            })
        data = response.json()
        return data

    def get_channel(self, channel_uuid=None):
        """
        Returns all channel objects associated with Client Application or 
        a particular channel object specified by channel_uuid param
        """       
        url = self.main_api_url + 'channels' 
        if channel_uuid is not None:
            response = self._get(url, params={'channel_id': channel_uuid})
            data = response.json()
            return data
        else:
            response = self._get(url)
            data = response.json()
            return data
            
    def get_all_members_from_channel(self, channel_uuid):
        """
        """
        url = self.main_api_url + 'chat_members'
        response = self._get(url, params={'channel_id': channel_uuid})
        data = response.json()
        return data

    def get_messages_from_channel(self, channel_uuid):
        """
        """
        url = self.main_api_url + 'chat_messages'
        response = self._get(url, params={'channel_id': channel_uuid})
        data = response.json()
        return data

    def generate_token_for_chat(self, channel_uuid, user_uuid):
        """
        """
        url = self.main_api_url + 'generate_token'
        response = self._post(url, data={
            'channel_id': channel_uuid, 
            'user_id': user_uuid
        })
        data = response.json()
        return data

    def get_online_users(self, channel_uuid=None):
        """
        returns all online users registered for application
        """
        url = self.main_api_url + 'user_connected'
        if channel_uuid is not None:
            response = self._get(url, params={'channel_id': channel_uuid})
            data = response.json()
            return data        
        else:
            response = self._get(url)
            data = response.json()
            return data        

    def get_user_notifications(self, user_id=None):
        """
        """
        url = self.main_api_url + 'notifications'
        if user_id is not None:
            response = self._get(url, params={'user_id': user_id})
            data = response.json()
            return data            
        else:
            response = self._get(url)
            data = response.json()
            return data        
        
    def update_user_notification(self, user_uuid):
        """
        """
        url = self.main_api_url + 'notifications'
        self._put(url, params={'user_id': user_uuid})
        

