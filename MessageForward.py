import json
from telethon import types,events,functions
from Plugin import Plugin
class MessageForward(Plugin):
    def __init__(self,client):
        super().__init__(client)
        self.source_id = set()
        self.des_id = set()
        self.message_queue = {}
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
    def Register(self):
        super().Register()
        
        self.bot.registerSingalMap('Joined',self.replay)

        @self.client.on(events.NewMessage)
        async def handle1(event):
            await self.notify(event)
    async def replay(self,msg):
        print(msg)
        me = await self.client.get_me()
        myId = me.id
        for item in self.message_queue.values():
            await self.client.forward_messages(msg,item.id,myId)
        if msg not in self.des_id:
            await self.client(functions.channels.LeaveChannelRequest(msg))
        # if event.user_joined:
            # joinedChannelId = event.action_message.peer_id.channel_id
            # userId = event.action_message.from_id.user_id
            # # me = await self.client.get_me()
            # myId = me.id
            # print(str(userId)+":"+str(myId))
            # if userId == myId:
            #     for item in self.message_queue.values():
            #         await self.client.forward_messages(joinedChannelId,item.id,myId)
            #     entity = await self.client.get_entity(joinedChannelId)
            #     await self.client(functions.channels.LeaveChannelRequest(entity))
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
                await self.client.forward_messages(des_id,event.message.id,id)
            self.message_queue[event.message.message] = event.message
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
    async def run(self):
        pass