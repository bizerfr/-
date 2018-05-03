import itchat
import os


# 回复用userId
userId = ''

# 获取好友消息
@itchat.msg_register([itchat.content.TEXT,itchat.content.PICTURE,itchat.content.RECORDING])
def reply(msg):
    # 让小冰回答
    global userId
    userId = msg['FromUserName']
    if msg['Type']=='Recording': #itchat目前不能转发语音
        itchat.send_msg('不听不听，王八念经！', userId)
    else:
        xbAnswer(msg)



# 向智能小冰提问
def xbAnswer(msg):
    xb = itchat.search_mps(name='小冰')[0]
    if msg['Type']=='Text':
        itchat.send_msg(msg['Text'], xb['UserName'])
    elif msg['Type'] == 'Picture':
        msg['Text'](msg['FileName']) #下载文件
        fileinfo = os.stat(msg['FileName'])
        if fileinfo.st_size==0: #itchat目前不能转发微信商店表情
            itchat.send_msg('看不见你发的表情', userId)
        itchat.send_image(msg['FileName'],xb['UserName'])


# 群信息
@itchat.msg_register([itchat.content.TEXT,itchat.content.PICTURE], isGroupChat = True)
def group_reply(msg):
    fromUserName = msg['FromUserName'];
    group = itchat.search_chatrooms(userName=fromUserName)
    #print(group['NickName'] + "群的 " + msg['ActualNickName'] + " 发来的消息\n" + getText(msg) )

    if msg['isAt'] == True :
        global userId
        userId = msg['FromUserName']
        xbAnswer(msg)

# 群信息
@itchat.msg_register(itchat.content.PICTURE, isGroupChat = True)
def group_pic(msg):
    msg['Text'](msg['FileName'])
    itchat.send_image(msg['FileName'])

#捕获公众号消息
@itchat.msg_register([itchat.content.TEXT,itchat.content.PICTURE,itchat.content.RECORDING], isMpChat = True)
def map_reply(msg):
    global userId
    if msg['Type']=='Text':
        itchat.send_msg(msg['Text'], userId)
    elif msg['Type'] == 'Picture':
        msg['Text'](msg['FileName'])
        itchat.send_image(msg['FileName'],userId)
    elif msg['Type']=='Recording':
        msg['Text'](msg['FileName'])
        itchat.send_file(msg['FileName'],userId)


# 获取昵称
def getUserNickName(msg):
    fromUserName = msg['FromUserName']
    fromUser = itchat.search_friends(userName=fromUserName)
    nickName = fromUser['NickName']
    return nickName





itchat.auto_login(hotReload=True)
itchat.run()
itchat.logout()