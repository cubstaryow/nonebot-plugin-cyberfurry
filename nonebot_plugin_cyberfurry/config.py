from nonebot import get_driver
from pydantic import BaseModel


class cyberfurry(BaseModel):
    cf_appid :str = ""
    cf_token :str = ""
    cubplugin_datadir : str=""
    cf_enableistome : bool = False
config: cyberfurry = cyberfurry.parse_obj(get_driver().config.dict())
