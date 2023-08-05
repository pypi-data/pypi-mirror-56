# base errors
class ModRCError(Exception):
    """Base class for ModRC errors."""
    pass


class ModRCIntegrityError(ModRCError):
    """Raised when there is an error with the ModRC installation."""
    pass


class ModRCPackageExistsError(ModRCError):
    """Raised when a package already exists."""
    pass


class ModRCPackageDoesNotExistError(ModRCError):
    """Raised when a package does not exist."""
    pass


class ModRCFileExistsError(ModRCError):
    """Raised when a file already exists."""
    pass


class ModRCFileDoesNotExistError(ModRCError):
    """Raised when a file directory does not exist."""
    pass


class ModRCLiveFileDoesNotExistError(ModRCError):
    """Raised when a live file does not exist."""
    pass


class ModRCFilterDoesNotExistError(ModRCError):
    """Raised when a file is compiled when no filters exist for it."""
    pass


class ModRCFilterNameError(ModRCError):
    """Raised when there is an invalid filter name"""
    pass
