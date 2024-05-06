import sys

def is_arg_present(arg_value):
    if arg_value in sys.argv:
        return True
    else:
        return False