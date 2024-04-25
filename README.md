<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/cubstaryow/nonebot-plugin-cyberfurry/blob/master/.github/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/cubstaryow/nonebot-plugin-cyberfurry/blob/master/.github/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-cyberfurry

_✨ nonebot插件 cyberfurry 与赛博狼狼对话吧~ ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/owner/nonebot-plugin-cyberfurry.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-cyberfurry">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-cyberfurry.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">

</div>

## 📖 介绍

官方网站 : [CyberFurry](https://chat.wingmark.cn/)

API申请请通过官方群聊找 群主 申请

### ⚠ 重要

请务必遵守 [用户协议](https://tailnet.cn/?page=yinyingzc)


easycf模型还未填坑,后续更新适配

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-cyberfurry

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-cyberfurry
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-cyberfurry
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-cyberfurry
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-cyberfurry
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_cyberfurry"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置


> [!WARNING]
> 若未配置必填项此插件将不会工作!!!!


| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| cf_appid | 是 | 无 | API的appid |
| cf_token | 是 | 无 | API的token |
| cubplugin_datadir | 否 | "" | 插件数据文件夹 |
| cf_enableistome | 否 | False | 在消息是对bot时是否启用chat |


## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| /chat /cf /yy | 群员 | 否 | 任意 | 触发对话 |
| cf刷新对话 | 群员 | 否 | 任意 | 刷新对话 |
 | cf设定模型 | 群员 | 否 | 任意 | 设定使用的yinying模型,注意,此为个人配置 |
 | cf当前模型 | 群员 | 否 | 任意 |  查看当前模型 |
 | cf模型列表 | 群员 | 否 | 任意 |  查看已加载的模型(包括自定义) |
 | cf设定 fur名字 fur种族 | 群员 | 否 | 任意 | 设定传入yinying的自身设定 |
