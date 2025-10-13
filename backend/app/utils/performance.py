"""
Performance monitoring for login API
"""
from functools import wraps
import time
import logging
from fastapi import Request

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def monitor_performance(operation_name: str):
    """Decorator to monitor API performance"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs) if hasattr(func, '__call__') else func(*args, **kwargs)
                end_time = time.time()
                duration = (end_time - start_time) * 1000  # Convert to ms
                
                if duration > 500:  # Log slow operations
                    logger.warning(f"🐌 SLOW {operation_name}: {duration:.1f}ms")
                elif duration > 200:
                    logger.info(f"⚠️ {operation_name}: {duration:.1f}ms")
                else:
                    logger.info(f"✅ {operation_name}: {duration:.1f}ms")
                    
                return result
            except Exception as e:
                end_time = time.time()
                duration = (end_time - start_time) * 1000
                logger.error(f"❌ {operation_name} FAILED after {duration:.1f}ms: {e}")
                raise
        return wrapper
    return decorator