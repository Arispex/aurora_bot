from nonebot.params import CommandArg
from nonebot.typing import T_State
import config
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, GroupMessageEvent, Message
import utils.database

bind = on_command("绑定")

player_info = on_command("玩家信息")

unbind = on_command("解除绑定")


@bind.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State, args: Message = CommandArg()):
    if event.group_id in config.group_id:  # 判断群号
        player_name = args.extract_plain_text()  # 获取命令
        if player_name:  # 语法是否正确
            player = utils.database.User.Get.by_qq(int(event.get_user_id()))
            if player:  # 是否已经绑定过了
                await bind.finish("绑定失败，您已经绑定过了。")
            else:
                player = utils.database.User.Get.by_name(player_name)
                if player:  # 此昵称是否被其他玩家绑定
                    await bind.finish("绑定失败，此昵称已被其他玩家绑定，请更换其他昵称。")
                else:
                    state["player_name"] = player_name  # 添加到state
        else:
            await bind.finish("用法错误\n绑定 <nickname>")


@bind.got("action", prompt="您确定绑定此昵称吗？一旦绑定后无法修改。请回复：是 / 否")
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    match str(state["action"]):  # 判断用户回复
        case "是":  # 绑定
            server = utils.database.Server.get()
            server.command(f"easywl add {state['player_name']}")
            utils.database.User.add(int(event.get_user_id()), state['player_name'])

            await bind.finish("绑定成功，请使用此昵称加入服务器。")
        case default:  # 不绑定
            await bind.finish("好的，再想想吧🤔。")


@player_info.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State, args: Message = CommandArg()):
    if event.group_id in config.group_id:  # 判断群号
        player_name = args.extract_plain_text()  # 获取填写的玩家昵称或QQ
        if player_name:  # 判断是否填写了玩家昵称（是否查询自己）
            if player_name.isdigit():  # 判断是昵称还是QQ号
                player = utils.database.User.Get.by_qq(int(player_name))
            else:
                player = utils.database.User.Get.by_name(player_name)
        else:
            player = utils.database.User.Get.by_qq(int(event.get_user_id()))

        if player:  # 判断是否存在此玩家
            await player_info.finish(f"QQ：{player.qq}\n"
                                     f"绑定昵称：{player.player_name}")
        else:
            await player_info.finish("查询失败，此玩家不存在。")


@unbind.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State, args: Message = CommandArg()):
    if event.group_id in config.group_id:  # 判断群号
        if int(event.get_user_id()) in config.admins:  # 判断是否为管理员
            player_name = args.extract_plain_text()  # 获取填写的玩家昵称或QQ
            if player_name:  # 判断是否填写了玩家昵称（是否查询自己）
                if player_name.isdigit():  # 判断是昵称还是QQ号
                    player = utils.database.User.Get.by_qq(int(player_name))
                else:
                    player = utils.database.User.Get.by_name(player_name)
                if player:  # 判断玩家是否存在
                    utils.database.User.delete(player.qq)
                    await unbind.finish("解除绑定成功。")
                else:
                    await unbind.finish("解除绑定失败，此玩家不存在。")
            else:
                await unbind.finish("用法错误\n"
                                    "解除绑定 <QQ>|<nickname>")

        else:
            await unbind.finish("权限不足")