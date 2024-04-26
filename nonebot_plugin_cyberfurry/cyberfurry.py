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
        "cyberfurry": cyberfurry_001(),
        "easycyberfurry": easycyberfurry_001(),
        "yinyingllm-v1": yinyingllm_v123(),
        "yinyingllm-v2": yinyingllm_v123(),
        "yinyingllm-v3": yinyingllm_v123()
    }
    model ={
        **basemodel,
        **loadmodel()
        }
    localdata=loaddata()
    maxtimes = 16
    userchat = localdata.get('userchat',{})
    usertimes = localdata.get('usertimes',{})
    
    localdata={}

    def __init__(self) -> None:
        pass
    def getuserchat(self):
        return {
            "userchat" : self.userchat,
            "usertimes": self.usertimes
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
        times = cls.getsettimes(cls, user_id)
        exdata = cls.makedata(cls, user_id=user_id, name=name)
        exdata['message'] = msg
        try:
            data = json.dumps(exdata)
            resp, _,type = await api(
                "post",
                url=apiurl,
                data=data,
                headers=cls.headers
            
            )
            content: str = resp['choices'][0]['message']['content']
            chat_id = resp["id"]
        except:
            logger.opt(colors=True).error(
                f"{resp}"
            )
            return f"[cyberfurry-E]非预期返回,请检查控制台", 0
        else:
            if times == 1:
                writehistory(chat_id, resp['model']+"\n")
            writehistory(
                chat_id, f"[{times:2}/{cls.maxtimes}]  user   :"+msg+"\n")
            writehistory(
                chat_id, f"[{times:2}/{cls.maxtimes}]assistant:"+content+"\n")
            if times >= cls.maxtimes:
                cls.setchat_id(cls, user_id)
                cls.getsettimes(cls, user_id, settime=0, init=True)
            return content, times
    pass


cf = cyberfurry()

