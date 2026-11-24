from slowapi import Limiter
from slowapi.util import get_remote_address

# Counts requests per client IP address, used on login and register
limiter = Limiter(key_func=get_remote_address)
