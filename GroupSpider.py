import re
import json
from telethon import types,functions
from Plugin import Plugin
import asyncio
class GroupSpider(Plugin):
    def __init__(self,Bot):
        super().__init__(Bot)
        self.nodes = set()
        self.GroupUrl = set()
        self.Bot = Bot
        config_data = None
        with open('./config.json','r+') as  config:
            data = ''
            for line in config:
                data += line.replace('\n','')
            config_data = json.loads(data)
        if 'source' in config_data:
            for item in config_data['destination']:
                self.addNode(int(item))
    def Register(self):
        super().Register()
    def isLegal(self):
        if len(self.nodes) > 0:
            return True
        return False
    def addNode(self,node):
        self.nodes.add(node)
    def addNodes(self,nodes):
        self.nodes = self.nodes | nodes
    def addUrl(self,url):
        self.GroupUrl.add(url)
    async def extractUrlAndJoin(self):
        pattern  = re.compile(r'https://t.me/[a-zA-Z][\w\d]{3,30}[a-zA-Z\d]',re.I)
        while True:
            for node in self.nodes:
                node_entity = await self.client.get_entity(node)
                async for message in self.client.iter_messages(node_entity):
                    if isinstance(message.message,str):
                        result = pattern.search(message.message)
                        if result is not None and result.group(0) not in self.GroupUrl:
                            name = result.group(0)
                            self.GroupUrl.add(name)
                            try:
                                url_entity = await self.client.get_entity(name)
                                join_result = None
                                if isinstance(url_entity,types.Channel) and url_entity.megagroup == True:
                                    join_result = await self.client(functions.channels.JoinChannelRequest(channel=name))
                                if isinstance(url_entity,types.Chat):
                                    join_result = await self.client(functions.channels.JoinChannelRequest(channel=name))
                                asyncio.sleep(10)
                            except Exception as e:
                                print('catch the exception:')
                                print(e)
                                continue
    async def sleep(self):
        print('GroupSpider sleep')
        await asyncio.sleep(10)
    async def run(self):
        await self.extractUrlAndJoin()