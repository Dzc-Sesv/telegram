from telethon import TelegramClient
from telethon import types,utils,functions
import asyncio
import argparse
import re
import sys
from  Bot import Bot
from MessageFilter import MessageFilter
from telethon.tl.functions.messages import ImportChatInviteRequest

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