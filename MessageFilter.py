import json
from telethon import types
class MessageFilter:
    def __init__(self):
        self.source_id = set()
        self.des_id = set()
        self.Bot = None
        config_data = None
        with open('./config.json','r+') as  config:
            data = ''
            for line in config:
                data += line.replace('\n','')
            config_data = json.loads(data)
        if 'source' in config_data:
            for item in config_data['source']:
                self.addSource(int(item))
        if "destination" in config_data:
            for item in config_data['destination']:
                self.addDes(int(item))
    async def notify(self,event):
        peerid = event.message.peer_id
        id = 0
        if isinstance(peerid,types.PeerUser):
            id = peerid.user_id
        elif isinstance(peerid,types.PeerChat):
            id = peerid.chat_id
        elif isinstance(peerid,types.PeerChannel):
            id = peerid.channel_id
        if id in self.source_id:
            for des_id in self.des_id:
                await self.Bot.client.forward_messages(des_id,event.message.id,id)
    def addSource(self,id):
        if id not in self.source_id:
            self.source_id.add(id)
    def addDes(self,id):
        if id not in self.des_id:
            self.des_id.add(id)
    def isLegal(self):
        if len(self.source_id) < 1 or len(self.des_id) < 1 :
            print('please set source and des in config.json')
            return False
        return True