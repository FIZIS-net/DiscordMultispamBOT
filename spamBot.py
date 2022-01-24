import json
import time
from urllib import request, response
import requests as r
from collections import OrderedDict, deque

class spamBot():

    def __init__(self, id_copied_chat, id_insert_chat) -> None:
        self.id_copied_chat = id_copied_chat
        self.id_insert_chat = id_insert_chat

    def get_messages(self, session):
        """get_messages
            gives you a list of recent messages
        Args:
            copied_chat_id (integer): id of the chat from which we will receive messages
        Returns:
            dict : list of messages in order
        """        
        msgArr = {}
        messages_ids=0
        try:
            copied_messages = session.get(f'https://discord.com/api/v9/channels/{ self.id_copied_chat }/messages?limit=100').json()
        except Exception as e:
            print(session.get(f'https://discord.com/api/v9/channels/{ self.id_copied_chat }/messages?limit=100').text)

        for message in copied_messages:
            try:
                msgArr[message["id"]] = {
                    'author_id': message["author"]['id'],
                    'message_content' : message["content"],
                }
                if "referenced_message" in message:
                    msgArr[message["id"]]["message_reference"] = {
                        "channel_id" : self.id_insert_chat,
                        "message_id" : message["referenced_message"]["id"]
                    }
            
                messages_ids += 1
            except:
                print('get_messages ERROR')
                print(message)
            
        return msgArr
    
    def create_session(self, discord_token):
        """create_session

        Args:
            discord_token (string): discord token for authorization

        Returns:
            obj : session
        """        
        session = r.session()
        session.headers['authorization'] = discord_token
        session.headers['accept'] = "*/*"
        session.headers["connection"]=  "keep-alive"
        # session.headers["accept-encoding"] = "br"
        session.headers["accept-language"] = "en-GB"
        session.headers["content-type"] = "application/json"
        session.headers["X-Debug-Options"] = "bugReporterEnabled"
        session.headers["cache-control"] = "no-cache"
        session.headers["sec-ch-ua"] = "'Chromium';v='92', ' Not A;Brand';v='99', 'Google Chrome';v='92'"
        session.headers["sec-fetch-site"] = "same-origin"
        session.headers["x-context-properties"] = "eyJsb2NhdGlvbiI6IkpvaW4gR3VpbGQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6Ijg4NTkwNzE3MjMwNTgwOTUxOSIsImxvY2F0aW9uX2NoYW5uZWxfaWQiOiI4ODU5MDcxNzIzMDU4MDk1MjUiLCJsb2NhdGlvbl9jaGFubmVsX3R5cGUiOjB9"
        session.headers["x-fingerprint"] = self.get_fingerprint()
        session.headers["x-super-properties"] = "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjkzLjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvOTMuMCIsImJyb3dzZXJfdmVyc2lvbiI6IjkzLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTAwODA0LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
        session.headers["sec-fetch-dest"] = "empty"
        session.headers["sec-fetch-mode"] = "cors"
        session.headers["sec-fetch-site"] = "same-origin"
        session.headers["origin"] = "https://discord.com"
        session.headers["referer"] = "https://discord.com/channels/@me"
        session.headers["user-agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.16 Chrome/91.0.4472.164 Electron/13.4.0 Safari/537.36"
        session.headers["te"] =  "trailers"
        return session

    def get_messages_before(self, session, last_message_id):
        """get_messages_before
            receiving messages after a certain
        Args:
            copied_chat_id (integer): id of the chat from which we are copying
            last_message_id (integer): id of the message after which we receive

        Returns:
            dict: list of messages in order
        """        
        copied_messages = session.get(f'https://discord.com/api/v9/channels/{ self.id_copied_chat }/messages?before={last_message_id}&limit=100').json()
        msgArr = {}
        for message in copied_messages:
            try:
                msgArr[message["id"]] = {
                    'author_id': message["author"]['id'],
                    'message_content' : message["content"]
                    }
                if "referenced_message" in message and message["referenced_message"] != None:
                    msgArr[message["id"]]["message_reference"] = {
                    "channel_id" : self.id_insert_chat,
                    "message_id" : message["referenced_message"]["id"]
                }
                elif "message_reference" in message and message["message_reference"] != None:
                    msgArr[message["id"]]["message_reference"] = {
                    "channel_id" : self.id_insert_chat,
                    "message_id" : message["message_reference"]["message_id"]
                }
                    
            except:
                print(f'get_messages_before ERROR')
        return msgArr

    def reverseDict(self, dict):
        dict = OrderedDict(reversed(dict.items()))
        return dict

    def get_last_messages_id(self,dictMessages):
        """get_last_messages_id

        Args:
            dict (dictMessages): dictionary of messages

        Returns:
            integer : id of the last message in the dictionary
        """        
        [last_id] = deque(dictMessages, maxlen=1)
        return last_id

    def get_first_messages_id(self,dictMessages):
        """get_first_messages_id

        Args:
            dictMessages (dict): dictionary of messages

        Returns:
            int : id of the last message
        """        
        keys = list(dictMessages.keys())
        return keys[0]

    def send_message(self,session,msg,sent_msg):
        """send_message
            sends a message through the session you selected
        Args:
            session (obj): the session through which the message is sent
            msg (string): message text

        Returns:
            string : response from the server
        """        
        try:
            text = msg["message_content"]
            if "message_reference" in msg and msg['message_reference']['message_id'] in sent_msg:
                _data = {
                    'content': text,
                    "message_reference": {
                        "channel_id": msg['message_reference']['channel_id'],
                        "message_id": sent_msg[msg['message_reference']['message_id']]["msg_id"]
                    },
                    'tts':False}
            else:
                _data = {'content':text, 'tts':False}
            req = session.post(f'https://discord.com/api/v9/channels/{self.id_insert_chat}/messages', json=_data).json()
            return req
        except Exception as e:
            print(e)
            return e

    def send_typing(self, session):
        response = session.post(f'https://discord.com/api/v9/channels/{self.id_insert_chat}/typing')
        return response

    def get_cookie(self):
        resp = r.get(f"https://discord.com")
        CookieDict = {}
        for cookie in resp.cookies:
            if cookie.name == "__dcfduid":
                CookieDict["Dcfduid"] = cookie.value
            if cookie.name == "__sdcfduid":
                CookieDict["Sdcfduid"] = cookie.value
        return CookieDict

    def send_join(self, session, inviteCode):
        url = "https://discord.com/api/v9/invites/" + inviteCode
        Cookie = self.get_cookie()
        if Cookie["Dcfduid"] == "" and Cookie["Sdcfduid"] == "":
            print("Error: Cookie is empty")
            return
        Cookies = "__dcfduid=" + Cookie["Dcfduid"] + "; " + "__sdcfduid=" + Cookie["Sdcfduid"] + "; " + "locale=ru"
        session.headers["cookie"] = Cookies
        req = session.post(url , data="{}")
        return req

    def get_fingerprint(self):
        resp = r.get(f"https://discordapp.com/api/v9/experiments")
        resp = json.loads(resp.text)
        resp = resp["fingerprint"]
        return resp
