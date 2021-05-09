class Error(Exception):
    """Base class for other exceptions"""
    pass


class InvalidUserNameError(Error):
    """Raised when the username is not present"""
    pass


class InvalidRoomError(Error):
    """Raised when the room is not present"""
    pass
