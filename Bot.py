from telethon import TelegramClient,types,utils,functions,events
import json
import asyncio
from GroupSpider import GroupSpider
class Bot:
    def __init__(self):
        self.API_ID = ''
        self.API_HASH = ''
        self.client = None
        self.messagefilter = None
        self.group_spider = None
        config_data = None
        with open('./config.json','r+') as  config:
            data = ''
            for line in config:
                data += line.replace('\n','')
            config_data = json.loads(data)
        if 'API_ID' in config_data:
            self.API_ID = config_data['API_ID']
        if 'API_HASH' in config_data:
            self.API_HASH = config_data['API_HASH']
    def isLegal(self):
        if self.API_ID == '' or self.API_HASH == '':
            print('please set api_id and api_hash in config.json')
            return False
        return True
    async def login(self):
        self.client = await TelegramClient('anonymous',self.API_ID,self.API_HASH).start()
    async def getIDS(self):
        if self.client == None:
            return ''
        result = ''
        async for dialog in self.client.iter_dialogs():
            entity = dialog.entity
            if isinstance(entity,types.Channel):
                temp_channel = await self.client.get_entity(entity)
                if temp_channel.megagroup == True or temp_channel.gigagroup == True:
                    result +="Channel(megagroup/gigagroup): " + str(entity.id) + " title: " + entity.title + "\n"
                else:
                    result +="Channel: " + str(entity.id) + " title: " + entity.title + "\n"
            if isinstance(entity,types.Chat):
                result += "Group: " + str(entity.id) + " title: " + entity.title + "\n"
            if isinstance(entity,types.User):
                result += "User: " + str(entity.id) + " name: " + entity.first_name + "\n"
        return result
    def addMessageFilter(self,filter):
        self.messagefilter = filter
        self.messagefilter.Bot = self
    async def startListen(self):
        await self.login()
        print('start forwarding')
        @self.client.on(events.NewMessage)
        async def notify(event):
            try:
                await self.messagefilter.notify(event)
            except Exception as e:
                print(e)
        @self.client.on(events.ChatAction)
        async def join(event):
            if event.user_joined:
                if isinstance(event.action_message.peer_id,types.PeerChannel):
                    me = await self.client.get_me()
                    if event.action_message.from_id.user_id == me.id:
                        self.messagefilter.addDes(event.action_message.peer_id.channel_id)
        group_spider = GroupSpider(self)
        self.group_spider = group_spider
        group_spider.addNodes(self.messagefilter.des_id)
        while True:
            await group_spider.extractUrl()
            