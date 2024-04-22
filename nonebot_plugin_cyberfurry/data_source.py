from pydantic import BaseModel

class aidata_demo(BaseModel):
    name :      str ="幼龙云"     #easycyberfurry_001
    ethnic :    str ="龙"       #easycyberfurry_001
    cfConAge :  str ="child"    #easycyberfurry_001
    cfConStyle: str ="chilly"    #easycyberfurry_001
    story :     str =""         #easycyberfurry_001
    promptPatch:str =""         #yinyingllm_v2
    model :     str ="yinyingllm-v2" #yinyingllm_v1_v3    

class userdata_demo(BaseModel):
    user_id:    str =""
    name:       str =""
    ethnic:     str =""
