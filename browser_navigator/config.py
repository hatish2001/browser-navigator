"""Configuration for browser navigator."""
import os
from pathlib import Path

# Base directories
HOME = Path.home()
CONFIG_DIR = HOME / ".config" / "browser-navigator"
PROFILE_DIR = CONFIG_DIR / "profiles"
DEFAULT_PROFILE = "default"

# Ensure directories exist
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
PROFILE_DIR.mkdir(parents=True, exist_ok=True)

# Xvfb settings
XVFB_DISPLAY_START = 99
XVFB_DISPLAY_RANGE = 100  # Number of displays to try

# Chrome settings - prefer snap chromium on ARM
SNAP_CHROME = "/snap/chromium/current/usr/lib/chromium-browser/chrome"
SYSTEM_CHROME_PATHS = [
    "/usr/bin/google-chrome",
    "/usr/bin/chromium-browser",
    "/usr/bin/chromium",
]

CHROME_BINARY = os.environ.get("CHROME_BINARY")
if CHROME_BINARY and Path(CHROME_BINARY).exists():
    pass
else:
    # Check snap chrome first (for ARM)
    if Path(SNAP_CHROME).exists():
        CHROME_BINARY = SNAP_CHROME
    else:
        # Fall back to system chrome
        CHROME_BINARY = next(
            (p for p in SYSTEM_CHROME_PATHS if Path(p).exists()),
            "/usr/bin/chromium-browser"
        )

# Chromedriver
CHROMEDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH", "/snap/chromium/current/usr/lib/chromium-browser/chromedriver")

# Default user agents (real Chrome versions)
USER_AGENTS = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
]

# Anti-detection options
DISABLE_WEBDRIVER = True
RANDOMIZE_USER_AGENT = True

# Default timeouts (seconds)
DEFAULT_TIMEOUT = 30
IMPLICIT_WAIT = 5
PAGE_LOAD_TIMEOUT = 60