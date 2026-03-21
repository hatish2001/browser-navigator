"""Xvfb manager for virtual display allocation."""
import subprocess
import logging
from pathlib import Path
from typing import Optional

from .config import XVFB_DISPLAY_START, XVFB_DISPLAY_RANGE
from .exceptions import XvfbError

logger = logging.getLogger(__name__)


class XvfbManager:
    """Manages Xvfb virtual display lifecycle."""

    def __init__(self, display: Optional[int] = None):
        """
        Initialize XvfbManager.

        Args:
            display: Specific display number to use. If None, auto-allocates.
        """
        self.display: Optional[int] = display
        self._process: Optional[subprocess.Popen] = None

    def start(self) -> int:
        """
        Start Xvfb with an available display.

        Returns:
            Display number that was allocated.

        Raises:
            XvfbError: If Xvfb cannot be started.
        """
        if self._process is not None:
            raise XvfbError("Xvfb is already running")

        # Find an available display
        display_num = self._find_available_display()

        try:
            # Start Xvfb
            self._process = subprocess.Popen(
                ["Xvfb", f":{display_num}", "-screen", "0", "1920x1080x24", "-ac"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            # Wait for Xvfb to start
            import time
            time.sleep(0.5)

            # Check if process is still running
            if self._process.poll() is not None:
                _, stderr = self._process.communicate()
                raise XvfbError(
                    f"Xvfb failed to start on display :{display_num}: {stderr.decode()}"
                )

            self.display = display_num
            logger.info(f"Xvfb started on display :{display_num}")
            return display_num

        except FileNotFoundError:
            raise XvfbError("Xvfb not found. Install with: sudo apt install xvfb")
        except XvfbError:
            raise
        except Exception as e:
            self._process = None
            raise XvfbError(f"Failed to start Xvfb: {e}")

    def _find_available_display(self) -> int:
        """Find an available display number."""
        if self.display is not None:
            return self.display

        # Just try displays sequentially - if one fails, move to the next
        for i in range(XVFB_DISPLAY_START, XVFB_DISPLAY_START + XVFB_DISPLAY_RANGE):
            # Check if display file exists (indicating display in use)
            display_file = f"/tmp/.X{i}-lock"
            if not Path(display_file).exists():
                return i

        raise XvfbError("No available Xvfb display found")

    def stop(self) -> None:
        """Stop Xvfb."""
        if self._process is not None:
            self._process.terminate()
            try:
                self._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._process.kill()
                self._process.wait()
            self._process = None
            logger.info(f"Xvfb stopped on display :{self.display}")
            self.display = None

    @property
    def is_running(self) -> bool:
        """Check if Xvfb is running."""
        return self._process is not None and self._process.poll() is None

    def __enter__(self) -> "XvfbManager":
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stop()