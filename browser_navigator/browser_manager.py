"""Browser manager for Chrome lifecycle."""
import logging
import os
import random
import subprocess
from pathlib import Path
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from .config import (
    CHROME_BINARY,
    CHROMEDRIVER_PATH,
    USER_AGENTS,
    DISABLE_WEBDRIVER,
    RANDOMIZE_USER_AGENT,
    PAGE_LOAD_TIMEOUT,
    IMPLICIT_WAIT,
)
from .xvfb_manager import XvfbManager
from .profile_manager import ProfileManager
from .exceptions import ChromeLaunchError

# Set Chrome binary path for webdriver-manager
os.environ["CHROME_BIN"] = CHROME_BINARY

logger = logging.getLogger(__name__)


class BrowserManager:
    """Manages Chrome browser lifecycle with Xvfb and anti-detection."""

    def __init__(
        self,
        profile_path: Optional[Path] = None,
        headless: bool = True,
        display: Optional[int] = None,
    ):
        """
        Initialize BrowserManager.

        Args:
            profile_path: Custom Chrome profile path.
            headless: Run Chrome in headless mode.
            display: Specific Xvfb display number.
        """
        self.headless = headless
        self.xvfb = XvfbManager(display=display)
        self.profile_manager = ProfileManager(profile_path)
        self._driver: Optional[webdriver.Chrome] = None

    def start(self) -> webdriver.Chrome:
        """
        Start Xvfb and launch Chrome.

        Returns:
            Selenium WebDriver instance.

        Raises:
            ChromeLaunchError: If Chrome fails to launch.
        """
        # Start Xvfb
        display_num = self.xvfb.start()
        logger.info(f"Xvfb started on display :{display_num}")

        # Ensure profile exists
        self.profile_manager.ensure_profile()

        # Configure Chrome options
        options = self._get_chrome_options(display_num)

        try:
            # Use the system chromedriver
            service = Service(CHROMEDRIVER_PATH)

            self._driver = webdriver.Chrome(service=service, options=options)
            self._driver.implicitly_wait(IMPLICIT_WAIT)
            self._driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)

            # Anti-detection: remove webdriver property
            if DISABLE_WEBDRIVER:
                self._driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                    "source": """
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined
                        });
                    """
                })

            logger.info("Chrome started successfully")
            return self._driver
        except Exception as e:
            self.xvfb.stop()
            raise ChromeLaunchError(f"Failed to launch Chrome: {e}")

    def _get_chrome_options(self, display_num: int) -> Options:
        """Build Chrome options with anti-detection measures."""
        options = Options()

        if self.headless:
            options.add_argument("--headless=new")

        # Set Chrome binary explicitly
        options.binary_location = CHROME_BINARY

        # Display
        options.add_argument(f"--display=:{display_num}")

        # Disable webdriver flag (anti-detection)
        if DISABLE_WEBDRIVER:
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

        # User agent
        if RANDOMIZE_USER_AGENT:
            user_agent = random.choice(USER_AGENTS)
            options.add_argument(f"--user-agent={user_agent}")

        # Window size
        options.add_argument("--window-size=1920,1080")

        # Disable sandbox (needed in some environments)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Disable infobars
        options.add_argument("--disable-infobars")

        # Disable extensions
        options.add_argument("--disable-extensions")

        # Disable GPU
        options.add_argument("--disable-gpu")

        # Profile settings
        profile_args = self.profile_manager.get_chrome_args()
        for arg in profile_args:
            options.add_argument(arg)

        return options

    def stop(self) -> None:
        """Stop Chrome and Xvfb."""
        if self._driver is not None:
            try:
                self._driver.quit()
            except Exception as e:
                logger.warning(f"Error quitting Chrome: {e}")
            self._driver = None
            logger.info("Chrome stopped")

        self.xvfb.stop()

    @property
    def driver(self) -> Optional[webdriver.Chrome]:
        """Get the WebDriver instance."""
        return self._driver

    @property
    def is_running(self) -> bool:
        """Check if browser is running."""
        return self._driver is not None and self.xvfb.is_running

    def __enter__(self) -> "BrowserManager":
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stop()