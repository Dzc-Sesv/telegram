import asyncio
import argparse
import sys
from  Bot import Bot
from MessageForward import MessageForward
from GroupSpider import GroupSpider
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
    
    
    if args.printIDS is None:
        message_filter = MessageForward(bot) #消息转发插件
        bot.addPlugin(message_filter)

        group_spider = GroupSpider(bot)
        bot.addPlugin(group_spider)
        asyncio.run(bot.run())