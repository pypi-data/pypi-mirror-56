class ProductPagesException(Exception):
    pass


class ReleaseNotFoundException(ProductPagesException):
    pass


class NoTasksException(ProductPagesException):
    """
    A release has no tasks at all. Product Management must fill in the tasks.
    """
    pass


class TaskNotFoundException(ProductPagesException):
    pass
