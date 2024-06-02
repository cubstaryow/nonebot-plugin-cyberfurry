from nonebot import get_bot, on_regex
from nonebot.adapters.onebot.v11 import(
    PrivateMessageEvent    
)
from nonebot.matcher import Matcher
from .cyberfurry import *
from nonebot.params import RegexGroup
from nonebot.permission import SUPERUSER
from .jsondata import  getqqdata ,setlifemodestatus

# 内测功能，暂不开放？

turn_life = on_regex(
    r"^切换(生命模式|标准对话)$",
    block=True,
    permission=SUPERUSER,
    priority=25
)

@turn_life.handle()
async def _(
    evnet : PrivateMessageEvent,
    matcher : Matcher,
    args : list = RegexGroup(),
):
    user_id = str(evnet.user_id)
    userdata = getqqdata(user_id)
    if userdata["name"]=="未知":
        await matcher.finish("[失败]请先设置你的设定信息\n(cf设定 名字 种族)")
    cf.initchat(user_id)
    if str(args[0]) == "生命模式":
        msg = "[成功](发癫)我要给它...完整的一生"
        setlifemodestatus(user_id,status=True)
    else:
        msg = "[成功]切换为标准对话"
        setlifemodestatus(user_id,status=False)
    await matcher.finish(msg)


from nonebot.adapters.onebot.v11 import (
   Bot ,MessageEvent,MessageSegment
)
from nonebot.params import CommandArg

async def cyberfurryliferun(
    bot:Bot,
    event:MessageEvent,
    matcher:Matcher,
    data: list = CommandArg(),  
):
    if len(data)==0:
        return 0
    msg = str(data[0])
    user_id = str(event.user_id)
    if msg == "重置循环":
        cf.initchat(user_id)
        cf.getsetlife(user_id,init=True)
        await matcher.send("[循环...重置..生命..初始化.缓存..清空..]")
        return 0
    if msg == "重启循环节":
        cf.initchat(user_id)
        await matcher.send("[循环节...重启..]")
        return 0
    time = cf.getsettimes(user_id,settime=0)
    sendmsg = ""
    userlife = cf.getsetlife(user_id=user_id)
    cycle = userlife.get('cycle')
    memory = userlife.get("memory")
    if time == 0 and memory != "":
        sendmsg += f"(你必须根据如下信息继续进行对话\n{memory})\n"
    sendmsg += "（当无法维持自我时，请输出“行为认知出现混乱”）\n"
    retmsg , times = await cf.chatlife(user_id,"用户",sendmsg + msg)
    othermsg = ""
    if times >= 6:
        memorysend = "（详细记录之前的对话核心信息，同时记录当前所处的位置、你的动作、说话的语气，以及你的感受，以便你将来能够回忆起这段对话。本次只能输出记忆）"
        #memorysend = "（用简洁的语言概括一下之前的对话，以及位置、动作、说话的语气、你的内心状态，形成记忆，方便日后回忆，本次只能输出记忆）"
        retmemory , _ = await cf.chatlife(user_id,"用户",memorysend)
        logger.info( retmemory )
        if "行为认知出现混乱" in retmemory or len(retmemory)<10:
            othermsg += "\n(记忆导出失败...此循环节作废)"
            cf.initchat(user_id)
        else:
            cf.getsetlife(user_id,setcycle=1,memory=retmemory)
            othermsg += "\n(记忆...进入循环...)"
            cf.initchat(user_id)
    if "行为认知出现混乱" in retmsg:
        othermsg += "\n(混乱的循环...请<重启循环节>)"
    setqqpushstatus(user_id, False)
    head = ""
    if not isinstance(event , PrivateMessageEvent):
        head = MessageSegment.reply(event.message_id)
    await matcher.send(
        head + retmsg + othermsg + f"\n[循环...{cycle}C..{times}T]"
    )
    