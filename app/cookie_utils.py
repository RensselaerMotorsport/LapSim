import sys

MAX_TOTAL_COOKIE_SIZE = 100000 # Arbutary number tht can be changed later
COOKIE_OVERHEAD = 100

def cookie_size_exceeded(session, new_cookie_key, new_cookie_value):
    total_cookie_size = sum(sys.getsizeof(k) + sys.getsizeof(v) + COOKIE_OVERHEAD for k, v in session.items())
    total_cookie_size += sys.getsizeof(new_cookie_key) + sys.getsizeof(new_cookie_value) + COOKIE_OVERHEAD
    return total_cookie_size >= MAX_TOTAL_COOKIE_SIZE

def new_session_size(session, new_cookie_key, new_cookie_value):
    total_cookie_size = sum(sys.getsizeof(k) + sys.getsizeof(v) + COOKIE_OVERHEAD for k, v in session.items())
    total_cookie_size += sys.getsizeof(new_cookie_key) + sys.getsizeof(new_cookie_value) + COOKIE_OVERHEAD
    return total_cookie_size

def can_add_cookie(session, new_cookie_key, new_cookie_value):
    new_size = new_session_size(session, new_cookie_key, new_cookie_value)
    return new_size <= MAX_TOTAL_COOKIE_SIZE