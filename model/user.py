import utils.database
import utils.exception


class User:
    """
    用户对象
    """
    def __init__(self, qq: int):
        """
        初始化
        :param qq: 用户QQ
        """
        user_info = utils.database.User.GetInfo.by_qq(qq)  # 查找用户
        if user_info:  # 如果存在
            self.qq = user_info[0]
            self.player_name = user_info[1]
        else:  # 不存在则报错
            raise utils.exception.UserNotFound(qq)
