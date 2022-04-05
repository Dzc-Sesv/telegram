from telethon import TelegramClient
from telethon import types,utils
from telethon.tl.functions.messages import SendMessageRequest
import asyncio
from sanic import Sanic
from sanic import response,request,html
from User import User
from sanic_session import Session,InMemorySessionInterface
from jinja2 import Environment,FileSystemLoader
import sys
app = Sanic("tele")
CurrentUser = None
IDAndHash = {}
LastSend = []
@app.route('/index')
async def index(request):
    global CurrentUser
    if CurrentUser!= None:
        return response.redirect('/dialog')
    return response.html("<form action = \"/login \" method = \"post\"   >\
            api_id:  \
                <input name = \"id\" type = \"text\">\
            api_hash:\
                <input name = \"hash\" type = \"text\">\
                <input type = \"submit\">\
            </form>")
@app.route('/login',methods=['POST'])
async def login(request):
    global IDAndHash,CurrentUser
    if CurrentUser != None:
        return response.redirect('/dialog')
    id = request.form.get("id")
    hash = request.form.get("hash")
    if id == None or hash == None:
        return response.redirect('/index')
    IDAndHash.clear()
    IDAndHash[id] = hash
    return response.redirect('/dialog')
@app.route('/login',methods=['GET'])
async def login_get(request):
    return response.redirect('/index')

@app.route('/dialog')
async def dialog(request):
    global IDAndHash,CurrentUser
    if CurrentUser == None:
        if len(IDAndHash) == 0:
            return response.redirect('/index')
        user = None
        for key in IDAndHash.keys():
            user = User(key,IDAndHash[key])
        client = await TelegramClient(user.getAPI_ID()+user.getAPI_Hash(),user.getAPI_ID(),user.getAPI_Hash()).start()
        user.setClient(client)
        CurrentUser = user
    result = []
    async for dialog in CurrentUser.getClient().iter_dialogs():
        entity = dialog.entity
        if isinstance(entity,types.Channel):
            temp = {}
            temp['id'] = entity.id
            temp['title'] = entity.title
            temp_channel = await CurrentUser.client.get_entity(entity)
            if temp_channel.broadcast == True:
                temp['canSend'] = False
            if temp_channel.megagroup == True:
                temp['canSend'] = True
            if temp_channel.gigagroup == True:
                temp['canSend'] = True
            result.append(temp)
        if isinstance(entity,types.Chat):
            temp = {}
            temp['id'] = entity.id
            temp['title'] = entity.title
            temp['canSend'] = True
            result.append(temp)
        if isinstance(entity,types.User):
            temp = {}
            temp['id'] = entity.id
            temp['title'] = entity.first_name
            temp['canSend'] = True
            result.append(temp)
    file_loader = FileSystemLoader('templates')
    env = Environment(loader = file_loader)
    template = env.get_template('checkDialog.html')
    template_content = template.render(Conlist=result,last=LastSend)
    LastSend.clear()
    return html(template_content)
@app.route('/logout')
async def logout(request):
    global CurrentUser
    if CurrentUser is not None:
        del CurrentUser.client
        CurrentUser = None
    return response.redirect('/index')
@app.route('/sendMsg',methods=['POST'])
async def sendMsg(request):
    global CurrentUser
    if CurrentUser == None:
        return response.redirect('/index')
    msgText = request.form.get('msg')
    for item in request.form:
        if item != 'msg':
            LastSend.append(int(item))
            item = 0-int(item)
            readid,peertype = utils.resolve_id(item)
            await CurrentUser.client.send_message(readid,request.form.get('msg'))
    return response.redirect('/dialog')
if __name__ == "__main__":
    app.run(host = '0.0.0.0',port = 7778)
