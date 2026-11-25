from slowapi import Limiter
from slowapi.util import get_remote_address

# Rate limit per IP
limiter = Limiter(key_func=get_remote_address)
