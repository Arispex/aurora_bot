from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, GroupMessageEvent, Message
import config

menu = on_command("菜单")


@menu.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if event.group_id == config.group_id:  # 判断群号
        services = ["在线", "服务器信息", "插件", "执行"]

        msg = "\n\n".join(services)

        await menu.finish(msg)