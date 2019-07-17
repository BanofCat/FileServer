class HttpException(Exception):
    def __init__(self, msg=None):
        self.msg = msg

    def what(self):
        return self.msg


class NeedLogin(HttpException):

    def __init__(self, msg=None):
        self.msg = msg
        super(NeedLogin, self).__init__()
