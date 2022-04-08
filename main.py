import json
from telethon import TelegramClient
from telethon import types,utils,functions
import asyncio
import argparse
import re
from telethon.tl.functions.messages import ImportChatInviteRequest
Source=[]
Des=[]
FoundChannel=set()
SourceEntityList = []
DesEntityList = []
API_ID=None
API_HASH=None
async def Forward():
    readMsgIds = []
    client = await TelegramClient('anonymous',API_ID,API_HASH).start()
    pattern1 = re.compile(r'https://t.me/[a-z0-9@#%&*()_+-={}\[\]\\|<>,./?]+',re.I)
    pattern2 = re.compile(r'https://t.me/[a-zA-Z][\w\d]{3,30}[a-zA-Z\d]',re.I)
    async for dialog in client.iter_dialogs():
        entity = dialog.entity
        if entity.id in Source:
            SourceEntityList.append(entity)
        if entity.id in Des:
            DesEntityList.append(entity)
    while True:
        for entity in SourceEntityList:
            msg = await client.get_messages(entity)
            if msg[0].id not in readMsgIds or len(DesEntityList) > 0:
                for item in DesEntityList:
                    print(item.title)
                    #await client.forward_messages(item.id,msg[0].id,entity.id)
                    nameSet = []
                    async for mes1 in client.iter_messages(item):      
                        if mes1.message  is not None and pattern2.search(mes1.message)  is not None:  
                            try:
                                name = pattern2.search(mes1.message).group(0)
                                if name  not in nameSet:
                                    nameSet.append(name)
                                    temp_entity = await client.get_entity(name)
                                    if isinstance(temp_entity,types.Channel) and temp_entity.megagroup == True:
                                        result = await client(functions.channels.JoinChannelRequest(channel=name))
                                    if isinstance(temp_entity,types.Chat):
                                        result = await client(functions.channels.JoinChannelRequest(channel=name))
                                    DesEntityList.append(temp_entity)
                            except Exception as e:
                                print(e)
                                continue
                    DesEntityList.remove(item)
                readMsgIds.append(msg[0].id)
        await asyncio.sleep(10)
async def PrintIDS():
    client = await TelegramClient('anonymous',API_ID,API_HASH).start()
    result = ""
    async for dialog in client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity,types.Channel):
            temp_channel = await client.get_entity(entity)
            if temp_channel.megagroup == True or temp_channel.gigagroup == True:
                result +="Channel(megagroup/gigagroup): " + str(entity.id) + " title: " + entity.title + "\n"
            else:
                result +="Channel: " + str(entity.id) + " title: " + entity.title + "\n"
        if isinstance(entity,types.Chat):
            result += "Group: " + str(entity.id) + " title: " + entity.title + "\n"
        if isinstance(entity,types.User):
            result += "User: " + str(entity.id) + " name: " + entity.first_name + "\n"
    with open("./IDS","w") as out:
        out.write(result)
if __name__ == "__main__":
    config_data = None
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--printIDS",help="显示id")
    parser.add_argument("-c","--config",help="使用配置文件")
    args = parser.parse_args()
    with open('./config.json','r+') as  config:
            data = ''
            for line in config:
                data += line.replace('\n','')
            config_data = json.loads(data)
    if args.printIDS == "file":
        if 'API_ID' in config_data:
            API_ID = config_data['API_ID']
        if 'API_HASH' in config_data:
            API_HASH = config_data['API_HASH']
        asyncio.run(PrintIDS())
    if args.config == 'config':
        if 'source' in config_data:
            Source.extend(config_data['source'])
            print(Source)
        if "destination" in config_data:
            Des.extend(config_data['destination'])
            print(Des)
        if 'API_ID' in config_data:
            API_ID = config_data['API_ID']
        if 'API_HASH' in config_data:
            API_HASH = config_data['API_HASH']
        if len(Source) == 0:
            print('please set source')
        if API_HASH == None or API_ID == None:
            print('please set API_HASH OR API_ID')
        asyncio.run(Forward())