import config
from nonebot import on_command, on_fullmatch
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, GroupMessageEvent, Message
from mcstatus import JavaServer
import utils.database

online_players = on_command("在线")

server_info = on_command("服务器信息")

plugin = on_command("插件")


@online_players.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if event.group_id in config.group_id:  # 判断群号
        server = utils.database.Server.get()

        query = server.server_query.query()
        # 在线玩家昵称
        players = query.players.names
        # 服务器玩家最大数量
        max = query.players.max
        # 服务器在线玩家数量
        online = query.players.online

        msg = f"以下玩家正在游玩服务器({online}/{max})：\n{' '.join(map(lambda x: f'[{x}]', players))}"

        await online_players.finish(Message(msg))


@server_info.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if event.group_id in config.group_id:  # 判断群号
        server = utils.database.Server.get()

        query = server.server_query.query()
        raw = query.raw
        # 服务器ip
        host_ip = raw["hostip"]
        # 服务器端口
        host_port = raw["hostport"]
        # 版本
        version = raw["version"]
        # 地图
        map = raw["map"]

        msg = f"IP：{host_ip}\n端口：{host_port}\n版本：{version}\n地图：{map}"

        await server_info.finish(Message(msg))


@plugin.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if event.group_id in config.group_id:  # 判断群号
        server = utils.database.Server.get()

        query = server.server_query.query()
        # 服务器插件列表
        plugins = query.software.plugins

        msg = "以下插件在服务器中启用：\n" + "\n".join(plugins)

        await plugin.finish(Message(msg))
