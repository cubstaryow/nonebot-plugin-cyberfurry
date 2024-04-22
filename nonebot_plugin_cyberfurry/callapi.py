import aiohttp
from loguru import logger


async def api(
    method:str,
    url:str,
    headers:dict = {},
    cookies:dict = {},
    data:dict = {}
):
    '''异步api调用,复用代码
    '''
    #logger.info(url)
    async with aiohttp.ClientSession() as session:
        async with (
            session.post(url=url,data=data,headers=headers,cookies=cookies) if method == "post" else
            session.get(url=url,headers=headers,cookies=cookies)  
            ) as response:
            type:str = check_type(response.content_type)
            resp = (
                    await response.json() if type == "json" else
                    await response.text() if type == "text" else
                    await response.content.read() if type in ["image","octet-stream"] else
                    f"httpcode:{response.status}\nAPI Data parsing failed")
            for cookie in response.cookies.values():
                cookies[cookie.key] = cookie.coded_value
            return resp , cookies , type

def check_type(type:str):
    content_type =  type.split("/")
    if  content_type[0] == "application":
        return content_type[-1]
    else:
        return content_type[0]
