from telethon import TelegramClient
from telethon import types,utils,functions
import asyncio
import argparse
import re
import sys
from  Bot import Bot
from MessageFilter import MessageFilter
from telethon.tl.functions.messages import ImportChatInviteRequest

FoundChannel=set()
SourceEntityList = []
DesEntityList = []
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
async def PrintIDS(bot,filename):
    await bot.login()
    idsData = await bot.getIDS()
    with open(filename,'w') as out:
        out.write(idsData)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--printIDS",help="显示id")
    parser.add_argument("-c","--config",help="使用配置文件")
    args = parser.parse_args()
    
    bot = Bot()
    if args.printIDS is not None:
        if bot.isLegal():
            asyncio.run(PrintIDS(bot,args.printIDS))
        sys.exit(0)
    
    message_filter = MessageFilter()
    if args.printIDS is None:
        if bot.isLegal() and message_filter.isLegal():
            bot.addMessageFilter(message_filter)
            asyncio.run(bot.startListen())
        sys.exit(0)