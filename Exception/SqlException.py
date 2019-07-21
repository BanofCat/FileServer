
class SQLException(Exception):
    def __init__(self, msg=None):
        self.msg = msg

    def what(self):
        return self.msg


class DBException(SQLException):
    pass


class ObjectNotExist(SQLException):
    pass


class InputInvalid(Exception):
    pass


