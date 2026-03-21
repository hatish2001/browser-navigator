#!/usr/bin/env python3
"""Example usage of the browser navigator framework."""
import logging

from browser_navigator import Navigator

# Enable logging
logging.basicConfig(level=logging.INFO)


def main():
    """Demonstrate browser navigator capabilities."""
    print("Starting Browser Navigator Example")
    print("=" * 50)

    with Navigator(headless=True) as nav:
        # Navigate to example domain
        print("\n1. Navigating to example.com...")
        nav.navigate("https://example.com")
        nav.wait_for_navigation()

        # Get page title
        print(f"   Page title: {nav.get_current_url()}")

        # Get main heading text
        try:
            heading = nav.get_text("h1")
            print(f"   Heading: {heading}")
        except Exception as e:
            print(f"   Could not get heading: {e}")

        # Take screenshot
        print("\n2. Taking screenshot...")
        nav.screenshot("/tmp/example_home.png")
        print("   Screenshot saved to /tmp/example_home.png")

        # Navigate to page with forms
        print("\n3. Navigating to a page with interactive elements...")
        nav.navigate("https://httpbin.org/forms/post")
        nav.wait_for_navigation()

        # Fill out a form field
        print("   Filling form field...")
        nav.type("input[name='custname']", "Test User")
        nav.type("input[name='custtel']", "555-1234")

        # Take screenshot after form fill
        nav.screenshot("/tmp/example_form.png")
        print("   Screenshot saved to /tmp/example_form.png")

        # Execute JavaScript
        print("\n4. Executing JavaScript...")
        title = nav.execute_js("return document.title")
        print(f"   Page title via JS: {title}")

        # Get element attribute
        print("\n5. Getting element attributes...")
        try:
            form_action = nav.get_attribute("form", "action")
            print(f"   Form action: {form_action}")
        except Exception as e:
            print(f"   Could not get form action: {e}")

        # Find multiple elements
        print("\n6. Finding multiple elements...")
        inputs = nav.find_elements("input")
        print(f"   Found {len(inputs)} input elements")

        # Demonstrate waiting
        print("\n7. Demonstrating wait functionality...")
        nav.navigate("https://example.com")
        element = nav.wait_for("body", state="visible")
        print(f"   Body element found: {element is not None}")

    print("\n" + "=" * 50)
    print("Example completed successfully!")


if __name__ == "__main__":
    main()
