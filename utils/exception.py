class UserNotFound(Exception):
    """
    用户无法找到
    """

    def __init__(self, user_qq: int):
        self.user_qq = user_qq

    def __str__(self):
        return "{} is an invalid user".format(self.user_qq)


class UserAlreadyExists(Exception):
    """
    用户已存在
    """

    def __init__(self, user_qq: int):
        self.user_qq = user_qq

    def __str__(self):
        return "{} already exists".format(self.user_qq)


class ServerConnectError(Exception):
    """
    无法连接服务器
    """

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg