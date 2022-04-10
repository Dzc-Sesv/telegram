import re
from telethon import types,functions
class GroupSpider:
    def __init__(self,Bot):
        self.nodes = set()
        self.GroupUrl = set()
        self.Bot = Bot 
    def addNodes(self,node):
        self.nodes = self.nodes | node
    def addUrl(self,url):
        self.GroupUrl.add(url)
    async def extractUrl(self):
        pattern  = re.compile(r'https://t.me/[a-zA-Z][\w\d]{3,30}[a-zA-Z\d]',re.I)
        for node in self.nodes:
            node_entity = await self.Bot.client.get_entity(node)
            async for message in self.Bot.client.iter_messages(node_entity):
                if isinstance(message.message,str):
                    result = pattern.search(message.message)
                    if result is not None and result.group(0) not in self.GroupUrl:
                        name = result.group(0)
                        print(name)
                        self.GroupUrl.add(name)
                        try:
                            url_entity = await self.Bot.client.get_entity(name)
                            join_result = None
                            if isinstance(url_entity,types.Channel) and url_entity.megagroup == True:
                                join_result = await self.Bot.client(functions.channels.JoinChannelRequest(channel=name))
                            if isinstance(url_entity,types.Chat):
                                join_result = await self.Bot.client(functions.channels.JoinChannelRequest(channel=name))
                        except Exception as e:
                            print('catch the exception:')
                            print(e)
                            continue