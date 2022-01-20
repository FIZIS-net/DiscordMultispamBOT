import time
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

        copied_messages = session.get(f'https://discord.com/api/v9/channels/{ self.id_copied_chat }/messages?limit=100').json()

        for message in copied_messages:
            try:
                msgArr[message["id"]] = {'author_id': message["author"]['id'], 'message_content' : message["content"]}
                messages_ids += 1
            except:
                print('error')
            
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
                msgArr[message["id"]] = {'author_id': message["author"]['id'], 'message_content' : message["content"]}
            except:
                print('error')
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

    def send_message(self,session,msg):
        """send_message
            sends a message through the session you selected
        Args:
            session (obj): the session through which the message is sent
            msg (string): message text

        Returns:
            string : response from the server
        """        
        try:
            _data = {'content':msg, 'tts':False}
            session.post(f'https://discord.com/api/v9/channels/{self.id_insert_chat}/messages', json=_data).json()
            return session.status_code
        except Exception as e:
            return e

