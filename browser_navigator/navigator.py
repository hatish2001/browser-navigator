"""Navigator class for browser interactions."""
import time
import logging
from typing import Optional, Union, List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
)

from .browser_manager import BrowserManager
from .config import DEFAULT_TIMEOUT
from .exceptions import (
    NavigationError,
    ElementNotFoundError,
    TimeoutError as NavigatorTimeoutError,
    JavaScriptError,
)

logger = logging.getLogger(__name__)


class Navigator:
    """High-level browser navigation and interaction."""

    def __init__(self, browser_manager: Optional[BrowserManager] = None, **kwargs):
        """
        Initialize Navigator.

        Args:
            browser_manager: Existing BrowserManager instance.
            **kwargs: Arguments passed to BrowserManager if not provided.
        """
        if browser_manager:
            self.browser = browser_manager
        else:
            self.browser = BrowserManager(**kwargs)
            self.browser.start()

        self._driver = self.browser.driver
        self._wait = WebDriverWait(self._driver, DEFAULT_TIMEOUT)

    @property
    def driver(self) -> webdriver.Chrome:
        """Get the WebDriver instance."""
        return self._driver

    def navigate(self, url: str) -> None:
        """
        Navigate to a URL.

        Args:
            url: URL to navigate to.

        Raises:
            NavigationError: If navigation fails.
        """
        try:
            self._driver.get(url)
            logger.info(f"Navigated to: {url}")
        except Exception as e:
            raise NavigationError(f"Failed to navigate to {url}: {e}")

    def click(
        self,
        selector: str,
        by: By = By.CSS_SELECTOR,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """
        Click an element.

        Args:
            selector: Element selector.
            by: Selector type (By.CSS_SELECTOR, By.XPATH, etc.).
            timeout: Maximum wait time in seconds.

        Raises:
            ElementNotFoundError: If element is not found.
            NavigatorTimeoutError: If timeout occurs.
        """
        try:
            element = self.wait_for(selector, by=by, timeout=timeout)
            element.click()
            logger.debug(f"Clicked element: {selector}")
        except TimeoutException as e:
            raise NavigatorTimeoutError(f"Timeout waiting for element: {selector}") from e
        except NoSuchElementException as e:
            raise ElementNotFoundError(f"Element not found: {selector}") from e

    def type(
        self,
        selector: str,
        text: str,
        by: By = By.CSS_SELECTOR,
        clear_first: bool = True,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """
        Type text into an element.

        Args:
            selector: Element selector.
            text: Text to type.
            by: Selector type.
            clear_first: Clear existing text before typing.
            timeout: Maximum wait time in seconds.

        Raises:
            ElementNotFoundError: If element is not found.
        """
        try:
            element = self.wait_for(selector, by=by, timeout=timeout)
            if clear_first:
                element.clear()
            element.send_keys(text)
            logger.debug(f"Typed text into: {selector}")
        except NoSuchElementException as e:
            raise ElementNotFoundError(f"Element not found: {selector}") from e

    def wait_for(
        self,
        selector: str,
        by: By = By.CSS_SELECTOR,
        timeout: float = DEFAULT_TIMEOUT,
        state: str = "visible",
    ) -> webdriver.remote.webelement.WebElement:
        """
        Wait for an element.

        Args:
            selector: Element selector.
            by: Selector type.
            timeout: Maximum wait time in seconds.
            state: Element state - "visible", "present", "clickable", "invisible".

        Returns:
            WebElement when found.

        Raises:
            NavigatorTimeoutError: If timeout occurs.
        """
        conditions = {
            "visible": EC.visibility_of_element_located((by, selector)),
            "present": EC.presence_of_element_located((by, selector)),
            "clickable": EC.element_to_be_clickable((by, selector)),
            "invisible": EC.invisibility_of_element_located((by, selector)),
        }

        condition = conditions.get(state, conditions["visible"])

        try:
            element = WebDriverWait(self._driver, timeout).until(condition)
            return element
        except TimeoutException as e:
            raise NavigatorTimeoutError(
                f"Timeout waiting for element ({state}): {selector}"
            ) from e

    def wait_for_navigation(
        self,
        timeout: float = DEFAULT_TIMEOUT,
        wait_for_js: bool = True,
    ) -> None:
        """
        Wait for page navigation to complete.

        Args:
            timeout: Maximum wait time in seconds.
            wait_for_js: Wait for JavaScript to load as well.
        """
        if wait_for_js:
            self._driver.execute_async_script("""
                var callback = arguments[arguments.length - 1];
                if (document.readyState === 'complete') {
                    callback();
                } else {
                    window.addEventListener('load', function() { callback(); });
                }
            """)

        try:
            WebDriverWait(self._driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException as e:
            raise NavigatorTimeoutError("Page navigation timeout") from e

    def get_text(
        self,
        selector: str,
        by: By = By.CSS_SELECTOR,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> str:
        """
        Get text content of an element.

        Args:
            selector: Element selector.
            by: Selector type.
            timeout: Maximum wait time in seconds.

        Returns:
            Element's text content.
        """
        element = self.wait_for(selector, by=by, timeout=timeout)
        return element.text

    def get_attribute(
        self,
        selector: str,
        attribute: str,
        by: By = By.CSS_SELECTOR,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> Optional[str]:
        """
        Get an attribute value of an element.

        Args:
            selector: Element selector.
            attribute: Attribute name.
            by: Selector type.
            timeout: Maximum wait time in seconds.

        Returns:
            Attribute value or None.
        """
        element = self.wait_for(selector, by=by, timeout=timeout)
        return element.get_attribute(attribute)

    def screenshot(self, path: str) -> None:
        """
        Take a screenshot.

        Args:
            path: File path to save screenshot.
        """
        self._driver.save_screenshot(path)
        logger.debug(f"Screenshot saved: {path}")

    def execute_js(self, script: str, *args) -> any:
        """
        Execute JavaScript.

        Args:
            script: JavaScript code to execute.
            *args: Arguments to pass to the script.

        Returns:
            Script result.

        Raises:
            JavaScriptError: If script execution fails.
        """
        try:
            return self._driver.execute_script(script, *args)
        except Exception as e:
            raise JavaScriptError(f"JavaScript execution failed: {e}") from e

    def hover(
        self,
        selector: str,
        by: By = By.CSS_SELECTOR,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """
        Hover over an element.

        Args:
            selector: Element selector.
            by: Selector type.
            timeout: Maximum wait time in seconds.
        """
        element = self.wait_for(selector, by=by, timeout=timeout, state="visible")
        ActionChains(self._driver).move_to_element(element).perform()

    def scroll_to_element(
        self,
        selector: str,
        by: By = By.CSS_SELECTOR,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """
        Scroll an element into view.

        Args:
            selector: Element selector.
            by: Selector type.
            timeout: Maximum wait time in seconds.
        """
        element = self.wait_for(selector, by=by, timeout=timeout)
        self.execute_js("arguments[0].scrollIntoView({block: 'center'});", element)

    def find_elements(
        self,
        selector: str,
        by: By = By.CSS_SELECTOR,
    ) -> List[webdriver.remote.webelement.WebElement]:
        """
        Find all elements matching selector.

        Args:
            selector: Element selector.
            by: Selector type.

        Returns:
            List of WebElements.
        """
        return self._driver.find_elements(by, selector)

    def get_current_url(self) -> str:
        """Get current page URL."""
        return self._driver.current_url

    def get_page_source(self) -> str:
        """Get current page source."""
        return self._driver.page_source

    def refresh(self) -> None:
        """Refresh the current page."""
        self._driver.refresh()

    def go_back(self) -> None:
        """Go back to previous page."""
        self._driver.back()

    def go_forward(self) -> None:
        """Go forward to next page."""
        self._driver.forward()

    def close(self) -> None:
        """Close the browser."""
        self.browser.stop()

    def __enter__(self) -> "Navigator":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
