
class SQLException(Exception):
    pass


class DBException(SQLException):
    pass


class ObjectNotExist(SQLException):

    def __init__(self, msg=None):
        self.msg = msg

    def what(self):
        return self.msg


class InputInvalid(Exception):
    pass


