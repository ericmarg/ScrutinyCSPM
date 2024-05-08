

def is_arg_present(args: tuple, arg_value) -> bool:
    """
    Check if a given argument value is present in the tuple of arguments.

    Args:
        args (tuple): The tuple of arguments to check.
        arg_value: The argument value to search for.

    Returns:
        bool: True if the argument value is present in the tuple of arguments, False otherwise.
    """

    if len(args) > 0:
        if arg_value in args:
            return True
    else:
        return False