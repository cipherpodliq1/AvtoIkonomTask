import re
from playwright.sync_api import Page, expect


def wait_for_url_contains(page: Page, fragment: str, timeout: int = 10000) -> None:
    """Wait until the current URL contains the given fragment.

    :param page: Playwright page instance.
    :param fragment: Substring expected in the current URL.
    :param timeout: Maximum wait time in milliseconds.
    """
    expect(page).to_have_url(re.compile(re.escape(fragment)), timeout=timeout)


def assert_element_visible(page: Page, selector: str, message: str = "") -> None:
    """Assert that a single element matched by *selector* is visible.

    :param page: Playwright page instance.
    :param selector: CSS selector string.
    :param message: Descriptive context surfaced on failure.
    """
    loc = page.locator(selector)
    try:
        expect(loc).to_be_visible(timeout=10000)
    except AssertionError:
        if message:
            raise AssertionError(message)
        raise


def reload_and_assert_visible(page: Page, selector: str, message: str = "") -> None:
    """Reload the page and assert the element is still visible.

    Used for persistence checks after create/edit operations.

    :param page: Playwright page instance.
    :param selector: CSS selector string.
    :param message: Descriptive context surfaced on failure.
    """
    page.reload()
    page.wait_for_load_state("networkidle")
    assert_element_visible(page, selector, message)
