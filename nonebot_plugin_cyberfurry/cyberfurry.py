from .data_source import aidata_demo, userdata_demo
from .jsondata import (
    getdate, getqqdata,
    defqqname, defqqmodel,
    datetime, writehistory,
    loaddata, savedata,
    driver , setqqpushstatus
)
import time
import json

from loguru import logger

from .callapi import api
from .cyberfurrymodel import (
    cyberfurry_001,
    easycyberfurry_001,
    yinyingllm_v123,
    config,
    loadmodel
)
cftype = cyberfurry_001 | easycyberfurry_001 | yinyingllm_v123

apiurl = "https://api-yinying-ng.wingmark.cn/v1/chatWithCyberFurry"



@driver.on_shutdown
async def _():
    savedata(cf.getuserchat())


class cyberfurry:
    headers = {
        'Content-type': 'application/json',
        'Authorization': f'Bearer {config.cf_token}'
    }
    basemodel = {
        #多模型示例
        #"cyberfurry": cyberfurry_001(),
        "easycyberfurry": easycyberfurry_001(),
        "yinying": yinyingllm_v123(),
    }
    model ={
        **basemodel,
        **loadmodel() #配置文件读取并载入
        }
    localdata=loaddata()
    maxtimes = 50
    userchat = localdata.get('userchat',{})
    usertimes = localdata.get('usertimes',{})
    userlife  = localdata.get('userlife',{})
    
    localdata={}

    def __init__(self) -> None:
        pass
    def getuserchat(self):
        return {
            "userchat" : self.userchat,
            "usertimes": self.usertimes,
            "userlife": self.userlife
        }
    def setchat_id(self, user_id):
        timeset = int(time.time())
        chat_id = f"{getdate()}XD{timeset}"
        self.userchat[user_id] = chat_id
        return chat_id

    def getchat_id(self, user_id):
        cid = self.userchat.get(user_id, None)
        if cid == None:
            cid = self.setchat_id(self, user_id)
        return cid

    def makedata(self, user_id, name):
        tmp = getqqdata(user_id)
        modelname = tmp['model']
        userdata = userdata_demo(
            user_id=user_id,
            name=tmp['name'] if tmp['name'] != "未知" else name,
            ethnic=tmp['ethnic']
        )
        aidata = aidata_demo(model=modelname)
        cfmodel: cftype = self.model.get(modelname)
        postdata = cfmodel.buliddata(
            chat_id=self.getchat_id(self, user_id),
            userdata=userdata,
            aidata=aidata
        )
        return postdata

    def initchat(
        self, user_id
    ):
        self.setchat_id(user_id)
        self.getsettimes(user_id, settime=0, init=True)
        return True

    def getsettimes(
        self,
        user_id,
        settime: int = 1,
        init: bool = False
    ):
        times = self.usertimes.get(user_id, None)
        if init or times == None:
            self.usertimes[user_id] = 0
        self.usertimes[user_id] += settime
        return self.usertimes[user_id]

    @classmethod
    async def chat(cls, user_id, name, msg):
        tmp = getqqdata(user_id)
        modelname = tmp['model']
        times = cls.getsettimes(cls, user_id)
        exdata = cls.makedata(cls, user_id=user_id, name=name)
        exdata['message'] = msg
        resp = "API无响应内容"
        try:
            data = json.dumps(exdata)
            resp, _,type = await api(
                "post",
                url=apiurl,
                data=data,
                headers=cls.headers
            
            )
            content: str = resp['choices'][0]['message']['content']
            role: str = resp['choices'][0]['message']['role']
            chat_id = resp["id"]
        except:
            logger.opt(colors=True).error(
                f"{resp}"
            )
            return f"[cyberfurry-E]非预期返回,出错于-api返回值处理\n>{resp.get('data')}", 0
        else:
            if times == 1:
                writehistory(chat_id, resp['model'] +"\n"+ modelname)
            writehistory(
                chat_id, f"[{times:2}/{cls.maxtimes}]user:"+msg)
            writehistory(
                chat_id, f"[{times:2}/{cls.maxtimes}]{role}:"+content)
            if times == 1:
                content += f"\n[ID-{chat_id.split('-')[-1]}]"
            if role !="assistant":
                cls.getsettimes(cls, user_id, settime=-1)
                times += -1
            if times >= cls.maxtimes:
                cls.setchat_id(cls, user_id)
                cls.getsettimes(cls, user_id, settime=0, init=True)
            return content, times
        
    
    def getsetlife(
        self,
        user_id:str ,
        setcycle:int = 0 ,
        memory:str | bool = False,
        init:bool = False
    )->dict:
        data = self.userlife.get(user_id,None)
        if data == None or init == True:
            self.userlife[user_id] = {
                'cycle':0,
                'memory':""
            }
            return self.userlife[user_id]
        self.userlife[user_id]['cycle'] += setcycle
        if memory:
            self.userlife[user_id]['memory'] = memory
        return self.userlife.get(user_id,None)


    @classmethod
    async def chatlife(cls, user_id, name, msg):
        times = cls.getsettimes(cls, user_id)
        exdata = cls.makedata(cls, user_id=user_id, name=name)
        exdata['message'] = msg
        resp = "API无响应内容"
        try:
            data = json.dumps(exdata)
            resp, tmp,type = await api(
                "post",
                url=apiurl,
                data=data,
                headers=cls.headers
            )
            content: str = resp['choices'][0]['message']['content']
            role: str = resp['choices'][0]['message']['role']
        except:
            logger.opt(colors=True).error(
                f"{resp}"
            )
            return f"[cyberfurry-E]非预期返回,出错于-api返回值处理\n>{resp.get('data')}", 0
        else:
            if role !="assistant":
                cls.getsettimes(cls, user_id, settime=-1)
                times += -1
            return content, times
    pass


cf = cyberfurry()

