"""
Rate limiter configuration
"""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# This will be initialized in app.py
limiter = None
