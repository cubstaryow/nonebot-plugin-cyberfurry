from loguru import logger
from .plugins_data import initdata,wdata,rdata,driver,data_dir
import os
from datetime import datetime
jsonname = "cyberfurry.json"
txtdir = "cyberfurry"
bashdata = {
    "status":1,
    "qqname":{},
    "usermodel":{},
    "userdata":{},
    "userchat":{}
}
initdata(jsonname,bashdata)
txt_dir =  data_dir / txtdir
if not os.path.isdir(txt_dir):
    os.mkdir(txt_dir)

def writehistory(
    chat_id:str,
    text:str
):
    data = chat_id.split("-")
    file_path=txt_dir+f"/{data[1]}"
    if not os.path.isdir(file_path):
        os.mkdir(file_path)
    with open(file_path+"/"+data[-1]+".txt",'a') as f:
        f.write(text)

def gethistorylist(
    user_id:str
):
    file_path=txt_dir+f"/{user_id}/"
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
    file_path=txt_dir+f"/{user_id}"
    filelist = os.listdir(file_path)
    if filename+".txt" in filelist:
        return file_path+"/"+filename+".txt"
    else:
        return False

def getdate():
    now = datetime.now() # current date and time
    date_time = now.strftime("%y%m%d")
    return (date_time)

def defqqname(
    user_id :int|str,
    userdata :dict = {
        "name":"未知",
        "ethnic":"狼",
        "model" :"yinyingllm-v2"
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
        "model" :"yinyingllm-v2"
        }
    )

def loaddata():
    temp = rdata(jsonname)
    return temp.get("userchat",{})

def savedata(data):
    temp = rdata(jsonname)
    temp["userchat"]=data
    wdata(jsonname,temp)