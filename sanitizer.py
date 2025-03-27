import re
from typing import Dict, Any, List, Optional
from html import escape

def sanitize_text(text: str) -> str:
    """
    Sanitize text content to prevent XSS and other injection attacks
    
    Args:
        text (str): Input text to sanitize
        
    Returns:
        str: Sanitized text
    """
    if not isinstance(text, str):
        return str(text)
    
    # Escape HTML characters
    text = escape(text)
    
    # Remove any potential script tags
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove any potential event handlers
    text = re.sub(r'on\w+\s*=', '', text, flags=re.IGNORECASE)
    
    return text

def sanitize_url(url: str) -> str:
    """
    Sanitize URLs to prevent injection attacks
    
    Args:
        url (str): Input URL to sanitize
        
    Returns:
        str: Sanitized URL
    """
    if not isinstance(url, str):
        return ""
    
    # Remove any potential javascript: URLs
    url = re.sub(r'javascript:', '', url, flags=re.IGNORECASE)
    
    # Ensure URL starts with http:// or https://
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    return url

def sanitize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively sanitize dictionary values
    
    Args:
        data (Dict[str, Any]): Input dictionary to sanitize
        
    Returns:
        Dict[str, Any]: Sanitized dictionary
    """
    if not isinstance(data, dict):
        return data
    
    sanitized = {}
    for key, value in data.items():
        if isinstance(value, str):
            sanitized[key] = sanitize_text(value)
        elif isinstance(value, dict):
            sanitized[key] = sanitize_dict(value)
        elif isinstance(value, list):
            sanitized[key] = sanitize_list(value)
        else:
            sanitized[key] = value
    
    return sanitized

def sanitize_list(data: List[Any]) -> List[Any]:
    """
    Recursively sanitize list values
    
    Args:
        data (List[Any]): Input list to sanitize
        
    Returns:
        List[Any]: Sanitized list
    """
    if not isinstance(data, list):
        return data
    
    return [sanitize_dict(item) if isinstance(item, dict) else 
            sanitize_list(item) if isinstance(item, list) else 
            sanitize_text(item) if isinstance(item, str) else 
            item for item in data]

def sanitize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize the entire API response
    
    Args:
        response (Dict[str, Any]): API response to sanitize
        
    Returns:
        Dict[str, Any]: Sanitized response
    """
    if not isinstance(response, dict):
        return response
    
    # Sanitize the main response fields
    sanitized = {
        'answer': sanitize_text(response.get('answer', '')),
        'sources': sanitize_list(response.get('sources', [])),
        'data': sanitize_dict(response.get('data', {})),
        'session_id': response.get('session_id')  # Don't sanitize session_id as it's internal
    }
    
    return sanitized 