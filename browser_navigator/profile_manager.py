"""Chrome profile manager."""
import shutil
import logging
from pathlib import Path
from typing import Optional

from .config import PROFILE_DIR, DEFAULT_PROFILE
from .exceptions import ProfileError

logger = logging.getLogger(__name__)


class ProfileManager:
    """Manages Chrome user profiles."""

    def __init__(self, profile_path: Optional[Path] = None):
        """
        Initialize ProfileManager.

        Args:
            profile_path: Custom profile path. If None, uses default.
        """
        if profile_path:
            self.profile_path = Path(profile_path)
        else:
            self.profile_path = PROFILE_DIR / DEFAULT_PROFILE

    def ensure_profile(self) -> Path:
        """
        Ensure the profile directory exists.

        Returns:
            Path to the profile directory.

        Raises:
            ProfileError: If profile cannot be created.
        """
        try:
            self.profile_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Profile ensured at: {self.profile_path}")
            return self.profile_path
        except Exception as e:
            raise ProfileError(f"Failed to create profile directory: {e}")

    def get_chrome_args(self) -> list:
        """
        Get Chrome command-line arguments for using this profile.

        Returns:
            List of Chrome arguments.
        """
        profile_dir = str(self.profile_path.resolve())
        return [
            f"--user-data-dir={PROFILE_DIR}",
            f"--profile-directory={self.profile_path.name}",
        ]

    @staticmethod
    def list_profiles() -> list:
        """
        List all available profiles.

        Returns:
            List of profile names.
        """
        if not PROFILE_DIR.exists():
            return []
        return [d.name for d in PROFILE_DIR.iterdir() if d.is_dir()]

    def delete_profile(self) -> None:
        """Delete the profile directory."""
        if self.profile_path.exists():
            shutil.rmtree(self.profile_path)
            logger.info(f"Profile deleted: {self.profile_path}")

    def reset_profile(self) -> None:
        """Reset the profile by deleting and recreating it."""
        self.delete_profile()
        self.ensure_profile()
