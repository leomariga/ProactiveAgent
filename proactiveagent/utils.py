"""Utility functions for Proactive AI agents"""

import time
import logging
from typing import Dict, Any, List, Callable
from functools import wraps


def setup_logging(level: str = "INFO") -> logging.Logger:
    """
    Set up logging for the application
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        
    Returns:
        Configured logger
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Suppress verbose debug logs from HTTP libraries and API clients
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('openai').setLevel(logging.WARNING)
    logging.getLogger('openai._base_client').setLevel(logging.WARNING)
    
    return logging.getLogger('active_ai')


def safe_async_call(func: Callable) -> Callable:
    """
    Decorator for safe async function calls with error handling
    
    Args:
        func: Async function to wrap
        
    Returns:
        Wrapped function with error handling
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise
    return wrapper


def format_elapsed_time(seconds: int) -> str:
    """
    Format elapsed time in human-readable format
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted time string
    """
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds}s"
    else:
        hours = seconds // 3600
        remaining_minutes = (seconds % 3600) // 60
        return f"{hours}h {remaining_minutes}m"


def validate_callback(callback: Callable) -> bool:
    """
    Validate that a callback function is callable and has correct signature
    
    Args:
        callback: Function to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not callable(callback):
        return False
    
    # Try to get the function signature
    try:
        import inspect
        sig = inspect.signature(callback)
        # Should accept at least one parameter (the response)
        return len(sig.parameters) >= 1
    except Exception:
        # If we can't inspect, assume it's valid
        return True


def create_message_dict(role: str, content: str, timestamp: float = None) -> Dict[str, Any]:
    """
    Create a standardized message dictionary
    
    Args:
        role: Message role ('user', 'assistant', 'system')
        content: Message content
        timestamp: Optional timestamp (defaults to current time)
        
    Returns:
        Message dictionary
    """
    return {
        'role': role,
        'content': content,
        'timestamp': timestamp or time.time()
    }


def extract_recent_messages(messages: List[Dict[str, Any]], count: int = 10) -> List[Dict[str, str]]:
    """
    Extract recent messages for AI provider (without timestamps)
    
    Args:
        messages: Full message history
        count: Number of recent messages to extract
        
    Returns:
        List of recent messages in AI provider format
    """
    recent = messages[-count:] if len(messages) > count else messages
    return [{'role': msg['role'], 'content': msg['content']} for msg in recent]


def calculate_user_engagement(
    messages: List[Dict[str, Any]], 
    time_window: int = 3600,
    high_threshold: int = 10,
    medium_threshold: int = 3
) -> str:
    """
    Calculate user engagement level based on recent activity
    
    Args:
        messages: Message history
        time_window: Time window in seconds to analyze
        high_threshold: Minimum messages for 'high' engagement
        medium_threshold: Minimum messages for 'medium' engagement
        
    Returns:
        Engagement level: 'low', 'medium', 'high'
    """
    current_time = time.time()
    recent_messages = [
        msg for msg in messages 
        if msg.get('timestamp', 0) > (current_time - time_window) and msg.get('role') == 'user'
    ]
    
    message_count = len(recent_messages)
    
    if message_count >= high_threshold:
        return 'high'
    elif message_count >= medium_threshold:
        return 'medium'
    else:
        return 'low'


def sanitize_context(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize context dictionary for safe AI processing
    
    Args:
        context: Raw context dictionary
        
    Returns:
        Sanitized context dictionary
    """
    sanitized = {}
    
    # Only include safe, serializable values
    safe_keys = [
        'user_engagement', 'urgency', 'topic', 'requires_followup',
        'conversation_length', 'last_activity', 'time_of_day'
    ]
    
    for key in safe_keys:
        if key in context:
            value = context[key]
            if isinstance(value, (str, int, float, bool)):
                sanitized[key] = value
    
    return sanitized