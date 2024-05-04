from nonebot.adapters.onebot.v11 import (
   Bot,MessageEvent 
)
from nonebot.adapters.onebot.v11 import GroupMessageEvent as onebotV11GroupMessageEvent
from nonebot.params import CommandArg
from nonebot import on_command
from nonebot.matcher import Matcher
from .cyberfurry import cf
from .jsondata import gethistorydata #,gethistorytxt ,gethistorylist

history = on_command(
    "cf导出对话",
    aliases={ "cf导出历史"} ,
    block=True,
    priority=25
)

 #暂不支持,请等待后续更新
@history.handle()
async def cyberfurryhistory(
    bot:Bot,event:MessageEvent,matcher:Matcher,cdata: list = CommandArg()
):
    user_id = str(event.user_id)
    if len(cdata)==0:
        filename = cf.getchat_id(user_id).split("-")[-1]
    else:
        filename = str(cdata[0])
    msg_list =[]
    data = gethistorydata(user_id,filename)
    if not data:
        await matcher.finish("[cyberfurry]文件不存在或该ID没有对话数据")
    await msglist_add(
        msg_list,
        f"[cyberfurry]\nID-{filename}-的对话历史\n模式:{data[0]}",
        event.self_id
    )
    setdata = list(data[1:])
    while(1):
        a = await longdata(setdata)
        msg = "\n".join(setdata[:a])
        id = event.self_id
        await msglist_add(msg_list,msg,id)
        del setdata[:a]
        if len(setdata) == 0:
            break
    await sendfm(msg_list,bot,event,matcher)

async def longdata(data) -> int:
    lt = 0
    long = 0
    for tmp in data:
        lt += 1
        long += len(tmp)
        if long >= 3000:
            return lt-1
    return None

async def msglist_add( msg_list , data ,user_id):
    msg_list.append(
        {
            "type": "node",
            "data": {
                "name":"幼龙云端核心-cyberfurry",
                "uin": user_id,
                "content": data
                }
            }
        )

async def sendfm(msg_list,bot,event,matcher):
    if isinstance(msg_list,list):
        if isinstance(event, onebotV11GroupMessageEvent):
            await bot.send_group_forward_msg(group_id=event.group_id, messages=msg_list)  # type: ignore
        else:
            await bot.send_private_forward_msg(user_id=event.user_id, messages=msg_list)
    else:
        await matcher.finish(msg_list)


'''
historylist = on_command(
    "cf对话历史",
    aliases={ "cf历史对话"} ,
    priority=25
)


@historylist.handle()
async def cyberfurryhistorylist(
    event:MessageEvent,matcher:Matcher,
):
    user_id = str(event.user_id)
    try:
        flist =gethistorylist(user_id=user_id)
        msg = str("[cyberfurry]历史对话文件列表\n"+"[ "+  
            (" ]\n[ ".join(flist))  +" ]")
    except:
        msg = "[cyberfurry]文件不存在"
    await matcher.send(msg)
    pass
'''
'''
gethistory = on_command(
    "cf获取对话历史文件",
    aliases={ "cf获取历史对话文件"} ,
    priority=25
)
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
'''