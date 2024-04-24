import json
import os
from pathlib import Path
from .cyberfurrymodel import (
    cyberfurry_001,
    easycyberfurry_001,
    yinyingllm_v123,
    config
)
cftype = cyberfurry_001 | easycyberfurry_001 | yinyingllm_v123

promptfile = os.path.dirname(__file__)+"/systemprompt.json"

def getdata():
    with open(promptfile, "r", encoding="utf-8") as f:
        data = json.loads(f.read())
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