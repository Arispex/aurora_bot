from mcstatus import JavaServer
import mcrcon
import utils.exception


class Server:
    """
    服务器对象
    """
    def __init__(self, host: str, query_port: int, rcon_port: int, rcon_password: str):
        """
        初始化
        :param host: 主机地址
        :param query_port: 查询端口
        :param rcon_port: 远程指令端口
        :param rcon_password: 远程指令密码
        """
        self.server_query = JavaServer.lookup(f"{host}:{query_port}", timeout=1)
        try:
            self.server_query.query().map  # 测试是否能连接查询端口
        except TimeoutError:  # 不能连接查询端口则报错
            raise utils.exception.ServerConnectError("Can't connect to server, please check the query_port.")

        self.server_rcon = mcrcon.MCRcon(host=host, port=rcon_port, password=rcon_password, timeout=1)
        try:
            self.server_rcon.connect()  # 测试是否能连接远程指令端口
        except (ConnectionRefusedError, TimeoutError):
            raise utils.exception.ServerConnectError("Can't connect to server, please check the rcon_port.")

    def command(self, cmd: str) -> str:
        """
        远程指令
        :param cmd: 指令内容
        :return: 返回结果
        """
        return self.server_rcon.command(cmd)

    def __del__(self):
        """
        回收垃圾
        :return:
        """
        self.server_rcon.disconnect()


