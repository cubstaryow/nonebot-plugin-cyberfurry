from nonebot.plugin import PluginMetadata
from loguru import logger
from .config import cyberfurry , config

__plugin_meta__ = PluginMetadata(
    name="cyberfurry",
    description="nonebot插件 cyberfurry 与赛博狼狼对话吧~",
    usage='''/chat 触发对话
cf刷新对话 刷新对话
cf设定模型 设定使用的yinying模型
cf当前模型 查看当前模型
cf设定 设定传入yinying的自身设定
    ''',

    type="application",
    # 发布必填，当前有效类型有：`library`（为其他插件编写提供功能），`application`（向机器人用户提供功能）。

    homepage="https://github.com/cubstaryow/nonebot-plugin-cyberfurry",
    # 发布必填。

    config=cyberfurry,
    # 插件配置项类，如无需配置可不填写。

    supported_adapters={"~onebot.v11" , "~telegram"},
    # 支持的适配器集合，其中 `~` 在此处代表前缀 `nonebot.adapters.`，其余适配器亦按此格式填写。
    # 若插件可以保证兼容所有适配器（即仅使用基本适配器功能）可不填写，否则应该列出插件支持的适配器。
)
if config.cf_appid == "" or config.cf_token == "" :
    logger.opt(colors=True).error(
        "cyberfurry缺失核心配置!!!!!取消载入核心!!!"
    )
else:
    from .cyberinit import *
    from .cyberhistory import * 
    
if config.cf_auto:
    from .cyberauto import *
else:
    logger.opt(colors=True).debug(
        "<red>cyberfurry自动对话推送服务已关闭</red>"
    )