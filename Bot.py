from this import d
from telethon import TelegramClient,types
import json
import asyncio
from GroupSpider import GroupSpider
import sys
class Bot:
    def __init__(self):
        self.API_ID = ''
        self.API_HASH = ''
        self.client = None
        self.plugins = []
        self.messagefilter = None
        self.group_spider = None
        self.singal = []
        self.singalmap = {}
        self.msgqueue = {}
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
    def registerSingalMap(self,Singal:str,handle):
        self.singalmap[Singal] = handle
    def addSingal(self,Singal,msg):
        print('addSingal')
        self.singal.append(Singal)
        self.msgqueue[len(self.msgqueue)] = msg
        print(self.singal)
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
    def addPlugin(self,plugin):
        if plugin.isLegal():
            self.plugins.append(plugin)
        else:
            sys.exit(0)
    async def process(self):
        while True:
            if len(self.singal) > 0:
                for index,singal in enumerate(self.singal):
                    if singal in self.singalmap.keys():
                        await self.singalmap[singal](self.msgqueue[index])
                    continue
                self.singal.clear()
                self.msgqueue.clear()
            await asyncio.sleep(1)
    async def run(self):
        if self.isLegal():
            await self.login()
            tasks = []
            for plugin in self.plugins:
                plugin.Register()
                tasks.append(plugin.run())
            tasks.append(self.process())
            await asyncio.wait(tasks)
            print('1')
        else:
            sys.exit(0)