from nonebot.adapters.onebot.v11 import (
   Bot,MessageEvent 
)
from nonebot.adapters.onebot.v11 import GroupMessageEvent as onebotV11GroupMessageEvent
from nonebot.params import CommandArg
from nonebot import on_command
from nonebot.matcher import Matcher
from .cyberfurry import *
from .jsondata import gethistorylist,gethistorytxt


historylist = on_command(
    "cf对话历史",
    aliases={ "cf历史对话"} ,
    priority=25
)
gethistory = on_command(
    "cf获取对话历史文件",
    aliases={ "cf获取历史对话文件"} ,
    priority=25
)

@historylist.handle()
async def cyberfurryhistorylist(
    event:MessageEvent,matcher:Matcher,
):
    user_id = str(event.user_id)
    flist =gethistorylist(user_id=user_id)
    msg = str("[cyberfurry]历史对话文件列表\n"+"[ "+  
        (" ]\n[ ".join(flist))  +" ]")
    await matcher.send(msg)
    pass

@gethistory.handle()
async def cyberfurrygethistory(
    bot:Bot,event:MessageEvent,matcher:Matcher,data: list = CommandArg()
):
    if len(data)==0:
        return 0
    filename = data[0]
    user_id = str(event.user_id)
    if isinstance(event,onebotV11GroupMessageEvent):
        path=gethistorytxt(user_id,filename)
        if path:
            await bot.call_api("upload_group_file",group_id=event.group_id,file=path)
            return
    await matcher.send("[cyberfurry]文件发送失败,可能适配器不支持或者文件不存在(obV11暂不支持私聊!)")


'''  #暂不支持,请等待后续更新
async def furrybarhistory(bot:Bot,event:MessageEvent,matcher,**other):
    msg_list =[]
    user_id = str(event.user_id)
    model = getqqmodel(user_id)
    await msglist_add(msg_list,"幼龙云端核心",f"[furrybar]\n{user_id}的对话历史\n模式:{model}",event.self_id)
    data = fb.getuserchat(user_id)
    for tmp in data:
        role = tmp['role']
        content = tmp['content']
        msg = f"{role}\n{content}"
        id = user_id if role=="user" else event.self_id
        await msglist_add(msg_list,role,msg,id)
    await sendfm(msg_list,bot,event,matcher)
    pass

async def msglist_add( msg_list,name , data ,user_id):
    msg_list.append(
        {
            "type": "node",
            "data": {
                "name":name,
                "uin": user_id,
                "content": data
                }
            }
        )

async def sendfm(msg_list,bot,event,matcher):
    if isinstance(msg_list,list):
        if isinstance(event, GroupMessageEvent):
            await bot.send_group_forward_msg(group_id=event.group_id, messages=msg_list)  # type: ignore
        else:
            await bot.send_private_forward_msg(user_id=event.user_id, messages=msg_list)
    else:
        await matcher.finish(msg_list)
'''
