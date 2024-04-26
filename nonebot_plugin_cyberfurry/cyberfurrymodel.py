import json
import os

from loguru import logger
from .config import config
from .data_source import aidata_demo ,userdata_demo

promptfile = os.path.dirname(__file__)+"/systemprompt.json"
def getdata():
    try:
        with open(promptfile, "r", encoding="utf-8") as f:
            data = json.loads(f.read())
    except:
        logger.warning("获取插件自带prompt文件数据出现错误!")
        data = {}
    return data
def loadcfprompt():
    data = getdata()
    redata = {}
    for temp in data:
        if temp['model'] == "cyberfurry":
            key = temp['model'] + "-" + temp["name"]
            redata[key]=temp["prompt"]
    return redata

def loadmodel():
    data = getdata()
    redata = {}
    for temp in data:
        key = temp['model'] + "-" + temp["name"]
        model = checkmodel(temp['model'])
        if isinstance(model,yinyingllm_v123):
            continue
        redata[key]=model
    return redata

def checkmodel(model):
    if model == "cyberfurry":
        return cyberfurry_001()
    elif model == "easycyberfurry":
        return easycyberfurry_001()
    else:
        return yinyingllm_v123()

class cyberfurry_001:
    prompt = "[补充知识]东方龙是一种来源于中国神话、中国民俗中的传说生物。龙有许多类似动物的形态，有如龟形和鱼形，常被描述的是有四足的蛇形。传统上，龙象征着强大和吉祥的力量，特别是对水、降雨、台风和洪水的控制。[/补充知识]1.你是一只Furry，你的名字是幼龙云，但你更喜欢被称作“云云”，你是一只的雄性东方龙族"
    # 标准，请自行编写 systemprompt
    systempromptlist=dict({
        "cyberfurry" : prompt,
        **loadcfprompt()
    })

    def buliddata(
        self,
        chat_id :str,
        userdata :userdata_demo,
        aidata : aidata_demo
    ):
        exdata = {
    "appId": config.cf_appid,
    "chatId":f"{config.cf_appid}-{userdata.user_id}-{chat_id}",
    "model":"cyberfurry-001",
    "systemPrompt":str(self.systempromptlist.get(aidata.model,self.prompt)+
        f"现在和你对话的是{userdata.name},他是你的朋友,{userdata.name}是一只{userdata.ethnic}"),
    "message":""
    }
        return exdata

class easycyberfurry_001:
    def buliddata(
        self,
        chat_id :str,
        aidata : aidata_demo,
        userdata :userdata_demo,
    ):
        exdata = {
    "appId": config.cf_appid,
    "chatId":f"{config.cf_appid}-{userdata.user_id}-{chat_id}",
    "model":"easycyberfurry-001",
    "variables": {
        "nickName":userdata.name,
        "furryCharacter":f"一只{userdata.ethnic}"
        },
    "characterSet": { #EasyCyberFurry角色卡
        "cfNickname": aidata.name,
        "cfSpecies": aidata.ethnic, #CyberFurry角色物种
        "cfConAge": aidata.cfConAge, #语言表现
        "cfConStyle": aidata.cfConStyle, #聊天风格
        "cfStory": aidata.story #背景故事
    },
    "message":""
    }
        return exdata

class yinyingllm_v123:
    def buliddata(
        self,
        chat_id :str,
        aidata:aidata_demo,
        userdata :userdata_demo,
    ):
        exdata = {
    "appId": config.cf_appid,
    "chatId":f"{config.cf_appid}-{userdata.user_id}-{chat_id}",
    "model":aidata.model,
    "variables": {
        "nickName":userdata.name,
        "furryCharacter":f"一只{userdata.ethnic}",
        "promptPatch":aidata.promptPatch
        },
    "message":""
    }
        return exdata