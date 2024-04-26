
from nonebot.adapters.onebot.v11 import (
   Bot ,MessageSegment , PrivateMessageEvent
)
from nonebot.matcher import Matcher
from .cyberfurry import *

from nonebot.adapters.onebot.v11 import MessageEvent as obV11event
from nonebot.params import CommandArg
from nonebot import on_command , on_message
from nonebot.rule import to_me ,Rule
from .config import config
try:
    from nonebot.adapters.telegram.event import MessageEvent as TGevent
except:
    TGevent = obV11event

MessageEvent = obV11event | TGevent

async def is_enable():
    return config.cf_enableistome

autorun = on_message(
    rule=to_me() & Rule(is_enable),
    priority=900
)

run = on_command(
    "/chat",
    aliases={"/yy","/cf"} ,
    block=config.cf_enableistome,
    priority=25
)
init = on_command(
    "cf刷新对话",
    aliases={ "cf初始化"} ,
    block=config.cf_enableistome,
    priority=25
)
set = on_command(
    "cf设定模型",
    aliases={ "cf切换模型"} ,
    block=config.cf_enableistome,
    priority=25
)
getset = on_command(
    "cf当前模型",
    block=config.cf_enableistome,
    priority=25
)
getmodellist = on_command(
    "cf模型列表",
    block=config.cf_enableistome,
    priority=25
)
setuser = on_command(
    "cf设定",
    block=config.cf_enableistome,
    priority=25
)


def checkmsg(word):
    blackkey = [
        "草你","草我","操","艹","撅","涩涩",
        "色色","小穴","龙根","肉棒","jb"
        ]
    msg=""
    key =True
    for tmp in blackkey:
        if  tmp in word :
            key =False
            msg ="\n名称不合规"
    return key ,msg

bashethnic = (
    [ "毛毛龙","鳞龙","羽龙","鱼龙","猫猫龙","东龙" ,"小龙雀","龙"] +
    [ "灵狐","龙狐","北极狐","猫狐","鱼狐","狐"] +
    [ "龙狼","狼鲨","狼","狐犬","麟犬","犬"] +
    [ "猫","蛞蝓猫","虎","灵猫","龙猫"] +
    [ "猫猫鱼","飞鱼","龙鱼","鱼"] +
    [ "飞鸟","咕咕鸽","小鸽子","凤凰","金乌","鸟","雀"]
)
def checkethnic(ethnic):
    liste = list(bashethnic)
    if ethnic in liste:
        return True ,""
    msg ="\n种族只支持:\n[" +"|".join(liste) + "]"
    return False ,msg

    
@run.handle()
async def cyberfurryrun(
    bot:Bot,
    event:MessageEvent,
    matcher:Matcher,
    data: list = CommandArg(),  
):
    if len(data)==0:
        return 0
    msg = str(data[0])
    user_id = str(event.user_id)
    matchObj ,_= checkmsg(msg)
    if not matchObj:
        await matcher.send("[幼龙云V5]:参数体不当...停止响应")
        return 0
    userinfo = await bot.get_stranger_info(user_id=user_id)
    name = userinfo.get("nickname","未知")
    if len(msg) > 75:
        await matcher.send(MessageSegment.reply(event.message_id)+"太长力xw")
        return 0 
    retmsg , times = await cf.chat(user_id,name,msg)
    maxtimes = cf.maxtimes
    setqqpushstatus(user_id, False)
    await matcher.send(
        MessageSegment.reply(event.message_id) +
        retmsg +
        (f"\n({times}/{maxtimes},将开启新对话)" if times >=maxtimes else f"\n({times}/{maxtimes}轮对话)")
    )
    
@autorun.handle()
async def cyberfurryautorun(
    bot:Bot,
    event:MessageEvent,
    matcher:Matcher,
):
    await cyberfurryrun(
        bot=bot,
        event=event,
        matcher=matcher,
        data=[event.get_message()]
    )

@setuser.handle()
async def cyberfurrysetuser(
    event:MessageEvent,matcher:Matcher ,args: list = CommandArg()
):
    user_id = str(event.user_id)
    if len(args) <1:
        return 0
    data = str(args[0]).split(" ")
    if (len(data)>=2):
        name = data[0]
        ethnic = data[1]
        msg = "[幼龙云V5]:出现问题"
        key1 ,msg1=checkmsg(name)
        key2 ,msg2= checkethnic(ethnic)
        msg+=msg1+msg2
        if (key1) and (key2):
            data=getqqdata(user_id)
            data["name"]=name
            data["ethnic"]=ethnic
            defqqname(user_id,data)
            await matcher.send(f"[幼龙云V5]:嗯哼,你好,{name}({ethnic})")
        else:
            await matcher.send(f"{msg}")
    else:
        await matcher.send("[幼龙云V5]参数不完整,应为\ncf设定 名称 种族(只支持常用种族)")

@init.handle()
async def cyberfurryinit(
    event:MessageEvent,matcher:Matcher
):
    user_id = str(event.user_id)
    cf.initchat(user_id)
    await matcher.send("[幼龙云V5]已刷新对话")

@getset.handle()
async def cyberfurrygetset(
    event:MessageEvent,matcher:Matcher
):
    user_id = str(event.user_id)
    msg="[幼龙云V5]"
    data = getqqdata(user_id)
    msg +=f"当前模型[{data['model']}]"
    await matcher.send(msg)

@getmodellist.handle()
async def cyberfurrygetmodellist(
    event:MessageEvent,matcher:Matcher
):
    modellist = list(cf.model.keys())
    msg =f"[cyberfurry]可用模型\n"
    msg += "\n".join(modellist)
    await matcher.send(msg)

@set.handle()
async def cyberfurryset(
    event:MessageEvent,matcher:Matcher,
    data: list = CommandArg()
):
    modelname = str(data[0])
    user_id = str(event.user_id)
    msg="[幼龙云V5]"
    if cf.model.get(modelname,None) != None:
        try:
            defqqmodel(user_id,modelname)
        except:
            defqqname(user_id,{
            "name":"未知",
            "ethnic":"狼",
            "model":modelname,
            "push" : False
            })
            msg +="\nWARN-你还未设置设定,请尽快设置\n"
        cf.initchat(user_id)
        msg +=f"设定模型[{modelname}]成功\n(已自动刷新对话)"
    else:
        msg +="模型不存在"
    await matcher.send(msg)
