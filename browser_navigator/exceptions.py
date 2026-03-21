"""Custom exceptions for browser navigator."""


class BrowserNavigatorError(Exception):
    """Base exception for browser navigator."""
    pass


class XvfbError(BrowserNavigatorError):
    """Xvfb display error."""
    pass


class ChromeLaunchError(BrowserNavigatorError):
    """Failed to launch Chrome."""
    pass


class ProfileError(BrowserNavigatorError):
    """Profile management error."""
    pass


class NavigationError(BrowserNavigatorError):
    """Page navigation error."""
    pass


class ElementNotFoundError(BrowserNavigatorError):
    """Element not found error."""
    pass


class TimeoutError(BrowserNavigatorError):
    """Operation timeout error."""
    pass


class JavaScriptError(BrowserNavigatorError):
    """JavaScript execution error."""
    pass
