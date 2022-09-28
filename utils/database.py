import sqlite3
import model.user
import model.server
import utils.exception
import config


def execute(sql: str, fetch_method: str = "none") -> list | None:
    """
    执行sql
    :param fetch_method: fetch方法(none, one, all)
    :param sql: sql语句
    :return: 结果
    """
    conn = sqlite3.connect("bot.sqlite")
    cursor = conn.cursor()
    cursor.execute(sql)
    match fetch_method:
        case "none":
            result = None
        case "one":
            result = cursor.fetchone()
        case "all":
            result = cursor.fetchall()

    cursor.close()
    conn.commit()
    conn.close()

    return result


class User:
    @staticmethod
    def add(qq: int, player_name: str):
        """
        添加新用户
        :param qq: 用户QQ
        :param player_name: 用户绑定昵称
        :return:
        """
        if User.GetInfo.by_qq(qq):  # 用户是否存在
            raise utils.exception.UserAlreadyExists(qq)
        else:
            execute("insert into user (qq, player_name) values ('%s', '%s')" % (qq, player_name))  # 插入数据库

    @staticmethod
    def delete(qq: int):
        """
        删除用户
        :param qq: 用户QQ
        :return:
        """
        if User.GetInfo.by_qq(qq):  # 用户是否存在
            execute("delete from user where qq = '%s'" % qq)  # 删除数据库
        else:
            raise utils.exception.UserNotFound(qq)

    class GetInfo:
        """
        获取用户信息
        """

        @staticmethod
        def by_qq(qq: int) -> list | None:
            """
            获取指定用户信息
            :param qq: 用户QQ
            :return: 用户信息
            """
            user_info = execute("select * from user where qq = '%s'" % qq, fetch_method="one")
            if user_info:  # 用户是否存在
                return user_info
            else:  # 用户不存在
                return None

        @staticmethod
        def by_name(player_name: str) -> list | None:
            """
            获取指定用户信息
            :param player_name: 用户绑定昵称
            :return: 用户信息
            """
            user_info = execute("select * from user where player_name = '%s'" % player_name, fetch_method="one")
            if user_info:  # 用户是否存在
                return user_info
            else:  # 用户不存在
                return None

        @staticmethod
        def all() -> list:
            """
            获取指定用户信息
            :return: 所有用户信息
            """
            user_info = execute("select * from user", fetch_method="all")
            return user_info

    class Get:
        """
        获取用户对象
        """

        @staticmethod
        def by_qq(qq: int) -> model.user.User | None:
            """
            获取指定用户对象
            :param qq: 用户QQ
            :return: 用户信息
            """
            try:  # 用户是否存在
                user = model.user.User(qq)
                return user
            except utils.exception.UserNotFound:
                return None

        @staticmethod
        def by_name(player_name: str) -> model.user.User | None:
            """
            获取指定用户对象
            :param player_name: 用户绑定昵称
            :return: 用户信息
            """
            user_info = User.GetInfo.by_name(player_name)
            if user_info:
                return model.user.User(user_info[0])
            else:
                return None

        @staticmethod
        def all() -> list[model.user.User]:
            """
            获取所有用户的对象列表
            :return: 所有用户的对象列表
            """
            users_info = utils.database.User.GetInfo.all()
            users = []
            for i in users_info:
                users.append(model.user.User(i[0]))
            return users


class Server:
    @staticmethod
    def get():
        return model.server.Server(config.host, config.query_port, config.rcon_port, config.rcon_password)