from loguru import logger
from .plugins_data import initdata,wdata,rdata,driver,data_dir
import os
from datetime import datetime
jsonname = "cyberfurry.json"
tempname = "cybertemp.json"
txtdir = "cyberfurry"
bashdata = {
    "status":1,
    "userdata":{},
    "autopush":[]
}
initdata(jsonname,bashdata)
initdata(tempname,{})


#====================推送服务========================

def loadpushlist():
    temp = rdata(jsonname)
    return temp.get("autopush",[])

def savepushlist(data):
    temp = rdata(jsonname)
    temp["autopush"]=data
    wdata(jsonname,temp)

def setqqpushstatus(
    user_id :int|str,
    push :bool = True,
):
    
    temp = rdata(jsonname)
    temp['userdata'][str(user_id)]["push"]=push
    wdata(jsonname,temp)


#====================历史对话文件存储 测试版========================
txt_dir =  data_dir / txtdir
if not os.path.isdir(txt_dir):
    os.mkdir(txt_dir)

def writehistory(
    chat_id:str,
    text:str
):
    data = chat_id.split("-")
    file_path=txt_dir / f"{data[1]}"
    if not os.path.isdir(file_path):
        os.mkdir(file_path)
    with open(file_path / (data[-1]+".txt"),'a') as f:
        f.write(text)

def gethistorylist(
    user_id:str
):
    file_path=txt_dir / "{user_id}/"
    filelist = os.listdir(file_path)
    flist = []
    for name in filelist:
        flist.append(name.split(".")[0])
    if len(flist)>=5:
        return flist[-5:].sort()
    else:
        return flist.sort()

def gethistorytxt(
    user_id:str,
    filename:str
):
    file_path=txt_dir / f"{user_id}"
    filelist = os.listdir(file_path)
    if filename+".txt" in filelist:
        return file_path / (filename+".txt")
    else:
        return False

#==================== 核心数据文件存储 ========================
def getdate():
    now = datetime.now()
    date_time = now.strftime("%y%m%d")
    return (date_time)

def defqqname(
    user_id :int|str,
    userdata :dict = {
        "name":"未知",
        "ethnic":"狼",
        "model" :"yinyingllm-v2",
        "push" : False
    }
):
    temp = rdata(jsonname)
    temp['userdata'][str(user_id)]=userdata
    wdata(jsonname,temp)
    return True

def defqqmodel(
    user_id :int|str,
    usermodel :str = "cf",
):
    
    temp = rdata(jsonname)
    temp['userdata'][str(user_id)]["model"]=usermodel
    wdata(jsonname,temp)
    return True

def getqqdata(
    user_id :int|str,
):
    temp = rdata(jsonname)
    return temp['userdata'].get(str(user_id),{
        "name":"未知",
        "ethnic":"狼",
        "model" :"yinyingllm-v2",
        "push" : False
        }
    )

#==================== 重启时的状态重启 ========================
def loaddata():
    temp = rdata(tempname)
    return temp

def savedata(data):
    temp = rdata(tempname)
    temp=data
    wdata(tempname,temp)