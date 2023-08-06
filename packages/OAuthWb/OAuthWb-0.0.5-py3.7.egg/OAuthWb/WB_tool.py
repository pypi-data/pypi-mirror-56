import requests
import json


class OAuthWB:
    def __init__(self, client_id, client_key, redirect_uri):
        self.client_id = client_id
        self.client_key = client_key
        self.redirect_uri = redirect_uri

    # 获取用户token和uid
    def get_access_token(self, code):
        url = "https://api.weibo.com/oauth2/access_token"

        params = {
            "client_id": self.client_id,
            "client_secret": self.client_key,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri
        }

        response = requests.post(url, params=params)

        return json.loads(response.text)

    # 查看token状态
    def get_show_user(self, access_token):
        url = 'https://api.weibo.com/oauth2/get_token_info'

        params = {'access_token': access_token}

        response = requests.get(url, params)

        return json.loads(response.text)

    # 清除token信息
    def get_del_token(self, access_token):
        url = 'https://api.weibo.com/oauth2/revokeoauth2'

        params = {'access_token': access_token}

        response = requests.get(url, params)

        return json.loads(response.text)

    # 返回用户信息
    def get_user_info(self, access_token_data):
        url = "https://api.weibo.com/2/users/show.json"

        params = {
            "uid": access_token_data['uid'],
            "access_token": access_token_data['access_token']
            }

        response = requests.request("GET", url, params=params)

        return json.loads(response.text)
