from abc import ABCMeta,abstractmethod
class Plugin:
    __metaclass__ = ABCMeta
    def __init__(self,bot):
        self.bot = bot
    @abstractmethod
    def Register(self):
        self.client=  self.bot.client
    @abstractmethod
    async def run(self):
        pass
    @abstractmethod
    def isLegal(self):
        pass