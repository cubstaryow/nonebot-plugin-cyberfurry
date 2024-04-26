import asyncio
import random
from nonebot import on_command , on_regex, require ,logger
try:
    require("nonebot_plugin_apscheduler")
    from nonebot_plugin_apscheduler import scheduler
    logger.opt(colors=True).debug(
        "<g>nonebot_plugin_apscheduler已安装，将可以使用定时任务功能</g>"
    )
except:
    scheduler = None
    logger.opt(colors=True).warning(
        "<r><bg #FFCC33>nonebot_plugin_apscheduler未安装，将无法使用定时任务功能</bg #FFCC33></r>"
    )
    
from nonebot import get_bot
from nonebot.adapters.onebot.v11 import(
    Bot, ActionFailed,
    PrivateMessageEvent    
)
from .config import config
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from .cyberfurry import *
from nonebot.params import RegexGroup
from .jsondata import loadpushlist , savepushlist , getqqdata ,setqqpushstatus

global pushlist
pushlist = []
pushlist = loadpushlist()

turn_push = on_regex(
    r"^(开启|关闭)对话推送服务$",
    block=True,
    priority=25
)
@turn_push.handle()
async def _(
    evnet : PrivateMessageEvent,
    matcher : Matcher,
    args : list = RegexGroup(),
):
    if not scheduler:
        await matcher.finish("[失败]核心依赖未安装!")
    user_id = str(evnet.user_id)
    userdata = getqqdata(user_id)
    if userdata["name"]=="未知":
        await matcher.finish("[失败]请先设置你的设定信息\n(cf设定 名字 种族)")
    global pushlist
    if str(args[0]) == "开启":
        if user_id in pushlist:
            await matcher.finish(f"你已启用推送服务")
        else:
            msg = "[成功]银影会来缠着你聊天喔w"
            pushlist.append(user_id)
            savepushlist(pushlist)
    else:
        if user_id not in pushlist:
            await matcher.finish(f"你未启用推送服务")
        else:
            msg = "[成功]那银影就不打扰你啦w"
            pushlist.remove(user_id)
            savepushlist(pushlist)
    await matcher.finish(msg)

turn_text = on_command(
    "测试推送服务1",
    block=True,priority=25,
    permission=SUPERUSER)
@turn_text.handle()
async def _():
    await autochat_scheduler()

turn_text2 = on_command(
    "测试推送服务2",
    block=True,priority=25,
    permission=SUPERUSER)
@turn_text2.handle()
async def _():
    await autochatgroup_scheduler()


async def autochat_scheduler():
    global pushlist
    bot: Bot = get_bot()
    for user_id in pushlist:
        userdata = getqqdata(user_id)
        if not userdata.get('push',True):
            setqqpushstatus(user_id,True)
            continue
        msg , _ = await cf.chat(
            user_id,
            userdata["name"],
            "(生成一段想找星佑聊天的话,比如“现在已经晚上xx点了欸,你已经很久没有找我聊天了耶w,什么时候来找我说说话qwq”,你不能直接输出这个例句,你必须根据现在的状态生成)"
        )
        try:
            await bot.send_private_msg(user_id=int(user_id), message=msg)
        except ActionFailed as e:
            logger.warning(f"向用户 {user_id} 推送失败，可能是机器人与此人不是好友 {repr(e)}")
            pushlist.remove(user_id)
            savepushlist(pushlist)
        await asyncio.sleep( random.randint(5, 30))

async def autochatgroup_scheduler():
    bot: Bot = get_bot()
    group_list = await bot.get_group_list()
    for groupinfo in group_list:
        group_id = groupinfo['group_id']
        if str(group_id) in config.cf_autogrouplist:
            if random.randint(1, 100) < 20:
                msg = "[Auto]银影:\n(悄悄的看群里正在干嘛)qwq"
                await bot.send_group_msg(group_id=int(group_id), message=msg)


if scheduler:
    scheduler.add_job(
        autochat_scheduler, "cron", hour='6,12,18,21', minute=10, id="cyberfurry-autochat1"
    )
    scheduler.add_job(
        autochatgroup_scheduler, "cron", hour='8-22', id="cyberfurry-autochat2"
    )