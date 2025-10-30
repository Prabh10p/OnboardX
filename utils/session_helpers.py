"""
Session State Helper Functions
Prevents type errors and ensures proper initialization
"""

import streamlit as st
from datetime import datetime

def get_or_init_list(key, default_factory):
    """
    Safely get or initialize a list in session state
    
    Args:
        key: session state key
        default_factory: function that returns default list value
    
    Returns:
        list from session state or default
    """
    if key not in st.session_state or not isinstance(st.session_state[key], list):
        st.session_state[key] = default_factory()
    
    return st.session_state[key]

def get_or_init_dict(key, default_factory):
    """
    Safely get or initialize a dict in session state
    
    Args:
        key: session state key
        default_factory: function that returns default dict value
    
    Returns:
        dict from session state or default
    """
    if key not in st.session_state or not isinstance(st.session_state[key], dict):
        st.session_state[key] = default_factory()
    
    return st.session_state[key]

def get_or_init_value(key, default_value):
    """
    Safely get or initialize any value in session state
    
    Args:
        key: session state key
        default_value: default value if not exists
    
    Returns:
        value from session state or default
    """
    if key not in st.session_state:
        st.session_state[key] = default_value
    
    return st.session_state[key]

def ensure_user_data_initialized(user):
    """
    Ensure all user-related session state is properly initialized
    
    Args:
        user: user dictionary
    """
    # Initialize join date if not present
    if 'join_date_full' not in user:
        user['join_date_full'] = datetime.now().isoformat()
    
    # Initialize lists that should exist
    list_keys = ['meetings', 'goals', 'notifications']
    for key in list_keys:
        if key not in st.session_state or not isinstance(st.session_state[key], list):
            st.session_state[key] = []
    
    # Initialize dicts that should exist
    if 'user_preferences' not in st.session_state or not isinstance(st.session_state['user_preferences'], dict):
        st.session_state['user_preferences'] = {
            'theme': 'Light',
            'language': 'English',
            'timezone': 'EST',
            'email_notifications': True,
            'meeting_reminders': True,
            'task_reminders': True
        }

def clear_user_session():
    """Clear all user session data on logout"""
    keys_to_keep = ['signup_step', 'signup_data']
    keys_to_clear = [k for k in st.session_state.keys() if k not in keys_to_keep]
    
    for key in keys_to_clear:
        del st.session_state[key]

def reset_page_state():
    """Reset page-specific state"""
    page_specific_keys = ['scheduling_member', 'show_scheduler', 'calendar_date']
    for key in page_specific_keys:
        if key in st.session_state:
            del st.session_state[key]