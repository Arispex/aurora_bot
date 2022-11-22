from nonebot.params import CommandArg, Matcher, Arg, ArgPlainText
from nonebot.typing import T_State
import config
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, GroupMessageEvent, Message
import utils.database

rcon = on_command("执行")


@rcon.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State, args: Message = CommandArg()):
    if event.group_id in config.group_id:  # 判断群号
        if int(event.get_user_id()) in config.admins:  # 判断是否为管理员
            command = args.extract_plain_text()  # 获取命令
            if command:
                server = utils.database.Server.get()
                response = server.command(command)

                if not response:  # 判断response返回信息是否为空
                    response = "似乎没有返回的内容"

                msg = f"执行成功，返回以下内容：\n{response}"

                await rcon.finish(Message(msg))
            else:
                await rcon.finish("用法错误\n执行 <command>")
        else:
            await rcon.finish("权限不足")
