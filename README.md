# Browser Navigator

A lightweight browser automation framework using Selenium and Xvfb for headless Chrome operation.

## Features

- **Headless Chrome** via Xvfb virtual display
- **Real Chrome Profile** persistence
- **Anti-Detection** measures (webdriver flag removal, user agent randomization)
- **Simple API** for common browser interactions

## Installation

```bash
# Install system dependencies
sudo apt install xvfb chromium-browser chromium-chromedriver

# Install Python dependencies
pip install -r requirements.txt
```

## Quick Start

```python
from browser_navigator import Navigator

# Simple usage
with Navigator() as nav:
    nav.navigate("https://example.com")
    title = nav.get_text("h1")
    print(f"Page title: {title}")
```

## API Reference

### Navigator

Main class for browser interactions.

#### Navigation

```python
nav = Navigator()

# Navigate to URL
nav.navigate("https://example.com")

# Wait for page load
nav.wait_for_navigation()

# Refresh, back, forward
nav.refresh()
nav.go_back()
nav.go_forward()
```

#### Element Interaction

```python
# Click element
nav.click("#submit-button")

# Type text
nav.type("input[name='email']", "user@example.com")

# Hover
nav.hover(".dropdown-menu")

# Scroll to element
nav.scroll_to_element("#footer")
```

#### Element Reading

```python
# Get text
text = nav.get_text(".content")

# Get attribute
href = nav.get_attribute("a", "href")

# Find all elements
links = nav.find_elements("a")
for link in links:
    print(link.get_attribute("href"))
```

#### Waiting

```python
# Wait for element to be visible
element = nav.wait_for(".loading", state="visible")

# Wait for clickable
nav.wait_for("button", state="clickable")

# Wait for invisible
nav.wait_for(".modal", state="invisible")
```

#### JavaScript

```python
# Execute JavaScript
result = nav.execute_js("return document.title")

# Scroll
nav.execute_js("window.scrollBy(0, 500)")
```

#### Screenshots

```python
nav.screenshot("page.png")
```

### BrowserManager

Lower-level browser lifecycle management.

```python
from browser_navigator import BrowserManager

browser = BrowserManager(headless=True)
browser.start()
driver = browser.driver

# ... use driver ...

browser.stop()
```

### ProfileManager

Manage Chrome user profiles.

```python
from browser_navigator import ProfileManager

# List profiles
profiles = ProfileManager.list_profiles()

# Reset profile
pm = ProfileManager("my-profile")
pm.reset_profile()
```

### XvfbManager

Manage Xvfb virtual displays.

```python
from browser_navigator import XvfbManager

with XvfbManager() as xvfb:
    print(f"Display: {xvfb.display}")
    # Xvfb automatically cleaned up
```

## Configuration

Configuration is stored in `~/.config/browser-navigator/`.

### Profile Directory

Profiles are stored at: `~/.config/browser-navigator/profiles/default/`

### Custom Profile

```python
from pathlib import Path
from browser_navigator import Navigator, ProfileManager

profile = ProfileManager(Path("/custom/profile/path"))
profile.ensure_profile()

nav = Navigator(profile_path=profile.profile_path)
```

## Anti-Detection Features

- Webdriver automation flags disabled
- Real Chrome user agent strings
- Persistent real Chrome profile
- Randomized user agent selection

## Example

See `example.py` for a complete example.

```bash
python example.py
```
