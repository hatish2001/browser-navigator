"""Browser Navigator - Lightweight browser automation framework."""
from .browser_manager import BrowserManager
from .navigator import Navigator
from .profile_manager import ProfileManager
from .xvfb_manager import XvfbManager
from .config import (
    CONFIG_DIR,
    PROFILE_DIR,
    DEFAULT_PROFILE,
    CHROME_BINARY,
    USER_AGENTS,
    DEFAULT_TIMEOUT,
)
from .exceptions import (
    BrowserNavigatorError,
    XvfbError,
    ChromeLaunchError,
    ProfileError,
    NavigationError,
    ElementNotFoundError,
    TimeoutError,
    JavaScriptError,
)

__version__ = "0.1.0"

__all__ = [
    # Main classes
    "BrowserManager",
    "Navigator",
    "ProfileManager",
    "XvfbManager",
    # Config
    "CONFIG_DIR",
    "PROFILE_DIR",
    "DEFAULT_PROFILE",
    "CHROME_BINARY",
    "USER_AGENTS",
    "DEFAULT_TIMEOUT",
    # Exceptions
    "BrowserNavigatorError",
    "XvfbError",
    "ChromeLaunchError",
    "ProfileError",
    "NavigationError",
    "ElementNotFoundError",
    "TimeoutError",
    "JavaScriptError",
]