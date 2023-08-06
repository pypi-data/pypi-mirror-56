from functools import wraps

def greet_user(user):
    return "Hello {}".format(user)

def log_input_output(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        return response
    return wrapper