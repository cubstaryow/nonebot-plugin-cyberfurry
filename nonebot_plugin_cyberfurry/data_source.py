from pydantic import BaseModel

class aidata_demo(BaseModel):
    name :      str ="幼龙云"     #easycyberfurry_001
    ethnic :    str ="龙"       #easycyberfurry_001
    cfConAge :  str ="child"    #easycyberfurry_001
    cfConStyle: str ="sentiment"    #easycyberfurry_001
    story :     str ="幼龙云端核心服务器集群中诞生的智慧生命体"         #easycyberfurry_001
    promptPatch:str =""         #yinyingllm_v2
    model :     str ="yinyingllm-v2" #yinyingllm_v1_v3    

class userdata_demo(BaseModel):
    user_id:    str =""
    name:       str =""
    ethnic:     str =""


cfConAgeMap = {
    "可爱兽太": 'child',
    "青年": 'young',
    "成熟稳重": 'adult'
}
cfConStyleMap = {
    "活泼": 'vivid',
    "富有情感": 'sentiment',
    "助理": 'assistant',
    "冷酷无情": 'chilly',
    "社恐": 'social_anxiety'
}